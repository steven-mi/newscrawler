"""
tests.test_extract_rss.py
~~~~~~~~~~~~~~~~~~~~

Test suite for the extract_rss.py module

"""

import pytest

from newscrawler.extract_rss import extract_rss
from newscrawler.utils import coerce_url


def test_zeit():
    url = coerce_url("zeit.de")
    assert isinstance(extract_rss(url), list)

def test_spiegel():
    url = coerce_url("spiegel.de")
    assert isinstance(extract_rss(url), list)
