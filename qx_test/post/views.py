from rest_framework import serializers, viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import Post, Category

# Create your views here.


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'name', 'user', 'category',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name',)


class PostViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,):

    permission_classes = (
        AllowAny,
    )
    serializer_class = PostSerializer

    queryset = Post.objects.all()


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,):

    permission_classes = (
        AllowAny,
    )
    serializer_class = CategorySerializer

    queryset = Category.objects.all()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
