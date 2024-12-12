from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_user import views

app_name = 'user'

router = DefaultRouter()
# router.register('memo1', Memo1ViewSet, basename='memo1')

urlpatterns = [
    path('create/', views.CreateUserView.as_view(),name='create'),
    path('', include(router.urls)),
]

# AUTH_USER_MODEL = 'accounts.CustomUser'
