import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .utils import MyUrlResolve, parse_url
from .request import RequestFactory
from .serializers import ResourceSerializer


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
        serializer = ResourceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        req_data = serializer.data

        response_list = []

        factory = RequestFactory()
        for item in req_data.get('request_list', []):

            _path, params = parse_url(item['path'])

            callback, callback_args, callback_kwargs = \
                MyUrlResolve.get_callback(_path)

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
                    '', headers=request.headers, **params)
            else:
                data = item.get('data', {})
                kwargs['data'] = json.dumps(data)
                _request = factory.generic(
                    method, '', content_type='application/json',
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
            if isinstance(resp.data, (dict, list)):
                response_list.append(resp.data)
            else:
                response_list.append(PATH_TYPERR_RESPONSE)
        return ApiResponse(response_list, code=200)
