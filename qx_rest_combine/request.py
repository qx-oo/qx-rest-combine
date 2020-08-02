from io import BytesIO
from urllib.parse import unquote_to_bytes, urlparse
from rest_framework.parsers import JSONParser
from django.http import SimpleCookie
from django.core.handlers.wsgi import WSGIRequest
from django.utils.encoding import force_bytes
from django.utils.http import urlencode
from django.conf import settings


class FakePayload:

    def __init__(self, content=None):
        self.__content = BytesIO()
        self.__len = 0
        self.read_started = False
        if content is not None:
            self.write(content)

    def __len__(self):
        return self.__len

    def read(self, num_bytes=None):
        if not self.read_started:
            self.__content.seek(0)
            self.read_started = True
        if num_bytes is None:
            num_bytes = self.__len or 0
        assert self.__len >= num_bytes, "Cannot read the available bytes."
        content = self.__content.read(num_bytes)
        self.__len -= num_bytes
        return content

    def write(self, content):
        if self.read_started:
            raise ValueError("Unable to write a payload after he's been read")
        content = force_bytes(content)
        self.__content.write(content)
        self.__len += len(content)


class RequestFactory:

    def __init__(self, *, json_encoder=JSONParser, **defaults):
        self.json_encoder = json_encoder
        self.defaults = defaults
        self.cookies = SimpleCookie()
        self.errors = BytesIO()

    def _base_environ(self, **request):
        """
        """
        return {
            'HTTP_COOKIE': '; '.join(sorted(
                '%s=%s' % (morsel.key, morsel.coded_value)
                for morsel in self.cookies.values()
            )),
            'PATH_INFO': '/',
            'REMOTE_ADDR': '127.0.0.1',
            'REQUEST_METHOD': 'GET',
            'SCRIPT_NAME': '',
            'SERVER_NAME': '127.0.0.1',
            'SERVER_PORT': '80',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': FakePayload(b''),
            'wsgi.errors': self.errors,
            'wsgi.multiprocess': True,
            'wsgi.multithread': False,
            'wsgi.run_once': False,
            **self.defaults,
            **request,
        }

    def request(self, **request):
        "Construct a generic request object."
        return WSGIRequest(self._base_environ(**request))

    def _get_path(self, parsed):
        path = parsed.path
        if parsed.params:
            path += ";" + parsed.params
        path = unquote_to_bytes(path)
        return path.decode('iso-8859-1')

    def get(self, path, data=None, secure=False, **extra):
        data = {} if data is None else data
        return self.generic('GET', path, secure=secure, **{
            'QUERY_STRING': urlencode(data, doseq=True),
            **extra,
        })

    def generic(self, method, path, data='',
                content_type='application/octet-stream', secure=False,
                **extra):
        """Construct an arbitrary HTTP request."""
        parsed = urlparse(str(path))  # path can be lazy
        data = force_bytes(data, settings.DEFAULT_CHARSET)
        r = {
            'PATH_INFO': self._get_path(parsed),
            'REQUEST_METHOD': method,
            'SERVER_PORT': '443' if secure else '80',
            'wsgi.url_scheme': 'https' if secure else 'http',
        }
        if data:
            r.update({
                'CONTENT_LENGTH': str(len(data)),
                'CONTENT_TYPE': content_type,
                'wsgi.input': FakePayload(data),
            })
        r.update(extra)
        if not r.get('QUERY_STRING'):
            # WSGI requires latin-1 encoded strings. See get_path_info().
            query_string = parsed[4].encode().decode('iso-8859-1')
            r['QUERY_STRING'] = query_string
        return self.request(**r)
