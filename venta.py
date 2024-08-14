from datetime import datetime

class Venta:
    def __init__(self, fecha, cliente, productos):
        self.__fecha = fecha
        self.__cliente = cliente
        self.__productos = productos
    
    @property
    def fecha(self):
        return self.__fecha
    
    @property
    def cliente(self):
        return self.__cliente
    
    @property
    def productos(self):
        return self.__productos
    

    def to_dict(self):
        return {
            'fecha': self.__fecha,
            'cliente': self.__cliente,
            'productos': self.__productos,
            'tipo': self.__class__.__name__
        }

class VentaOnline(Venta):
    def __init__(self, fecha, cliente, productos, direccion_envio):
        super().__init__(fecha, cliente, productos)
        self.__direccion_envio = direccion_envio

    def to_dict(self):
        data = super().to_dict()
        data['direccion_envio'] = self.__direccion_envio
        return data

class VentaLocal(Venta):
    def __init__(self, fecha, cliente, productos, tienda):
        super().__init__(fecha, cliente, productos)
        self.__tienda = tienda

    def to_dict(self):
        data = super().to_dict()
        data['tienda'] = self.__tienda
        return data
