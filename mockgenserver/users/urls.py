from django.urls import path

from mockgenserver.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
)
from mockgenserver.users.api.views import LoginAPIView

app_name = "users"
urlpatterns = [
    path("login/", view=LoginAPIView.as_view(), name="login-api"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
