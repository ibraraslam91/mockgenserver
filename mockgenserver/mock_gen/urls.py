from rest_framework_extensions.routers import ExtendedSimpleRouter

from mockgenserver.mock_gen.api.views import ProjectViewSet, ScreenViewSet, LayerViewSet

app_name = "mock_gen"

router = ExtendedSimpleRouter()
router.register(r"projects", ProjectViewSet, basename="project").register(
    r"screens", ScreenViewSet, basename="screen", parents_query_lookups=["project"]
)
router.register(r"layers", LayerViewSet, basename="layer")


urlpatterns = router.urls
