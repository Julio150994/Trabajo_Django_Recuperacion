from django.contrib import messages


class CarritoCompra:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        
        if not carrito:
            carrito = self.session["carrito"] = {}# igualamos el carrito a nuestra sesión actual            
        self.carrito = carrito
        
    def aniadir(self, medicamento):
        if str(medicamento.id) not in self.carrito.keys():
            self.carrito[medicamento.id] = {
                "nombre": medicamento.nombre,
                "descripcion": medicamento.descripcion,
                "receta": medicamento.receta,
                "precio": medicamento.precio,
                "stock": medicamento.stock,
                "cantidad": 0 # inicializamos a 0 por no tener productos en el carrito
            }
        else:
            for clave, valor in self.carrito.items():# porque guardamos información en diccionario
                if clave == str(medicamento.id):
                    valor["cantidad"] += 1
                    break
        self.save() # para almacenar medicamentos en sesión
        
    def save(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True
        
    def eliminar(self, medicamento):
        id_medicamento = str(medicamento.id)
        
        if id_medicamento in self.carrito:
            del self.carrito[id_medicamento]# eliminamos elemento de lista
            self.save()# para persistir durante la sesión actual
            
    def decrementar(self, medicamento):
        for clave, valor in self.carrito.items():
            if clave == str(medicamento.id):
                valor["cantidad"] -= 1 # para decrementar en 1
                
                if valor["cantidad"] < 1:
                    self.eliminar(medicamento)
                else:
                    self.save()
                break
            else:
                messages.add_message(self.request, level=messages.WARNING, message="Medicamentos no encontrados en el carrito")
                
    def limpiar(self):
        # Eliminamos todos los medicamentos del carrito a la vez
        self.session["carrito"] = {}
        self.session.modified = True