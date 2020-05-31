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
        return find_rss_urls(self.url)[0]

    def _extract_article_text_from_html(self, html):
        article = Article('')
        article.set_html(html)
        article.parse()
        return article.text
    
    def _extract_article_information_from_html(self, html):
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
        article_dict = self._extract_article_information()
        return pd.DataFrame.from_dict(article_dict)
    

    def _extract_article_information(self):
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
