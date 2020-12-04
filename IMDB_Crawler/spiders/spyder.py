from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from IMDB_Crawler.items import MovieItem



class IMDBspider(Spider):
    name = 'IMDBspider'
    allowed_domains = ['imdb.com']

    def start_requests(self):
        start_url = 'https://www.imdb.com/search/title/?title_type=feature&'
        yield Request(url=start_url, callback=self.parse_film_links)

        # test
        # start_url = 'https://www.imdb.com/title/tt0290677/?ref_=adv_li_tt'
        # start_url = 'https://www.imdb.com/title/tt4154796/?ref_=nv_sr_srsg_0'
        # yield Request(url=start_url, callback=self.parse_film_features)

    def parse_film_links(self, response):
        film_links = response.xpath('//*[@id="main"]/div/div[3]/div/div/div[3]/h3/a')
        yield from response.follow_all(film_links, self.parse_film_features)

        next_page = response.xpath('//*[@id="main"]/div/div[4]/a')
        yield from response.follow_all(next_page, self.parse_film_links)

    def parse_film_features(self, response):
        l = ItemLoader(item=MovieItem(), response=response)

        l.add_value('url', response.url)
        l.add_xpath('title', '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/h1/text()[1]')
        l.add_xpath('imdb_rating', '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()')
        l.add_xpath('rating_count', '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/a/span/text()')
        l.add_xpath('release_date', '//*[@id="titleDetails"]/div[h4/text()="Release Date:"]/text()[2]')
        l.add_css('directors', '.plot_summary > div:nth-child(2) > a::text')
        l.add_css('writers', '.plot_summary > div:nth-child(3) > a::text')
        l.add_xpath('countries', '//*[@id="titleDetails"]/div[contains(h4/text(), "Country")]/a/text()')
        l.add_xpath('languages', '//*[@id="titleDetails"]/div[contains(h4/text(), "Language")]/a/text()')
        l.add_xpath('known_as', '//*[@id="titleDetails"]/div[contains(h4/text(), "Known")]/text()[2]')
        l.add_xpath('filming_locations', '//*[@id="titleDetails"]/div[contains(h4/text(), "Locations")]/a/text()')
        l.add_xpath('metascore', '//*[@id="title-overview-widget"]/div[2]/div[@class="titleReviewBar "]/div[1]/a/div/span/text()')
        l.add_xpath('popularity', '//*[@id="title-overview-widget"]/div[2]/div[@class="titleReviewBar "]/div[5]/div[2]/div[2]/span/text()')
        l.add_xpath('reviews', '//*[@id="title-overview-widget"]/div[2]/div[@class="titleReviewBar "]/div[3]/div[2]/span/a[1]/text()')
        l.add_xpath('main_cast_members', '//*[@id="titleCast"]/table/tr/td[2]/a/text()')
        l.add_xpath('story_line', '//*[@id="titleStoryLine"]/div[1]/p/span/text()')
        l.add_xpath('plot_keywords', '//*[@id="titleStoryLine"]/div[contains(h4/text(), "Keywords")]/a/span/text()')
        l.add_xpath('genres', '//*[@id="titleStoryLine"]/div[contains(h4/text(), "Genres")]/a/text()')
        l.add_xpath('mpaa', '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/div/text()[1]')
        l.add_xpath('budget', '//*[@id="titleDetails"]/div[contains(h4/text(), "Budget")]/text()[2]')
        l.add_xpath('opening_weekend_USA', '//*[@id="titleDetails"]/div[contains(h4/text(), "Weekend")]/text()[2]')
        l.add_xpath('cumulative_world_wide_gross', '//*[@id="titleDetails"]/div[contains(h4/text(), "Worldwide")]/text()[2]')
        l.add_xpath('production_co', '//*[@id="titleDetails"]/div[contains(h4/text(), "Production")]/a/text()')
        l.add_xpath('runtime', '//*[@id="titleDetails"]/div[contains(h4/text(), "Runtime")]/time/text()')
        l.add_xpath('aspect_ratio', '//*[@id="titleDetails"]/div[contains(h4/text(), "Ratio")]/text()[2]')

        yield l.load_item()



