from IMDB_Crawler.selenium_get_pagination_keys import run
from time import time

start = time()
run()
print('execution time: ', time() - start)