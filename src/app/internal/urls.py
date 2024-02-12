from django.urls import path

from app.internal.transport.rest.handlers import UserDetailAPIView

urlpatterns = [
    path("user/<int:external_id>/me", UserDetailAPIView.as_view(), name='/me')
]
