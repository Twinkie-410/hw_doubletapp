from app.internal.models.user import User


async def get_user_by_id(id):
    return await User.objects.filter(external_id=id).afirst()


async def get_user_by_username(username):
    return await User.objects.filter(username=username).afirst()


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


async def add_to_favorite(instance_username, favorite_username):
    instance_user = await get_user_by_username(instance_username)
    favorite_user = await get_user_by_username(favorite_username)
    favorites = [user async for user in instance_user.favorites.all()]

    if instance_user and favorite_user and favorite_user not in favorites:
        await instance_user.favorites.aadd(favorite_user)


async def remove_from_favorites(instance_username, favorite_username):
    instance_user = await get_user_by_username(instance_username)
    favorite_user = await get_user_by_username(favorite_username)
    favorites = [user async for user in instance_user.favorites.all()]

    if instance_user and favorite_user and favorite_user in favorites:
        await instance_user.favorites.aremove(favorite_user)


async def get_list_favorites(username):
    user = await get_user_by_username(username)
    if user:
        list_favorites = [favorite.username async for favorite in user.favorites.all()]
        return list_favorites
