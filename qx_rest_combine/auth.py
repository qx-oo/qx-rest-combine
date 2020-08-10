from rest_framework.authentication import (
    BaseAuthentication,
)


class ResourceAuthentication(BaseAuthentication):

    def authenticate(self, request):

        user = getattr(request, '__resource_user', None)
        token = self.get_token_by_request(request)

        if not user or not user.is_active:
            return None

        return (user, token)

    def get_token_by_request(self, request):
        return None
