from rest_framework import serializers, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from qx_rest_combine.viewsets import viewset_sqlcache
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


@viewset_sqlcache
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

    @action(methods=['get'], url_path='test', detail=False)
    def list_test(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        # again
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data.extend(serializer.data)
        return Response(data)
