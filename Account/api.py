from Account.schemas import *
from Cosmetic.schemas import MessageOut
from ninja import Router
from django.contrib.auth import get_user_model, authenticate
from Account.authorization import *

User = get_user_model()

account_controller = Router(tags=['auth'])


@account_controller.post('signup', response={
    400: MessageOut,
    201: AuthOut,
})
def signup(request, account_in: AccountCreate):
    if account_in.password1 != account_in.password2:
        return 400, {'detail': 'Passwords do not match!'}

    try:
        User.objects.get(email=account_in.email)
    except User.DoesNotExist:
        new_user = User.objects.create_user(first_name=account_in.first_name, last_name=account_in.last_name,
                                            email=account_in.email, password=account_in.password1,
                                            phone_number=account_in.phone_number, address=account_in.address)

        token = get_tokens_for_user(new_user)

        return 201, {
            'token': token,
            'account': new_user,
        }

    return 400, {'detail': 'User already registered!'}


@account_controller.post('signin', response={
    200: AuthOut,
    404: MessageOut,
})
def signin(request, signin_in: SigninSchema):
    user = authenticate(email=signin_in.email, password=signin_in.password)
    if not user:
        return 404, {'detail': 'User does not exist'}

    token = get_tokens_for_user(user)

    return {
        'token': token,
        'account': user
    }


@account_controller.get('', auth=GlobalAuth(), response={
    200: AccountOut,
    401: MessageOut})
def me(request):
    if 'pk' not in request.auth:
        return 401, {'detail': "Unauthorized"}
    return User.objects.get(id=request.auth['pk'])


@account_controller.put('update', auth=GlobalAuth(), response={
    200: AccountOut,
    401: MessageOut
})
def update_account(request, update_in: AccountUpdate):
    User.objects.filter(id=request.auth['pk']).update(**update_in.dict())
    return User.objects.get(id=request.auth['pk'])


@account_controller.post('change-password', auth=GlobalAuth(), response={
    200: MessageOut,
    400: MessageOut,
    401: MessageOut
})
def change_password(request, password_update: ChangePasswordSchema):
    user = User.objects.get(id=request.auth['pk'])
    if password_update.new_password1 != password_update.new_password2:
        return 400, {'detail': 'passwords do not match'}
    is_old = user.check_password(password_update.old_password)

    if not is_old:
        return 401, {'detail': 'Old Password Is Incorrect'}
    user.set_password(password_update.new_password1)
    user.save()
    return 200, {'detail': 'password updated successfully'}
