import time
import json
import logging
import threading
from random import random

import redis


class AutoKnightError(Exception):
    pass


class AutoKnight(object):
    """
    judge处理方式：
    1：判断服务qps
    2：更新catch_present
    3：按比例降级服务，当前服务级百分比为100%时，仍然保持max(0.1%, 100)流量进行尝试，以便更改需降级比例。
    save_status 处理方式
    1：将当前status,delay 存储到redis中
    2：如果当前正常状态，且status = False or delay > tolerate_max_delay, 计算降级比例
    3: 如果当前为降级状态，计算降级比例
    calculate_present 计算降级比例
    1：如果当前为正常状态，获取全部队列错误和delay，计算需降级的比例，存储至redis
    2：如果当前为部分降级状态，计算降级比例应为前present * granularity 个(保证试错的实时响应)，存储至redis
    3：如果当前为全部降级状态，有一次成功后，将redis错误队列清空，qps释放至20%，存储至redis
    """

    KNIGHT_ERROR_DELAY_PREFIX = 'auto_knight/granularity/error_delay/{consul_name}'  # 时间窗口内的服务情况
    CONSUL_KNIGHT_PRESENT_PREFIX = 'auto_knight/present/{consul_name}'  # float 需要降级的比例
    CONSUL_QPS_PREFIX = 'auto_knight/qps/{consul_name}/{time_stamp}'  # 服务qps

    def __init__(self, redis_client, consul_name,
                 granularity=100,
                 tolerate_max_delay=3000,
                 tolerate_max_error=0.1,
                 tolerate_present=0.1,
                 care_min_qps=None,
                 qps_window=1,
                 min_retry_qps_present=0.01,
                 fuse_recover_step=0.01,
                 fuse_recover_delay=1000,
                 **kwargs):
        """
        自动熔断类
        在监控粒度内，发生错误 或 延迟时，将会计算此时服务延迟率或错误率
        当平均延迟大于tolerate_max_delay(ms)或错误率大于tolerate_max_error，此时的熔断比例将产生，公式为max(错误比例, 延迟比例)
        当产生的熔断比例大于tolerate_present时，开启熔断
        当熔断到100%时，仍然会开启min_retry_qps_present流量尝试恢复，最小0.001
        当计算熔断比例小于当前熔断比例时，熔断比例下降，下降步长=fuse_recover_step，下降间隔=fuse_recover_delay(ms)
        用法：
        import redis
        redis_client = redis.StrictRedis(host,port)
        autoknight = AutoKnight(redis_client, 'text_consul_name')
        # 用法1
        try:
            with autoknight:
                you_method()
        except AutoKnightError:
            print 'consul was fused'
        except Exception as e:
            print e
        # 用法2
        try:
            autoknight.judge()
            start_time = time.time()
            you_method()
            autoknight.save_status(True, int((time.time() - start_time) * 1000))
        except AutoKnightError:
            print 'consul was fused'
            # 注意，当熔断时不要将此状态存入autoknight.save_status，这样会导致恢复时的异常。
        except Exception as e:
            autoknight.save_status(False, int((time.time() - start_time) * 1000))
            print e
        :param redis_client: redis client，存储窗口和服务信息
        :param granularity: 监控粒度，次
        :param tolerate_max_delay: 监控窗口内平均延迟熔断标志 毫秒
        :param tolerate_max_error: 监控窗口内错误量熔断标志 占监控窗口中的比例
        :param care_min_qps: 熔断起作用的最小qps
        :param qps_window: qps 统计窗口 秒
        :param min_retry_qps_present: 完全不可用时的测试qps
        :param fuse_recover_step: 熔断恢复比例步长，用于熔断恢复时，防止流量突然暴涨 百分比
        :param fuse_recover_delay: 熔断恢复步长之间的延迟，用于熔断恢复时，防止流量突然暴涨 毫秒
        :param kwargs:
        :except AutoKnightError: 熔断error
        """
        assert isinstance(redis_client, redis.StrictRedis), 'redis_client should be kv/pyredis.redis_client.RedisClient'
        self.redis_client = redis_client
        self.consul_name = consul_name
        self.granularity = granularity
        self.tolerate_max_delay = tolerate_max_delay
        self.tolerate_max_error = tolerate_max_error
        self.tolerate_present = tolerate_present
        self.care_min_qps = care_min_qps
        self.qps_window = max(qps_window, 1)
        self.min_retry_qps_present = 1 - float(max(min_retry_qps_present, 0.001))
        self.fuse_recover_step = min(fuse_recover_step, 1)
        self.fuse_recover_delay = max(fuse_recover_delay, 0)
        self.kwargs = kwargs

        self.local_param = threading.local()
        self.cache_present = 0  # 缓存上次获取的降级比例
        self._last_recover_time_stemp = time.time()  # 缓存上次解除熔断时间

        self.knight_error_delay_key = AutoKnight.KNIGHT_ERROR_DELAY_PREFIX.format(consul_name=self.consul_name)
        self.knight_present_key = AutoKnight.CONSUL_KNIGHT_PRESENT_PREFIX.format(consul_name=self.consul_name)

    def _get_qps(self, auto_increase=True, check_size=3):
        """
        获取前2个window 的平均qps
        :param auto_increase: 是否当前访问加一
        :param check_size: 检查窗口数量，不要超过6个
        :return:
        """
        now = int(int(time.time()) / self.qps_window) * self.qps_window
        keys = [AutoKnight.CONSUL_QPS_PREFIX.format(consul_name=self.consul_name,
                                                    time_stamp=str(now - (i * self.qps_window))) for i in
                range(check_size)]
        if auto_increase:
            value = self.redis_client.incrbyfloat(keys[0], 1.0)
            if value < 2:
                # 第一次加入这个key，设置过期时间
                self.redis_client.expire(keys[0], 60)
        values = self.redis_client.mget(keys[1:])
        value_len, sum_value = 0, 0
        for v in values:
            if not v:
                continue
            value_len, sum_value = value_len + self.qps_window, sum_value + float(v)
        return 0 if value_len <= 0 else sum_value * 1.0 / value_len

    def _present_return(self, present):
        # 全部降级时，也要留1%流量重试
        if random() < min(present, self.min_retry_qps_present):
            raise AutoKnightError('%s fuse error, present=%s' % (self.consul_name, present))
        return True

    def judge(self):
        """
        判断consul 是否可用
        :return: True or raise AutoKnightError
        """
        if self.care_min_qps:
            # 判断当前qps
            qps = self._get_qps()
            if self.cache_present == 0 and qps < self.care_min_qps:
                return True
        # 获取当前降级比例
        redis_present = self.redis_client.get(self.knight_present_key)
        if not redis_present:
            redis_present = 0
        present = float(redis_present)
        if present < self.tolerate_present:
            present = 0.0
        self.cache_present = present
        return self._present_return(present)

    def save_status(self, status, delay):
        """
        保存当前访问状态和延迟
        :param status: bool True or False
        :param delay: 延迟时间 毫秒
        :return: None or present
        """
        status = int(bool(status))
        delay = int(delay)
        self._save2redis(status, delay)
        # 有问题，需要进行
        if status == 0 or delay > self.tolerate_max_delay:
            present = self.calculate_present(status, delay)
            if present > self.tolerate_present:
                return present
        # 已经在熔断状态，必须进行熔断检查，方便后续恢复
        if self.cache_present:
            present = self.calculate_present(status, delay)
            if present > self.tolerate_present:
                return present
        return None

    def calculate_present(self, status=None, delay=None):
        """
        计算当前降级比例
        :return: present
        """
        present = 0
        range_len = self.granularity
        if self.cache_present:
            # 如果当前处于降级状态，则只取前cache_present 数据进行计算， 降级比例为100%时，取最近访问的一次结果
            range_len = max(int(range_len * (1 - self.cache_present)), 1)
        error_delay_list = self.redis_client.lrange(self.knight_error_delay_key, 0, range_len)
        if not error_delay_list:
            error_delay_list = []
        error_list, delay_list = [], []
        for i in error_delay_list:
            try:
                error, delay = json.loads(i)
                error_list.append(int(error))
                delay_list.append(float(delay))
            except:
                continue
        # 计算延迟比例
        if delay:
            delay_list.append(delay)
        delay_list_len = len(delay_list)
        avg_delay = sum(delay_list) * 1.0 / delay_list_len
        if avg_delay > self.tolerate_max_delay:
            present = len(map(lambda x: x > self.tolerate_max_delay, delay_list)) * 1.0 / delay_list_len
        else:
            pass

        # 计算错误比例
        if status is not None:
            error_list.append(int(bool(not status)))
        error_list_len = len(error_list)
        avg_error = sum(error_list) * 1.0 / error_list_len
        if avg_error > self.tolerate_max_error:
            present = max(present, avg_error)
        else:
            pass

        # 当从完全熔断恢复时，清空所有error，delay队列
        if self.cache_present >= 1 and present == 0:
            self.redis_client.ltrim(self.knight_error_delay_key, 0, 1)
            # 计算恢复熔断step
            if (self.cache_present - present) > self.fuse_recover_step:
                time_stemp = time.time()
                if (time_stemp - self._last_recover_time_stemp) * 1000 > self.fuse_recover_delay:
                    present = max(0.0, (self.cache_present - self.fuse_recover_step))
                    self._last_recover_time_stemp = time_stemp
                else:
                    present = self.cache_present
            else:
                # 直接存储present就可以了
                pass
        elif self.cache_present > 0 and present > 0:
            # 计算熔断上涨
            present = min(1.0, self.cache_present + present)
        elif self.cache_present > 0.0 and present == 0:
            # 当熔断恢复时，控制恢复流量比例
            if (self.cache_present - present) > self.fuse_recover_step:
                time_stemp = time.time()
                if (time_stemp - self._last_recover_time_stemp) * 1000 > self.fuse_recover_delay:
                    present = max(0.0, (self.cache_present - self.fuse_recover_step))
                    self._last_recover_time_stemp = time_stemp
                else:
                    present = self.cache_present
            else:
                pass

        # 存储降级比例到redis
        self.redis_client.set(self.knight_present_key, present)
        return present

    def _save2redis(self, status, delay):
        """
        存储当前状态
        :param status: 调用是否成功
        :param delay: 调用延迟
        :return: None
        """
        try:
            if not status:
                logging.debug('%s save error' % self.consul_name)
            if delay > self.tolerate_max_delay:
                logging.debug('%s save delay' % self.consul_name)
            status = 0 if status else 1
            error_delay = json.dumps([status, delay])
            self.redis_client.lpush(self.knight_error_delay_key, error_delay)
            self.redis_client.ltrim(self.knight_error_delay_key, 0, self.granularity)
        except Exception as e:
            logging.error('%s save_status error(%s)' % (self.consul_name, e))

    def __enter__(self):
        self.judge()
        self.local_param.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save_status(exc_type is None, (time.time() - self.local_param.start_time) * 1000)
        return False
