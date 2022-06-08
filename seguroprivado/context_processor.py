# Para realizar el proceso del total de carrito de compra
def precio_total(request):
    total = 0.0
    
    if request.user.is_authenticated:
        if "carrito_compra" in request.session.keys():   
            for clave, valor in request.session["carrito_compra"].items():
                total += int(valor["precio_acumulado"])
    
    return {"precio_total": total}