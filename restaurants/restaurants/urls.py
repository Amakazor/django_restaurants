from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import restaurants_site.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurant/<str:slug>', restaurants_site.views.restaurant),
    path('signup', restaurants_site.views.signup),
    path('signin', restaurants_site.views.signin),
    path('signout', restaurants_site.views.signout),
    path('add', restaurants_site.views.add_restaurant),
    path('activate/<uidb64>/<token>', restaurants_site.views.activate),
    path('', restaurants_site.views.home),
    path('<str:catchall>', restaurants_site.views.redirect),

] + static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)
