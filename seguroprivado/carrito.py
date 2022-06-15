# Para realizar el carrito de compra utilizando nuestras sesiones

class CarritoCompra(object):
    lista_compra = list()
    medicamentos = list()
    
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
        else:
            self.carrito_compra[id]["cantidad"] += 1
            self.carrito_compra[id]["precio_acumulado"] = multiplicar_precio(medicamento.precio, self.carrito_compra[id]["cantidad"])
            self.carrito_compra[id]["nombre"] = medicamento.nombre
            self.carrito_compra[id]["precio"] = medicamento.precio # precio sin aumentar
            
        self.session["nombre"] = medicamento.nombre
        self.session["precio"] = medicamento.precio
        
        print("Traza: "+str(self.carrito_compra[id].values()))
        #self.lista_compra.append(set_medicamento)
        
        """for compra in self.carrito_compra[id].values():
            for medicamento in self.medicamentos:    
                #self.medicamentos.append(compra)
                self.lista_compra.append(medicamento)
        
        print("Traza(1): "+str(self.lista_compra))"""
        self.comprar()

    def comprar(self):
        self.session["carrito"] = self.carrito_compra
        self.session.modified = True
        
    def eliminar(self, medicamento):
        id_medicamento = str(medicamento.id)
        
        if id_medicamento in self.carrito_compra:
            self.session["nombre"] = medicamento.nombre
            self.session["precio"] = medicamento.precio
            print(self.carrito_compra[id_medicamento])
            
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
            #print(self.carrito_compra[id])
            
            if self.carrito_compra[id]["cantidad"] == 0:
                # Eliminamos el medicamento del carrito
                self.eliminar(medicamento)
                #self.lista_compra.clear()
                #print(self.carrito_compra[id])
            self.comprar()
        
    def limpiar(self):
        self.session["carrito"] = {}
        #self.lista_compra.clear()
        print(self.carrito_compra)
        self.session.modified = True

# Función para la multiplicación de los medicamentos añadidos al carrito
def multiplicar_precio(num1, num2):
    if num2 == 0:
        return 0
    elif num2 == 1:
        return num1
    else:
        return num1 + multiplicar_precio(num1, num2-1)