from django.shortcuts import redirect
from django.contrib import messages

# Nuestro fichero para el carrito de compra con la utilización de sesiones

class CarritoCompra:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito_compra = self.session["carrito"]
        
        if not carrito_compra:
            self.session["carrito"] = {}
            self.carrito_compra = self.session["carrito"]
        else:
            self.carrito_compra = carrito_compra
            
    def aniadir(self, medicamento):
        id = str(medicamento)
        
        if id not in self.carrito_compra.keys():
            self.carrito_compra[id] = {
                "id": id,
                "nombre": medicamento.nombre,
                "descripcion": medicamento.descripcion,
                "receta": medicamento.receta,
                "precio_acumulado": medicamento.precio,
                "stock": medicamento.stock,
                "cantidad": 1,
            }
        else:
            self.carrito_compra[id]["cantidad"] += 1
            self.carrito_compra[id]["precio_acumulado"] += medicamento.precio
        return redirect('tienda')

    def comprar(self):
        self.session["carrito"] = self.carrito_compra
        self.session.modified = True
        messages.add_message(self.request, level=messages.INFO, message="Su compra ha sido realizada correctamente")
        
    def eliminar(self, medicamento):
        id_medicamento = str(medicamento.id)
            
        if id_medicamento in self.carrito_compra:
            del self.carrito_compra[id_medicamento]# eliminamos elemento de lista
            self.comprar()# para persistir durante la sesión actual
            
    def restar(self, medicamento):
        id = str(medicamento.id)
        
        if id in self.carrito_compra.keys():
            self.carrito_compra[id]["cantidad"] -= 1
            self.carrito_compra[id]["precio_acumulado"] -= medicamento.precio
            # Verificamos las cantidades de los medicamentos
            if self.carrito[id]["cantidad"] <= 0:
                self.eliminar(medicamento)
            self.comprar()
        
    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True