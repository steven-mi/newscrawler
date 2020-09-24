"""
newscrawler.crawler.py
~~~~~~~~~~~~~~~~

This module contains the Crawler class, the main logic of our library. It handles the RSS feed extraction,
and aswell the frameworks for information extraction.
"""
import logging

import feedparser

import pandas as pd

from time import mktime

from newspaper import Article
from newsplease import NewsPlease

from newscrawler.extract_rss import get_page, extract_rss
from newscrawler.utils import tag_dict_list_to_tag_list, coerce_url


def extract_article_text_from_html(html):
    """
    This methods gets a website the HTML as string and extracts the text of
    the article

    :param html: a HTML object from package requests
    :return: the article text as string
    """
    # run with newspaper
    article_newspaper = Article('')
    article_newspaper.set_html(html)
    article_newspaper.parse()
    newspaper_text = article_newspaper.text
    # run with newsplease
    article_newsplease = NewsPlease.from_html(html)
    newsplease_text = article_newsplease.cleaned_text
    # run with goose
    #from goose3 import Goose
    #extractor = Goose()
    #article = extractor.extract(raw_html=html)
    #text = article.cleaned_text
    if len(newspaper_text.split(" ")) > len(newsplease_text.split(" ")):
        return newspaper_text
    else:
        newsplease_text


class Crawler:
    """
    The Crawler object contains all the methods for extracting information from a given URL

    Args:
        url (str): URL of a website as string

    Attributes:
        url (str): This is where we the website url
        rss_feed (str): This is where we the rss feed url
    """

    NEWSKEYS = ['title',
                'summary',
                'author',
                'published',
                'link',
                'tags',
                'text']

    def __init__(self, url) -> str:
        self.url = coerce_url(url)
        self.rss_feed = extract_rss(self.url)[0]

    def get_article_information_as_dataframe(self):
        """
        This method extracts the article information and returns it as a pandas Dataframe

        :return: pandas.Dataframe with all article informations
        """
        try:
            article_dict = self._extract_article_information()
            return pd.DataFrame.from_dict(article_dict)
        except:
            import ssl
            ssl._create_default_https_context = ssl._create_unverified_context
            article_dict = self._extract_article_information()
            return pd.DataFrame.from_dict(article_dict)

    def _extract_article_information(self):
        """
        This method extracts article informations from the current RSS feed. The
        informations are storing in a dictionary with keys:
            - text
            - summary
            - author
            - published
            - tags
            - title

        :return: all articles of the rss feed as dictionary
        """
        logging.info("parsing: {}".format(self.rss_feed))
        parsed_feed = feedparser.parse(self.rss_feed)
        feed = parsed_feed.entries

        article_information = {}
        for item in feed:
            article_html = get_page(item["link"])
            html_article_information = extract_article_text_from_html(article_html)

            for key in self.NEWSKEYS:
                value = item.get(key, None)

                if key == "published":
                    value = mktime(item["published_parsed"])
                elif key == " tags":
                    value = tag_dict_list_to_tag_list(item["published_parsed"])
                    value = ', '.join(value)
                elif key == "text":
                    value = html_article_information[key]
                article_information[key] = article_information.get(key, []) + [value]
        return article_information
