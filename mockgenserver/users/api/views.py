from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from mockgenserver.users.api.serializers import LoginRequestSerializer, UserSerializer

User = get_user_model()


class UserViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        company_id = self.request.user.company_id
        return User.objects.filter(company_id=company_id)

    def create(self, request, *args, **kwargs):
        request_data = request.data
        company = self.request.user.company_id
        request_data["company"] = company
        return super().create(request)


class LoginAPIView(APIView):

    permission_classes = [
        AllowAny,
    ]

    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def post(self, request):
        request_serializer = LoginRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        email = request_serializer.validated_data["email"]
        password = request_serializer.validated_data["password"]
        user = authenticate(email=email.lower(), password=password)
        if not user:
            return Response(
                data={"message": "Incorrect email or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        tokens = self.get_tokens_for_user(user)
        response_data = {
            "user": UserSerializer(user).data,
            "roles": user.groups.values_list("name", flat=True),
            "tokens": tokens,
        }
        response = Response(data=response_data, status=status.HTTP_200_OK)
        return response
