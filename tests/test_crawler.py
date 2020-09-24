"""
tests.test_crawler.py
~~~~~~~~~~~~~~~~~~~~

Test suite for the crawler.py
"""
import pandas as pd
import pytest

from newscrawler import Crawler


class TestCrawler:

    def test_faz(self):
        crawler = Crawler("faz.net")
        article_df = crawler.get_article_information_as_dataframe()
        assert isinstance(article_df, pd.DataFrame)

    def test_sueddeutsche(self):
        crawler = Crawler(["http://sueddeutsche.de", "bild.de"])
        article_df = crawler.get_article_information_as_dataframe()
        assert isinstance(article_df, pd.DataFrame)
