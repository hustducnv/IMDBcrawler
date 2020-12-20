import os


BASE_DIR = os.path.dirname(__file__)
CORE_DATA_DIR = os.path.join(BASE_DIR, 'data')


class ReviewSpiderConfig:
    KEYS_PATH = os.path.join(CORE_DATA_DIR, 'review_pagination_keys', 'pkeys_feature_2020.csv')
    MAX_IDX = 20
    START_IDX = 0
    END_IDX = 3

class SeleniumConfig:
    OS = 'WINDOWN'  # 'UBUNTU' or 'WINDOWN'
    if OS == 'WINDOWN':
        driver = 'chromedriver.exe'
    elif OS == 'UBUNTU':
        driver = 'chromedriver'
    else:
        raise Exception('OS wrong! See configs.py')
    N_THREADS = 4
    CHROME_DRIVER_PATH = os.path.join(CORE_DATA_DIR, 'Chrome', driver)
    MAX_IDX = 10520
    START_IDX = 0
    END_IDX = 10  # EXCLUSIVE
    SAVE_TO = os.path.join(CORE_DATA_DIR, 'review_pagination_keys', 'pkeys_{0}_{1}.csv'.format(START_IDX, END_IDX))
