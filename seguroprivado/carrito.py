# Para realizar el carrito de compra utilizando nuestras sesiones

class CarritoCompra(object):
    lista_medicamentos = list()
    
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito_compra = self.session.get("carrito")
        
        if not carrito_compra:
            self.session["carrito"] = {}
            self.carrito_compra = self.session["carrito"]
        else:
            self.carrito_compra = carrito_compra
            
    def aniadir(self, medicamento):
        id = str(medicamento.id)
        
        if id not in self.carrito_compra.keys():
            self.carrito_compra[id] = {
                "medicamento_id": id,
                "nombre": medicamento.nombre,
                "descripcion": medicamento.descripcion,
                "receta": medicamento.receta,
                "precio": medicamento.precio,
                "precio_acumulado": medicamento.precio,
                "stock": medicamento.stock,
                "cantidad": 1,
            }
            self.lista_medicamentos.append(self.carrito_compra[id])
            print("Lista(1): "+str(self.lista_medicamentos))
        else:
            self.carrito_compra[id]["cantidad"] += 1
            self.carrito_compra[id]["precio_acumulado"] = multiplicar_precio(medicamento.precio, self.carrito_compra[id]["cantidad"])
            self.carrito_compra[id]["nombre"] = medicamento.nombre
            self.carrito_compra[id]["precio"] = medicamento.precio # precio sin aumentar
        
        self.session["nombre"] = medicamento.nombre
        self.session["precio"] = medicamento.precio
        
        print("Traza(1): "+str(self.carrito_compra[id])+"\n")
        self.comprar()

    def comprar(self):
        self.session["carrito"] = self.carrito_compra
        self.session.modified = True
        
    def eliminar(self, medicamento):
        id_medicamento = str(medicamento.id)
        
        if id_medicamento in self.carrito_compra:
            self.session["nombre"] = medicamento.nombre
            self.session["precio"] = medicamento.precio
            
            self.lista_medicamentos.remove(self.carrito_compra[id_medicamento])
            print("Lista(2): "+str(self.lista_medicamentos))
            del self.carrito_compra[id_medicamento]# eliminamos medicamento
            self.comprar()# para persistir durante la sesión actual
            
    def restar(self, medicamento):
        id = str(medicamento.id)
        
        if id in self.carrito_compra.keys():
            self.session["nombre"] = medicamento.nombre
            self.session["precio"] = medicamento.precio
            
            self.carrito_compra[id]["cantidad"] -= 1
            self.carrito_compra[id]["nombre"] = medicamento.nombre
            self.carrito_compra[id]["precio_acumulado"] -= medicamento.precio
            self.carrito_compra[id]["precio"] = medicamento.precio # precio sin reducir
            
            self.lista_medicamentos.remove(self.carrito_compra[id])
            print("Lista(3): "+str(self.lista_medicamentos))
            
            # Verificamos las cantidades de los medicamentos
            if self.carrito_compra[id]["cantidad"] == 0:
                # Eliminamos el medicamento del carrito
                self.eliminar(medicamento)
                self.lista_medicamentos.clear()
            self.comprar()
        
    def limpiar(self):
        self.session["carrito"] = {}
        self.lista_medicamentos.clear()
        print("Lista(4): "+str(self.lista_medicamentos))
        self.session.modified = True

# Función para la multiplicación de los medicamentos añadidos al carrito
def multiplicar_precio(num1, num2):
    if num2 == 0:
        return 0
    elif num2 == 1:
        return num1
    else:
        return num1 + multiplicar_precio(num1, num2-1)