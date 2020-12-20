"""
get pagination key for reviews
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pandas import read_csv, DataFrame
from tqdm import tqdm
import numpy as np
import threading
import concurrent.futures
from configs import *


PATH = SeleniumConfig.CHROME_DRIVER_PATH
options = webdriver.ChromeOptions()
options.add_argument('headless')  # options to not open Chrome UI
desired_capabilities = options.to_capabilities()

# url_film = 'https://www.imdb.com/title/tt10048342/reviews'
BASE_URL = 'https://www.imdb.com/title/{}/reviews'


def get_pagination_keys(url, film_id=None):
    driver = webdriver.Chrome(PATH, desired_capabilities=desired_capabilities)
    driver.get(url)
    pagination_keys = set()

    try:
        div_load_more = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'load-more-data'))
        )
        load_more_btn = div_load_more.find_element_by_id('load-more-trigger')
        while load_more_btn.is_displayed():
            data_key = div_load_more.get_attribute('data-key')
            # print(data_key)
            pagination_keys.add(data_key)
            load_more_btn.click()
            time.sleep(3)
    except:
        print('ERROR--------------', url)
    finally:
        driver.quit()

    pagination_keys = list(pagination_keys)
    print('#'*50)
    print('url: {} DONE'.format(url))
    print('got {} keys'.format(len(pagination_keys)))
    if film_id is not None:
        return pagination_keys, film_id  # return film_id for multi-threading
    return pagination_keys


def run():
    film_ids = read_csv(
        os.path.join(CORE_DATA_DIR, 'id2020.csv'),
        header=0,
        dtype={'film_id': str}
    )
    film_ids = list(film_ids['film_id'].values)
    key_list_col = []
    film_id_col = []
    start, end = SeleniumConfig.START_IDX, SeleniumConfig.END_IDX
    film_ids = film_ids[start:end]
    n_threads = SeleniumConfig.N_THREADS

    print('#' * 50)
    print('N_THREADS = ', n_threads)
    if n_threads == 1:
        for film_id in tqdm(film_ids):
            keys = get_pagination_keys(BASE_URL.format(film_id))
            film_id_col.append(film_id)
            key_list_col.append(keys)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=n_threads) as executor:
            futures = []
            for film_id in film_ids:
                futures.append(executor.submit(get_pagination_keys, url=BASE_URL.format(film_id), film_id=film_id))
            for future in concurrent.futures.as_completed(futures):
                keys, film_id = future.result()
                film_id_col.append(film_id)
                key_list_col.append(keys)

    df = DataFrame({'film_id': film_id_col, 'pkeys': key_list_col})
    df.to_csv(SeleniumConfig.SAVE_TO, index=False)

