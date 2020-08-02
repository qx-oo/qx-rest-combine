from django.apps import AppConfig


class QxRestCombineConfig(AppConfig):
    name = 'qx_rest_combine'

    def ready(self):
        from django.conf import settings
        from django.utils.module_loading import import_string
        from django.urls.resolvers import (
            URLPattern, URLResolver,
        )
        from .utils import MyUrlResolve
        for cls in import_string(
                '{}.urlpatterns'.format(settings.ROOT_URLCONF)):
            if isinstance(cls, URLResolver) or isinstance(cls, URLPattern):
                MyUrlResolve._urls.append(cls)
