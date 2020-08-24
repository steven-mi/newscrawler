"""
newscrawler.crawler.py
~~~~~~~~~~~~~~~~

This module contains the Crawler class, the main logic of our library. It handles the RSS feed extraction,
and aswell the frameworks for information extraction.
"""
import logging

import feedparser

import pandas as pd

from newspaper import Article

from newscrawler.utils import get_page
from newscrawler.utils import find_rss_urls


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

    def __init__(self, url):
        self.url = url
        self.rss_feed = self.get_rss_feed()
        

    def get_rss_feed(self):
        """
        Uses the attribute url as input and returns the rss feed back

        :return: returns the rss_feed back
        """
        return find_rss_urls(self.url)[0]

    def _extract_article_text_from_html(self, html):
        """
        This methods gets a website as HTML and returns the newspaper article back

        :param html: a HTML object from package requests
        :return: article as string
        """
        article = Article('')
        article.set_html(html)
        article.parse()
        return article.text
    
    def _extract_article_information_from_html(self, html):
        """
        This methods gets a website as HTML, extracts text, summary, author, publish date, tags and title,
        stores these informations in a dictionary and returns the dictionary

        :param html: a HTML object from package requests
        :return: Dict Object with keys: text, summary, author, published, tags, title
        """
        article = Article('')
        article.set_html(html)
        article.parse()
        
        article_information = {}
        article_information["text"] = article.text
        article_information["summary"] = article.summary
        article_information["author"] = str(article.authors).strip('[]')
        article_information["published"] = article.publish_date
        article_information["tags"] = article.tags
        article_information["title"] = article.title
        return article_information
     
    def get_article_information_as_dataframe(self):
        """
        This method extracts the article information and returns it as a pandas Dataframe

        :return: pandas.Dataframe with all article informations
        """
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
        NewsFeed = feedparser.parse(self.rss_feed)
        feed = NewsFeed.entries

        article_information = {}
        for item in feed:
            for key in self.NEWSKEYS:
                value = item.get(key, '')
                if not value and item.get("link", ""):
                    html = get_page(item["link"])
                    article = self._extract_article_information_from_html(html)
                    value = article[key]
                    
                article_information[key] = article_information.get(key, []) + [value]
        return article_information
