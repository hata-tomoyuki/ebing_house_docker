from django.views.generic import TemplateView
from django.utils.timezone import now
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import timedelta

## for adding username in cookies
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

## logout
from django.contrib.auth import logout
from django.http import JsonResponse

## build react
# from django.shortcuts import render

# def index(request):
#     return render(request, 'index.html')  # コピーされた build/index.html を参照

from django.http import FileResponse

def serve_media(request, path):
    return FileResponse(open(f'media/{path}', 'rb'), content_type='image/webp')


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['start_date'] = now().date()- timedelta(days=7)
        context['end_date'] = now().date()
        return context
    
## for adding username in cookies
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']  # 認証されたユーザー
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,          # トークン
            'username': user.username,  # ユーザー名を追加
        })
        

def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})

