from rest_framework.generics import RetrieveAPIView

from app.internal.models.user import User
from app.internal.services.user_service import UserSerializer


class UserDetailAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "external_id"

