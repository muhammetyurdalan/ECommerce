from graphql_jwt.decorators import user_passes_test

def roles_required(*roles):
    def check_perm(user, *args, **kwargs):
        if not user.is_active:
            return False
        if user.role in roles:
            return True
        return False
    return user_passes_test(check_perm)
