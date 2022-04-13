# qx-combine-rest

my django project combine rest api apps

### Install:

    pip install -e git://github.com/qx-oo/qx-rest-combine.git@master#egg=qx-rest-combine

### Usage:

settings.py:

    INSTALLED_APPS = [
        ...
        'qx_rest_combine',
    ]

    COMBINE_REST_REQUEST_SET = "qx_test.utils.request_set"
    COMBINE_REST_DENY_LIST = ["/api/test"]

urls.py:

    urlpatterns = [
        ...
        path('api/resource/', include('qx_rest_combine.urls')),
        ...
    ]

View Class Sql Cache:

    from qx_rest_combine.viewsets import viewset_sqlcache

    @viewset_sqlcache
    class TestView:
        pass

### Tests:

    python manage.py migrate

    python manage.py runserver

    python qx_test/test_request.py