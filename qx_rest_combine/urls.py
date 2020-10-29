from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets

router = DefaultRouter()
router.register('upload-img', viewsets.UploadImageViewset,
                basename="upload_image")

urlpatterns = [
    path('', include(router.urls)),
]
