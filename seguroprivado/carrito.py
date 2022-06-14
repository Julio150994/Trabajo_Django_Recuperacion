# Para realizar el carrito de compra utilizando nuestras sesiones

class CarritoCompra(object):
    lista_medicamentos = list()
    dict_medicamentos = dict()
    
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
            
            print("Traza(1): "+str(self.carrito_compra[id]))
            #self.lista_medicamentos.append(self.carrito_compra[id])
            print("Traza(2): "+str(self.carrito_compra[id]["nombre"]))
            print("Traza(3): "+str(self.carrito_compra[id]["cantidad"]))
            #print("Lista(1): "+str(self.lista_medicamentos))
            self.dict_medicamentos = {self.carrito_compra[id]["nombre"] : self.carrito_compra[id]["cantidad"]}
            
            for medicamento in self.lista_medicamentos:
                self.lista_medicamentos.append(medicamento)
            
            print("Resultado: "+str(self.lista_medicamentos))
            print("Dict(1): "+str(self.dict_medicamentos))
        else:
            self.carrito_compra[id]["cantidad"] += 1
            self.carrito_compra[id]["precio_acumulado"] = multiplicar_precio(medicamento.precio, self.carrito_compra[id]["cantidad"])
            self.carrito_compra[id]["nombre"] = medicamento.nombre
            self.carrito_compra[id]["precio"] = medicamento.precio # precio sin aumentar
            
            print("Traza(1.1): "+str(self.carrito_compra[id]))
            print("Traza(2.1): "+str(self.carrito_compra[id]["nombre"]))
            print("Traza(3.1): "+str(self.carrito_compra[id]["cantidad"]))
            
            print("Dict(2): "+str(self.dict_medicamentos))
            
        self.session["nombre"] = medicamento.nombre
        self.session["precio"] = medicamento.precio
        self.comprar()

    def comprar(self):
        self.session["carrito"] = self.carrito_compra
        self.session.modified = True
        
    def eliminar(self, medicamento):
        id_medicamento = str(medicamento.id)
        
        """if self.carrito_compra[id_medicamento] in self.lista_medicamentos:
            self.lista_medicamentos.remove(self.carrito_compra[id_medicamento])
            print("Lista(3): "+str(self.lista_medicamentos))"""
        
        if id_medicamento in self.carrito_compra:
            self.session["nombre"] = medicamento.nombre
            self.session["precio"] = medicamento.precio
            
            print("Traza(1.2): "+str(self.carrito_compra[id_medicamento]))
            print("Traza(2.2): "+str(self.carrito_compra[id_medicamento]["nombre"]))
            print("Traza(3.2): "+str(self.carrito_compra[id_medicamento]["cantidad"]))
            
            del self.carrito_compra[id_medicamento]# eliminamos medicamento
            print("Traza (1.2.1): "+str(self.carrito_compra))
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
            
            print("Traza(1.3): "+str(self.carrito_compra[id]))
            print("Traza(2.3): "+str(self.carrito_compra[id]["nombre"]))
            print("Traza(3.3): "+str(self.carrito_compra[id]["cantidad"]))
            #self.lista_medicamentos.remove(self.carrito_compra[id])
            #print("Lista(4): "+str(self.lista_medicamentos))
            # Verificamos las cantidades de los medicamentos
            if self.carrito_compra[id]["cantidad"] == 0:
                #self.lista_medicamentos.remove(self.carrito_compra[id])
                #print("Lista(5): "+str(self.lista_medicamentos))
                print("Traza(1.4): "+str(self.carrito_compra))
                # Eliminamos el medicamento del carrito
                self.eliminar(medicamento)
                #self.lista_medicamentos.clear()
            self.comprar()
        
    def limpiar(self):
        self.session["carrito"] = {}
        #self.lista_medicamentos.clear()
        #print("Lista(6): "+str(self.lista_medicamentos))
        self.session.modified = True

# Función para la multiplicación de los medicamentos añadidos al carrito
def multiplicar_precio(num1, num2):
    if num2 == 0:
        return 0
    elif num2 == 1:
        return num1
    else:
        return num1 + multiplicar_precio(num1, num2-1)