"""
newscrawler.utils.py
~~~~~~~~~~~~~~~~
"""
import requests


def tag_dict_list_to_tag_list(tag_dict_list):
    tags = []

    if isinstance(tag_dict_list, list):
        for tag_dict in tag_dict_list:
            tag = tag_dict.get("term", None)
            if tag:
                tags.append(tag)
    return tags


def coerce_url(url):
    """
    Gets a url as string and returns it in the right format

    :param url: str
    :return: formatted url as string
    """
    url = url.strip()
    if url.startswith("feed://"):
        return "http://{0}".format(url[7:])
    for proto in ["http://", "https://"]:
        if url.startswith(proto):
            return url
    return "http://{0}".format(url)


def get_page(url):
    """
    Gets a url as string and returns the corresponding html object.

    :param url: str
    :return: html object
    """
    try:
        r = requests.get(url)
        return r.text
    except:
        return None
