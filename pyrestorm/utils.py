import six
import urllib.request, urllib.parse, urllib.error
from urllib.parse import parse_qsl, urlparse, urlunparse


def unicode_to_ascii(item):
    '''Removes non-URL encodable characters(unicode) from the URL.
    '''
    if isinstance(item, dict):
        for key in list(item.keys()):
            if isinstance(item[key], six.string_types):
                item[key] = item[key].encode('ascii', 'ignore')

    return item


def build_url(url, **kwargs):
    '''Adds **kwargs to the query parameters and reforms the URL.
    '''
    parsed_url = list(urlparse(url))
    qs = dict(parse_qsl(parsed_url[4]))
    qs.update(unicode_to_ascii(kwargs))
    parsed_url[4] = urllib.parse.urlencode(qs)
    return urlunparse(parsed_url)
