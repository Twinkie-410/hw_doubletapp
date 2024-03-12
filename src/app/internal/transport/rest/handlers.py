from django.http import JsonResponse
from django.views import View
from app.internal.services.user_service import get_user_by_id


class UserDetailAPIView(View):
    @staticmethod
    async def get(request, external_id):
        user = await get_user_by_id(external_id)
        if not user:
            return JsonResponse({'error': f'user by id: {external_id} not found'}, status=404)
        return JsonResponse({
            'external_id': user.external_id,
            'first_name': user.first_name,
            'username': user.username,
            'phone': user.phone.as_e164
        }, status=200)
