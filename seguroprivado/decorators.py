from django.contrib.auth.decorators import user_passes_test


def RolAdmin(function=None, login='sign_in'):
    decorador = user_passes_test(lambda usuario: usuario.is_active
        and usuario.is_superuser, login_url=login,)
    
    if function:
        return decorador

def RolMedico(function=None, login='sign_in'):
    decorador = user_passes_test(lambda usuario: usuario.is_active
        and usuario.is_staff and not usuario.is_superuser, login_url=login,)
    
    if function:
        return decorador

def RolPaciente(function=None, login='sign_in'):
    decorador = user_passes_test(lambda usuario: usuario.is_active
        and not usuario.is_superuser and not usuario.is_staff, login_url=login,)
    
    if function:
        return decorador