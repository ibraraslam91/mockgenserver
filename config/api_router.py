from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from mockgenserver.users.api.views import UserViewSet, GroupViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet, basename="users")
router.register("groups", GroupViewSet, basename="groups")


app_name = "api"
urlpatterns = router.urls
