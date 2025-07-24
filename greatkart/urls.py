from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from . import views, settings

urlpatterns = [
    path('', views.index, name='home'),
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    path('account/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
