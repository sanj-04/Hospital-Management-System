from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from knox.auth import TokenAuthentication


class KnoxLoginAPI(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(KnoxLoginAPI, self).post(request, format=None)


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class RFLoginAPI(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        from knox.models import AuthToken

        knoxToken = AuthToken.objects.create(user)[1]
        return Response(
            {
                "token": token.key,
                "created": created,
                "knoxToken": knoxToken,
            }
        )


class HomeView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        content = {"message": "Hello, World!"}
        return Response(content)
