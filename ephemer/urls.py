"""ephemer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from magicauth.urls import urlpatterns as magicauth_urls

from ephemer.apps.experiments.urls import urlpatterns as experiments_urls
from ephemer.apps.home import views as home_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_views.Home.as_view(), name="home"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("faq", home_views.faq, name="home-faq"),
    path("guide", home_views.guide, name="home-guide"),
    path("contact", home_views.contact, name="home-contact"),
    path("__debug__/", include(debug_toolbar.urls)),
]

urlpatterns.extend(magicauth_urls)
urlpatterns.extend(experiments_urls)

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
