import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from ..config import input_url, extension, scrap_tag, scrap_class


class ReviewScrapper:

    def __init__(self, company: str, page_max=100):
        url_to_scrap = input_url + company + extension
        self.url = url_to_scrap
        self.page_max = page_max

    def scrap_data(self):
        titles = []
        ratings = []
        reviews = []
        dates = []
        replies = []
        reply_dates = []
        for index in range(self.number_of_pages):
            url = self.url + "?page=" + str(index + 1)
            soup = self._get_soup(url)
            _titles, _ratings, _reviews, _dates, _replies, _reply_dates = self._get_content(soup)
            titles += _titles
            ratings += _ratings
            reviews += _reviews
            dates += _dates
            replies += _replies
            reply_dates += _reply_dates
        reviews_dict = {'titles': titles, 'ratings': ratings, 'reviews': reviews,
                        'dates': dates, 'replies': replies, 'reply_dates': reply_dates}
        reviews_df = pd.DataFrame.from_dict(reviews_dict)
        return reviews_df

    @staticmethod
    def _get_soup(url: str) -> BeautifulSoup:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup

    @staticmethod
    def _get_content(soup: BeautifulSoup):

        def _get_review_title(_card: BeautifulSoup):
            paragraphs = _card.findAll(scrap_tag['title'], class_=scrap_class['title'])
            contents = paragraphs[0].contents if paragraphs else []
            review_title = ''
            for line in contents:
                review_title += str(line) if str(line) != '<br/>' else '\n'
            return review_title

        def _get_review_rating(_card: BeautifulSoup):
            paragraphs = _card.findAll(scrap_tag['rating'], class_=scrap_class['rating'])
            paragraph = paragraphs[0] if paragraphs and 0 < len(paragraphs) else '-1'
            rating = paragraph.get('data-service-review-rating')
            return rating

        def _get_review(_card: BeautifulSoup):
            paragraphs = _card.findAll(scrap_tag['review'], class_=scrap_class['review'])
            contents = paragraphs[0].contents if paragraphs else []
            review = ''
            for line in contents:
                review += str(line) if str(line) != '<br/>' else '\n'
            return review

        def _get_review_date(_card: BeautifulSoup):
            paragraphs = _card.findAll('time')
            date = paragraphs[0].get('datetime') if 0 < len(paragraphs) else ''
            return date

        """
        def _get_review_date(_card: BeautifulSoup):
            paragraphs = _card.findAll(scrap_tag['date'], class_=scrap_class['date'])
            contents = paragraphs[0].contents if paragraphs else []
            review_date = contents[-1] if 0 < len(contents) else ''
            return review_date
        """

        def _get_reply(_card: BeautifulSoup):
            paragraphs = _card.findAll(scrap_tag['reply'], class_=scrap_class['reply'])
            reply = ''
            if 1 < len(paragraphs):
                contents = paragraphs[2].contents if paragraphs else []
                if 0 < len(contents):
                    reply = contents[0]
            return reply

        def _get_reply_date(_card: BeautifulSoup):
            paragraphs = _card.findAll('time')
            reply_date = paragraphs[1].get('datetime') if 1 < len(paragraphs) else ''
            return reply_date

        titles, ratings, reviews, dates, replies, reply_dates = [], [], [], [], [], []
        cards = soup.findAll(scrap_tag['card'], class_=scrap_class['card'])
        if cards:
            for card in cards:
                titles.append(_get_review_title(card))
                ratings.append(_get_review_rating(card))
                reviews.append(_get_review(card))
                dates.append(_get_review_date(card))
                replies.append(_get_reply(card))
                reply_dates.append(_get_reply_date(card))
        content = titles, ratings, reviews, dates, replies, reply_dates
        return content

    @property
    def number_of_pages(self):
        num_of_pages = self.page_max
        if 1 < self.page_max:
            soup = self._get_soup(self.url)
            content_for_pages = soup.findAll("script", id="__NEXT_DATA__")[0].contents[0]
            content_for_pages_json = json.loads(content_for_pages)
            num_of_pages: int = \
                content_for_pages_json.get('props').get('pageProps').get('filters').get('pagination').get('totalPages')
            num_of_pages = min(num_of_pages, self.page_max)
        return num_of_pages
