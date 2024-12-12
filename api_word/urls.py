from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WordsViewSet

app_name = 'api_word'

router = DefaultRouter()
router.register(r'word', WordsViewSet, basename='word')

urlpatterns = [
    path('',include(router.urls))
]
