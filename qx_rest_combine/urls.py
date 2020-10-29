from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets

router = DefaultRouter()
router.register('resource', viewsets.ResourceViewSet, basename="resource")

urlpatterns = [
    path('', include(router.urls)),
]
