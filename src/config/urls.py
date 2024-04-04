from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from app.internal.transport.rest.handlers import TelegramBotWebhookView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('app.internal.urls')),
    path('tg-webhook/', csrf_exempt(TelegramBotWebhookView.as_view()))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
