from ast import pattern
from django.conf import settings
# from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.contrib import admin
# from django.contrib.auth.views import login, logout
from django.urls import path
from ecommerce.settings import STATIC_ROOT
from sellinghub import views
from sellinghub import api_views
urlpatterns = [
    path('api/v1/products',api_views.ProductList.as_view()),
    path('api/v1/products/new',api_views.ProductCreate.as_view()),
    path('api/v1/products/<int:id>/',api_views.ProductRetrieveUpdateDestroy.as_view()),
    path('admin/', admin.site.urls),
    path('',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('display/',views.display,name='display'),
    path('checkout/',views.checkout,name='checkout'),
    path('orders/<int:or_id>',views.orders,name='orders'),
    path('details/<int:pr_id>/',views.details,name='details'),
    path('orderlist/',views.orderlist, name='orderlist'),
    path('addexcel/',views.addexcel, name='addexcel'),
    path('addxml/',views.addxml, name='addxml'),
    path('logout/',views.logout,name='logout'),
    path('viewtable/',views.viewtable,name='viewtable'),
]
urlpatterns += static(settings.STATIC_URL, document_root =settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)