import logging
import traceback


if __name__ == '__main__':


    try:

        a=1/0

    except Exception as e:
        logging.exception("s")
