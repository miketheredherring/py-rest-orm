import six
import urllib
from urlparse import parse_qsl, urlparse, urlunparse


def unicode_to_ascii(item):
    if isinstance(item, dict):
        for key in item.keys():
            if isinstance(item[key], six.string_types):
                item[key] = item[key].decode('unicode_escape').encode('ascii', 'ignore')

    return item


def build_url(url, **kwargs):
    parsed_url = list(urlparse(url))
    qs = dict(parse_qsl(parsed_url[4]))
    qs.update(unicode_to_ascii(kwargs))
    parsed_url[4] = urllib.urlencode(qs)
    return urlunparse(parsed_url)
