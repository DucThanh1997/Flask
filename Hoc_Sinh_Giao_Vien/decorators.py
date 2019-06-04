from models.user import UserModel


def sv_authenticate(func):
    def wrapper(id, *args, **kwargs):
        user = UserModel.find_by_ma(id)
        if user.chuc_vu == 1:
            return func(id, *args, **kwargs)
        else:
            return {'messages': 'Không phải là học sinh'}
    return wrapper


def gv_authenticate(func):
    def wrapper(id, *args, **kwargs):
        user = UserModel.find_by_ma(id)
        if user.chuc_vu == 2:
            return func(id, *args, **kwargs)
        else:
            return {'messages': 'Không phải là giáo viên'}
    return wrapper
