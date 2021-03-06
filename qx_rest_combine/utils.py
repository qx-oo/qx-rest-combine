import urllib
from django.urls.exceptions import Resolver404
from rest_framework.routers import APIRootView


class MyUrlResolve():

    _urls = []

    @classmethod
    def get_callback(cls, url) -> (object, dict):
        """
        get view by url
        """
        for pattern in cls._urls:
            try:
                resolver_match = pattern.resolve(url)
                if not resolver_match:
                    pass
                elif resolver_match[0].cls == APIRootView:
                    pass
                else:
                    return resolver_match
            except Resolver404:
                pass
        raise Resolver404()


def parse_url(url):
    parser = urllib.parse.urlparse(url)
    _path = parser.path.lstrip('/')
    params = urllib.parse.parse_qsl(parser.query)
    return _path, {
        key: val
        for key, val in params
    }
