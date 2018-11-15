import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_DIR)

DEBUG=False
USER_CODE = ''
DB_PATH = os.path.join(BASE_DIR, 'db', 'weibo.db')

INTERVAL = 2