from django.apps import AppConfig


class MockGenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "mockgenserver.mock_gen"
