"""
URL configuration for diplom_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from diplom_API.views import UsersView, FileDataView, UsersCreateView, UpdateDataView, DownloadFileView, GenerateExternalDownloadLinkView, ExternalDownloadLinkView, CheckUser, GetFilesAllUsers, GetFilesUser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers
from diplom_API.yasg import urlpatterns as docs_urls

router = routers.SimpleRouter()
router.register(r'users', UsersView)
# router.register(r'user', UsersDestroyView)
router.register(r'user', UsersCreateView)
router.register(r'files', FileDataView)
router.register(r'file', UpdateDataView)
router.register(r'download', DownloadFileView)
router.register(r'create_external_link', GenerateExternalDownloadLinkView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/download_external_link', ExternalDownloadLinkView.as_view()),
    path('api/v1/check_user', CheckUser.as_view()),
    path('api/v1/get_all_files', GetFilesAllUsers.as_view()),
    path('api/v1/get_user_files/<int:id>', GetFilesUser.as_view()),
]

urlpatterns += docs_urls
