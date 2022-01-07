"""restaurants URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

import restaurants_site.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurant/<str:slug>', restaurants_site.views.restaurant),
    path('', restaurants_site.views.home),
    path('signup', restaurants_site.views.signup),
    path('signin', restaurants_site.views.signin),
    path('signout', restaurants_site.views.signout),
    path('authtest', restaurants_site.views.authtest),
    path('<str:catchall>', restaurants_site.views.redirect),

] + static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)
