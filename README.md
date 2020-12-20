
################################
Run Selenium in Colab to get review pagination keys
if not run in Colab -> start from step 3

# step 1:
!pip install scrapy
!pip install selenium
!apt install chromium-chromedriver

# step 2:
cd to google drive

# run only the first time
!git clone https://github.com/hustducnv/IMDBcrawler.git

# step 3:
cd project base directory (eg. IMBDcralwer)

# step 4: config in config.py file
OS_IDX = 2 (0 if UBUNTU, 1 if WINDOWNS, 2 if Colaeb)
START_IDX = ?
END_IDX = ?

# step 5: Run crawler
!python manager.py