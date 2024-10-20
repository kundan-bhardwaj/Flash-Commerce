"""
URL configuration for FlashCommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from api.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('products/', create_product, name='product-list-create'),
    path('products/<int:pr>/', view_update_products, name='product-detail'),
    path('orders/', create_order, name='order-list-create'),
    path('orders/<int:pr>/', view_orders, name='order-detail'),
    path('orders/<int:pr>/cancel/', cancel_order, name='cancel-order'),
    path('orders/<int:pr>/ship/', ship_order, name='ship-order'),
    path('orders/<int:pr>/deliver/', deliver_order, name='deliver-order'),

] 

handler404 = 'api.views.custom_404_view'
