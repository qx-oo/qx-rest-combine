# qx-combine-rest

my django project combine rest api apps

### Install:

    pip install -e git://github.com/qx-oo/qx-combine-rest.git@master#egg=qx-combine-rest

### Usage:

settings.py:

    INSTALLED_APPS = [
        ...
        # Make sure to put it last
        'qx_rest_combine',
    ]

    COMBINE_REST_REQUEST_SET = "qx_test.utils.request_set"

urls.py:

    from qx_rest_combine.viewsets import ResourceViewSet

    router = DefaultRouter()

    router.register('resource', ResourceViewSet, basename="resource")

    urlpatterns = [
        ...
        path('api/', include(router.urls)),
    ]

### Tests:

    python manage.py migrate

    python manage.py runserver

    python qx_test/test_request.py