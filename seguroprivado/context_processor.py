# Para realizar el proceso del total de carrito de compra
def precio_total(request):
    total = 0.0
    
    # Validamos que sea un usuario paciente
    if request.user.is_authenticated and not request.user.is_staff:
        if "carrito" in request.session.keys():
            for clave, valor in request.session["carrito"].items():
                total += float(valor["precio_acumulado"])
                request.session["precio_acumulado"] = total
    return {"precio_total": total}