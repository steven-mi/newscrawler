# based on https://github.com/dfm/feedfinder2
import logging

import requests

from bs4 import BeautifulSoup
from six.moves.urllib import parse as urlparse



def coerce_url(url):
    url = url.strip()
    if url.startswith("feed://"):
        return "http://{0}".format(url[7:])
    for proto in ["http://", "https://"]:
        if url.startswith(proto):
            return url
    return "http://{0}".format(url)


def get_page(url):
    try:
        r = requests.get(url)
    except Exception as e:
        logging.warn("Error while getting '{0}'".format(url))
        logging.warn("{0}".format(e))
        return None
    return r.text


def is_rss(url):
    text = get_page(url)
    if text is None:
        return False

    data = text.lower()
    if data.count("<html"):
        return False
    return data.count("<rss")+data.count("<rdf")+data.count("<feed")


def is_rss_data(data):
    data = data.lower()
    if data.count("<html"):
        return False
    return data.count("<rss")+data.count("<rdf")+data.count("<feed")


def is_rss_url(url):
    return any(map(url.lower().endswith,
                   [".rss", ".rdf", ".xml", ".atom"]))



def is_rsslike_url(url):
    return any(map(url.lower().count,
                   ["rss", "rdf", "xml", "atom", "feed"]))


def url_feed_prob(url):
    if "comments" in url:
        return -2
    if "georss" in url:
        return -1
    kw = ["atom", "rss", "rdf", ".xml", "feed"]
    for p, t in zip(range(len(kw), 0, -1), kw):
        if t in url:
            return p
    return 0


def sort_urls(feeds):
    return sorted(list(set(feeds)), key=url_feed_prob, reverse=True)


def find_rss_urls(url):
    # Format the URL properly.
    url = coerce_url(url)

    # Download the requested URL.
    text = get_page(url)
    if text is None:
        print("None")
        return []

    # Check if it is already a feed.
    if is_rss_data(text):
        return [url]

    # Get all links which might be RSS URLs.
    tree = BeautifulSoup(text, "html.parser")
    links = []
    for link in tree.find_all("link"):
        if link.get("type") in ["application/rss+xml",
                                "text/xml",
                                "application/atom+xml",
                                "application/x.atom+xml",
                                "application/x-atom+xml"]:
            url = urlparse.urljoin(url, link.get("href", ""))
            links.append(url)

            
    # Check the detected links.
    urls = list(filter(is_rss, links))
    if len(urls):
        return sort_urls(urls)

    # Look for <a> tags.
    local, remote = [], []
    for a in tree.find_all("a"):
        href = a.get("href", None)
        if href is None:
            continue
        if "://" not in href and is_rss_url(href):
            local.append(href)
        if is_rsslike_url(href):
            remote.append(href)

    # Check the local URLs.
    local = [urlparse.urljoin(url, l) for l in local]
    urls += list(filter(is_rss, local))
    logging.info("Found {0} local <a> links to feeds.".format(len(urls)))
    if len(urls):
        return sort_urls(urls)

    # Check the remote URLs.
    remote = [urlparse.urljoin(url, l) for l in remote]
    urls += list(filter(is_rss, remote))
    logging.info("Found {0} remote <a> links to feeds.".format(len(urls)))
    if len(urls):
        return sort_urls(urls)

    # Guessing potential URLs.
    fns = ["atom.xml", "index.atom", "index.rdf", "rss.xml", "index.xml",
           "index.rss", "feeds/latest.rss", "rssfeed.rdf"]
    urls += list(filter(is_rss, [urlparse.urljoin(url, f)
                                         for f in fns]))
    return sort_urls(urls)

