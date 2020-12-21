import os

BASE_DIR = os.path.dirname(__file__)
CORE_DATA_DIR = os.path.join(BASE_DIR, 'data')


class ReviewSpiderConfig:
    KEYS_PATH = os.path.join(CORE_DATA_DIR, 'review_pagination_keys', 'pkeys_feature_2020.csv')
    MAX_IDX = 20
    START_IDX = 0
    END_IDX = 3


class SeleniumConfig:
    OS_LIST = ['UBUNTU', 'WINDOWNS', 'COLAB']
    OS_IDX = 1
    if OS_IDX == 1:
        driver = 'chromedriver.exe'
        CHROME_DRIVER_PATH = os.path.join(CORE_DATA_DIR, 'Chrome', driver)
    elif OS_IDX == 0:
        driver = 'chromedriver'
        CHROME_DRIVER_PATH = os.path.join(CORE_DATA_DIR, 'Chrome', driver)
    elif OS_IDX == 2:
        CHROME_DRIVER_PATH = '/usr/lib/chromium-browser/chromedriver'
    else:
        raise Exception('OS_IDX wrong! See configs.py')

    N_THREADS = 5

    MAX_IDX = 8701
    START_IDX = 0
    END_IDX = 7  # EXCLUSIVE
    SAVE_TO = os.path.join(CORE_DATA_DIR, 'review_pagination_keys', 'pkeys_{0}_{1}.csv'.format(START_IDX, END_IDX))
