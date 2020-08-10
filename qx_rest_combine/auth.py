from rest_framework.authentication import (
    BaseAuthentication,
)


class ResourceAuthentication(BaseAuthentication):

    def authenticate(self, request):

        user = getattr(request, '__resource_user', None)
        if not user or not user.is_active:
            return None

        token = self.get_token_by_request(request)
        return (user, token)

    def get_token_by_request(self, request):
        return None
