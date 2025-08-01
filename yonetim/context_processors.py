def user_roles_processor(request):
    """
    Tüm şablonlara kullanıcının temel rol bilgilerini ekler.
    """
    is_sube_muduru = False
    if request.user.is_authenticated:
        is_sube_muduru = request.user.groups.filter(name="Şube Müdürü").exists()

    return {"is_sube_muduru": is_sube_muduru}
