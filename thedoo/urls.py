from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('master/', admin.site.urls),
    path('',include('user.urls')),
    path('thedoo/',include('master.urls')),
    path('shop/',include('store.urls')),
    path('cart/',include('cart.urls')),
    path('order/', include('order.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = 'user.views.error_404'