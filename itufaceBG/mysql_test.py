from django.db import connection

import traceback

import logging

logging.basicConfig(level=logging.INFO,)




if __name__ == '__main__':

    try:
        1/0
    except TypeError as e:
        logging.error(e)
