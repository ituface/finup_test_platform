import time
import asyncio

now = lambda : time.time()

async def do_some_work(x):
    print('Waiting: ', x)
    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)

def callback(future):
    print('Callback: ', future.result())

def main():
    start = now()

    coroutine = do_some_work(2)
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(coroutine)
    task.add_done_callback(callback)
    return 'sunccess'
    loop.run_until_complete(task)

    print('TIME: ', now() - start)





if __name__ == '__main__':
    print(main())


