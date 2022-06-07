from django.shortcuts import redirect
from django.contrib import messages

# Utilizamos sesiones para las funcionalidades del carrito de compra

class CarritoCompra(object):
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito_compra = self.session["carrito"]
        
        if not carrito_compra:
            self.session["carrito"] = {}
            self.carrito_compra = self.session["carrito"]
        else:
            self.carrito_compra = carrito_compra
            
    def aniadir_medicamento(self, medicamento):
        id = str(medicamento)
        print("Id de medicamento: "+str(id))
        print("Nombre: "+str())
        
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

    def guardar_compra(self):
        self.session["carrito"] = self.carrito_compra
        self.session.modified = True
        messages.add_message(self.request, level=messages.INFO, message="Su compra ha sido realizada correctamente")
        
    def eliminar_medicamento(self, medicamento):
        id_medicamento = str(medicamento.id)
            
        if id_medicamento in self.carrito_compra:
            del self.carrito_compra[id_medicamento]# eliminamos elemento de lista
            self.guardar_compra()# para persistir durante la sesión actual
            
    def restar(self, medicamento):
        id = str(medicamento.id)
        
        if id in self.carrito_compra.keys():
            self.carrito_compra[id]["cantidad"] -= 1
            self.carrito_compra[id]["precio_acumulado"] -= medicamento.precio
            # Verificamos las cantidades de los medicamentos
            if self.carrito[id]["cantidad"] <= 0:
                self.eliminar_medicamento(medicamento)
            self.guardar_compra()
        
    def limpiar_compra(self):
        self.session["carrito"] = {}
        self.session.modified = True
        
    # Para realizar el proceso del total de carrito de compra
    def precio_total(request):
        total = 0
        
        if request.user.is_authenticated:
            if "carrito_compra" in request.session.keys():   
                for clave, valor in request.session["carrito_compra"].items():
                    total += int(valor["precio_acumulado"])
        
        return {"precio_total": total}