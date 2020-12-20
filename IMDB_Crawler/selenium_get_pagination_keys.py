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
from configs import *


PATH = SeleniumConfig.CHROME_DRIVER_PATH
options = webdriver.ChromeOptions()
options.add_argument('headless')  # options to not open Chrome UI
desired_capabilities = options.to_capabilities()

# url_film = 'https://www.imdb.com/title/tt10048342/reviews'
BASE_URL = 'https://www.imdb.com/title/{}/reviews'


def get_pagination_keys(url, multithreading_args=None):
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
    if multithreading_args is not None:
        film_id, film_id_col, key_list_col, lock = multithreading_args
        # print(film_id)
        lock.acquire()
        film_id_col.append(film_id)
        key_list_col.append(pagination_keys)
        lock.release()
    return pagination_keys


def multithreadings_get_pkeys(film_ids, film_id_col, key_list_col):
    threads = []
    for film_id in film_ids:
        lock = threading.Lock()
        _thread = threading.Thread(target=get_pagination_keys, args=(BASE_URL.format(film_id), (film_id, film_id_col, key_list_col, lock)))
        _thread.start()
        threads.append(_thread)

    for _thread in threads:
        _thread.join()


# if __name__ == '__main__':
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
    n_threads = SeleniumConfig.N_THREADS

    print('#' * 50)
    print('N_THREADS = ', n_threads)
    if n_threads == 1:
        for film_id in tqdm(film_ids[start:end]):
            keys = get_pagination_keys(BASE_URL.format(film_id))
            film_id_col.append(film_id)
            key_list_col.append(keys)
    else:
        n_ids = len(film_ids[start:end])
        for i in tqdm(range(int(np.ceil(n_ids / n_threads)))):
            start_idx = i * n_threads
            end_idx = start_idx + n_threads
            if end_idx > n_ids:
                end_idx = n_ids
            multithreadings_get_pkeys(film_ids[start_idx:end_idx], film_id_col, key_list_col)
    # print(film_id_col)
    df = DataFrame({'film_id': film_id_col, 'keys': key_list_col})
    df.to_csv(SeleniumConfig.SAVE_TO, index=False)

