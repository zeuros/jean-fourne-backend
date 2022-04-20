"""bake_end URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import TemplateView

from . import settings
from .views import Clients, Products, Categories, ShoppingCartUpdate, ShoppingCart, ClientUpdate

urlpatterns = [
    # OAuth stuff
    path('auth/', TemplateView.as_view(template_name="index.html")),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
    path('admin/', admin.site.urls),

    # Api paths
    path('client/<int:pk>/', ClientUpdate.as_view()),
    path('clients/', Clients.as_view(), name="cart"),
    path('products/', Products.as_view()),
    path('category/', Categories.as_view()),
    path('cart/', ShoppingCart.as_view(), name="cart"),
    path('cart-item/<int:pk>/', ShoppingCartUpdate.as_view()),

    # Uploaded files paths
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]