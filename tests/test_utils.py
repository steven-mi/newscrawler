"""
tests.test_utils.py
~~~~~~~~~~~~~~~~~~~~

Test suite for the utils.py module
"""

import pytest

from newscrawler.utils import coerce_url, tag_dict_list_to_tag_list


def test_coerce_url():
    url = "zeit.de"
    cleaned = coerce_url(url)
    assert cleaned == "https://zeit.de"

def test_tag_dict_list_to_tag_list():
    tag_dict_list = [{'term': 'News', 'scheme': None, 'label': None}, {'term': 'News', 'scheme': None, 'label': None}]
    tag_list = tag_dict_list_to_tag_list(tag_dict_list)
    assert "News" in tag_list
    assert len(tag_list) == 2