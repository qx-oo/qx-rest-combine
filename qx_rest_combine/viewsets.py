import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.urls.exceptions import Resolver404
from django.http import JsonResponse
from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .sql import _thread_locals
from .utils import MyUrlResolve, parse_url
from .request import RequestFactory
from .serializers import ResourceSerializer


logger = logging.getLogger(__name__)


def _set_query_cache():
    if not hasattr(_thread_locals, 'query_cache'):
        _thread_locals.query_cache = {}


def viewset_sqlcache(cls):
    cls.___init__ = cls.__init__

    def __init__(self, *args, **kwargs):
        _set_query_cache()
        self.___init__(*args, **kwargs)
    cls.__init__ = __init__
    return cls


PATH_NOTFOUND_RESPONSE = {
    'code': 4044,
    'msg': ['path error']
}
PATH_TYPERR_RESPONSE = {
    'code': 4040,
    'msg': ['response content type error']
}
PATH_ERROR_RESPONSE = {
    'code': 4040,
    'msg': ['can not use resource in resouce api']
}

request_callback = None
if hasattr(settings, 'COMBINE_REST_REQUEST_SET'):
    request_callback = import_string(settings.COMBINE_REST_REQUEST_SET)
deny_list = []
if hasattr(settings, 'COMBINE_REST_DENY_LIST'):
    if isinstance(settings.COMBINE_REST_DENY_LIST, list):
        deny_list = settings.COMBINE_REST_DENY_LIST


class ApiResponse(JsonResponse):
    def __init__(self, data: dict, code: int):
        results = {
            "code": code,
            "msg": ["success"],
            "data": data
        }
        super().__init__(data=results, status=code)


class ResourceViewSet(viewsets.GenericViewSet):
    """
    合并接口获取资源
    ---

    create:
        多个资源同时请求

        data最大长度10
        请求参数:
        {
            "request_list": [
                {
                    "path": "/api/category/",
                    "method": "post",
                    "data": {
                        "name": "123"
                    }
                },
                {
                    "path": "/api/category/",
                    "method": "get"
                }
            ]
        }
        返回结果列表
        {
            "response_list": [
                {
                    "id": 1,
                    "name": "123"
                },
                {}
            ]
        }
    """

    permission_classes = (
        AllowAny,
    )
    serializer_class = ResourceSerializer

    def create(self, request, *args, **kwargs):
        _set_query_cache()

        serializer = ResourceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        req_data = serializer.data

        response_list = []

        factory = RequestFactory()
        for item in req_data.get('request_list', []):

            _path, params = parse_url(item['path'])

            if _path in deny_list:
                response_list.append(PATH_NOTFOUND_RESPONSE)
                continue

            try:
                callback, callback_args, callback_kwargs = \
                    MyUrlResolve.get_callback(_path)
            except Resolver404:
                response_list.append(PATH_NOTFOUND_RESPONSE)
                continue

            if self.__class__ == callback.cls:
                response_list.append(PATH_ERROR_RESPONSE)
                continue

            method = item['method'].upper()

            # 404 error
            if not callback:
                response_list.append(PATH_NOTFOUND_RESPONSE)
                continue

            if method == "GET":
                _request = factory.get(
                    item['path'], headers=request.headers, **params)
            else:
                data = item.get('data', {})
                kwargs['data'] = json.dumps(data)
                _request = factory.generic(
                    method, item['path'], content_type='application/json',
                    **params, **kwargs)
            # set request params
            if request.META.get('HTTP_MYAUTHORIZATION'):
                _request.META['HTTP_MYAUTHORIZATION'] = \
                    request.META.get('HTTP_MYAUTHORIZATION', '')

            # set request user
            _request.__resource_user = request.user

            # request set callback
            if request_callback:
                request_callback(_request, request)

            # send request
            resp = csrf_exempt(callback)(
                _request, *callback_args, **callback_kwargs)
            try:
                ret = json.loads(resp.content)
                response_list.append(ret)
            except Exception:
                response_list.append(PATH_TYPERR_RESPONSE)
        return ApiResponse(response_list, code=200)
