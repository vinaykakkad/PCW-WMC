"""pclub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from home.views import home_page_view
from resources.views import ResourcesView
from account.views import RegisterView, LoginView, EmailActivateView, ForgotPasswordView, PasswordSetterView, logout_view, ProfileView
from events.views import EventsPageView
from about.views import about_page_view 
from profiles.views import profiles_list_view, home_profile_view, github_api_view, codeforces_api_view
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # home
    path('', home_page_view, name='home'),
    # account
    path('login/', LoginView.as_view(), name='user_login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>', EmailActivateView.as_view(), name='activate'),
    path('password/forgot/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('password/reset/', PasswordSetterView.as_view(), name='reset_password'),
    path('password/reset/<username64>/<token>/', PasswordSetterView.as_view(), name='reset_password'),
    path('logout/', logout_view, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    # resources
    path('resources/', ResourcesView.as_view(), name='resources'),
    # events
    path('events/', EventsPageView.as_view(), name='events'),
    # about
    path('about/', about_page_view, name='about'),
    # profiles
    path('profile/home', home_profile_view, name='profile_home'),
    path('profile/cfapi/', codeforces_api_view, name='cfapi'),
    path('profile/github/', github_api_view, name='github'),
    path('profiles/list/', profiles_list_view, name='profiles')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
