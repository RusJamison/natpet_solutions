"""
URL configuration for natpet_solutions project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    FullTextSearch,
    RobotsViews,
    SiteMapView,
    custom_page_not_found_view,
    custom_error_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('shop.urls')),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('basket/', include('basket.urls')),
    path('checkout/', include('checkout.urls')),
    path("search/", FullTextSearch.as_view(), name="search_items"),
    path('robots.txt/', RobotsViews.as_view()),
    path('sitemap.xml/', SiteMapView.as_view()),
    path("admin_dashboard/", include("admin_dashboard.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = custom_page_not_found_view
handler500 = custom_error_view
