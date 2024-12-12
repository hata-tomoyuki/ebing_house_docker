from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path,include
from .views import HomeView

# from rest_framework.authtoken import views
from .views import CustomAuthToken

from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth.views import LogoutView

from .views import logout_view, serve_media
#  index  # config/views.py にある logout_view をインポート

from django.http import HttpResponseRedirect

def dev_redirect(request):
    # React 開発サーバーにリダイレクト
    print("#########  redirect to 3000  #########")
    return HttpResponseRedirect("http://localhost:3000/")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('wlist/', include('wlist.urls')),
    # path('',TemplateView.as_view(template_name='home.html'), name='home'),
    path('home/', HomeView.as_view(template_name='home.html'), name='home'),

    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # path('authen/', views.obtain_auth_token),  # rest_frameworkの標準
    path('authen/', CustomAuthToken.as_view()),
    path('api_user/',include('api_user.urls')),
    path('api_word/',include('api_word.urls')),
    path('api_memo1/',include('api_memo1.urls')),
    path('api_memo2/',include('api_memo2.urls')),

    # path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('api/logout/', logout_view, name='logout'),  # logout_view をルートに追加

    # path('react_index/', index, name='index'),

    ##### 本番環境用 #####
    # path('', TemplateView.as_view(template_name='index.html'), name='react_index'),
    # path('media/<path:path>', serve_media, name='serve_media'),
    # path('<path:path>', TemplateView.as_view(template_name='index.html')),  # その他のReact用ルート
    #####################

    ##### 開発環境用 #####
    path("", dev_redirect),
    #####################

]

if settings.DEBUG or settings.ALLOW_MEDIA_DELIVERY_IN_PRODUCTION:  # 開発環境、本番環境でメディアファイル提供を許可
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
