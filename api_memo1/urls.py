from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Memo1ViewSet

app_name = 'api_memo1'

router = DefaultRouter()
router.register(r'memo1', Memo1ViewSet, basename='memo1')

urlpatterns = [
    path('',include(router.urls))
]
