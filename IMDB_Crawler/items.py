# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import re


def clean_input(value):
    value = value.strip()
    if value != '':
        return value
    return None


def clean_tilte(title):
    title = title.replace('\xa0', '').strip()
    if title != '':
        return title


def clean_rating_count(rating_count):
    return rating_count.replace(',', '')


def clean_popularity(popularity):
    popularity = re.sub(r'\(|\)', '', popularity).strip()
    if popularity != '':
        return popularity


def clean_n_reviews(reviews):
    return re.sub(r',|user| ', '', reviews)


class MovieItem(Item):
    imdb_url = Field()

    # Details
    title = Field(input_processor=MapCompose(clean_tilte), output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    imdb_rating = Field(output_processor=TakeFirst())
    rating_count = Field(input_processor=MapCompose(clean_rating_count), output_processor=TakeFirst())
    release_date = Field(input_processor=MapCompose(clean_input), output_processor=TakeFirst())
    directors = Field(output_processor=Join(', '))
    writers = Field(output_processor=Join(', '))
    countries = Field(output_processor=Join(', '))
    languages = Field(output_processor=Join(', '))
    known_as = Field(input_processor=MapCompose(clean_input), output_processor=TakeFirst())
    filming_locations = Field(output_processor=Join(', '))
    metascore = Field(output_processor=TakeFirst())
    reviews = Field(input_processor=MapCompose(clean_n_reviews), output_processor=TakeFirst())
    popularity = Field(input_processor=MapCompose(clean_popularity), output_processor=TakeFirst())
    main_cast_members = Field(input_processor=MapCompose(clean_input), output_processor=Join(', '))
    story_line = Field(input_processor=MapCompose(clean_input), output_processor=TakeFirst())
    plot_keywords = Field(output_processor=Join(', '))
    genres = Field(output_processor=Join(', '))
    mpaa = Field(input_processor=MapCompose(clean_input), output_processor=TakeFirst())  # motion picture rating

    # Box Office
    budget = Field(input_processor=MapCompose(clean_input), output_processor=TakeFirst())
    opening_weekend_USA = Field(input_processor=MapCompose(clean_input), output_processor=TakeFirst())
    cumulative_world_wide_gross = Field(input_processor=MapCompose(clean_input), output_processor=TakeFirst())

    # Company credits
    production_co = Field(input_processor=MapCompose(clean_input), output_processor=Join(', '))

    # Technical Specs
    runtime = Field(output_processor=TakeFirst())
    aspect_ratio = Field(input_processor=MapCompose(clean_input), output_processor=TakeFirst())


def get_id(text):
    # '/user/ur59804772/', '/review/rw6208113/'
    try:
        id = text.split('/')[-2]
    except:
        return None
    return id


class ReviewItem(Item):
    user_id = Field(input_processor=MapCompose(get_id), output_processor=TakeFirst())
    comment_id = Field(input_processor=MapCompose(get_id), output_processor=TakeFirst())
    date = Field(output_processor=TakeFirst())
    star_rating = Field(output_processor=TakeFirst())
    title = Field(input_processor=MapCompose(clean_input), output_processor=TakeFirst())
    content = Field(output_processor=TakeFirst())

