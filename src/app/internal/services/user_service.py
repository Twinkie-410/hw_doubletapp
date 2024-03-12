from app.internal.models.user import User


async def get_user_by_id(id):
    return await User.objects.filter(external_id=id).afirst()


async def create_user(id, username, first_name='', phone=''):
    return await User.objects.acreate(exteranl_id=id,
                                      username=username,
                                      first_name=first_name,
                                      phone=phone)


async def get_or_create(id, username, first_name, phone=''):
    return await User.objects.aget_or_create(external_id=id,
                                             defaults={
                                                 'username': username,
                                                 'first_name': first_name,
                                                 'phone': phone})


async def set_phone_number(id, number, username='', first_name=''):
    return await User.objects.aupdate_or_create(external_id=id,
                                                defaults={
                                                    'first_name': first_name,
                                                    'username': username,
                                                    'phone': number
                                                })
