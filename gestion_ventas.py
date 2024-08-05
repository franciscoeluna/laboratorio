import json
from datetime import datetime

#Clase base
class Venta:
    def __init__(self, fecha, cliente, productos):
        self.fecha = fecha
        self.cliente = cliente
        self.productos = productos

    def to_dict(self):
        return {
            'fecha': self.fecha,
            'cliente': self.cliente,
            'productos': self.productos,
            'tipo': self.__class__.__name__
        }

#Clase derivada
class VentaOnline(Venta):
    def __init__(self, fecha, cliente, productos, direccion_envio):
        super().__init__(fecha, cliente, productos)
        self.direccion_envio = direccion_envio

    def to_dict(self):
        data = super().to_dict()
        data['direccion_envio'] = self.direccion_envio
        return data

#Clase derivada
class VentaLocal(Venta):
    def __init__(self, fecha, cliente, productos, tienda):
        super().__init__(fecha, cliente, productos)
        self.tienda = tienda

    def to_dict(self):
        data = super().to_dict()
        data['tienda'] = self.tienda
        return data


class GestorVentas:
    def __init__(self, archivo):
        self.archivo = archivo
        self.ventas = self.cargar_ventas()

    def cargar_ventas(self):
        try:
            with open(self.archivo, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def guardar_ventas(self):
        with open(self.archivo, 'w') as file:
            json.dump(self.ventas, file, indent=4)

    def crear_venta(self, venta):
        try:
            if not isinstance(venta, Venta):
                raise ValueError("El objeto no es una instancia de la clase Venta.")
            self.ventas.append(venta.to_dict())
            self.guardar_ventas()
        except Exception as e:
            print(f"Error al crear la venta: {e}")

    def leer_venta(self, index):
        try:
            return self.ventas[index]
        except IndexError:
            print("Venta no encontrada.")
            return None

    def actualizar_venta(self, index, nueva_venta):
        try:
            if not isinstance(nueva_venta, Venta):
                raise ValueError("El objeto no es una instancia de la clase Venta.")
            self.ventas[index] = nueva_venta.to_dict()
            self.guardar_ventas()
        except IndexError:
            print("Venta no encontrada.")
        except Exception as e:
            print(f"Error al actualizar la venta: {e}")

    def eliminar_venta(self, index):
        try:
            self.ventas.pop(index)
            self.guardar_ventas()
        except IndexError:
            print("Venta no encontrada.")
        except Exception as e:
            print(f"Error al eliminar la venta: {e}")

#Menú interactivo
def main():
    gestor = GestorVentas('ventas.json')
    
    while True:
        print("\n--- Gestión de Ventas ---")
        print("1. Crear venta online")
        print("2. Crear venta local")
        print("3. Leer venta")
        print("4. Actualizar venta")
        print("5. Eliminar venta")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            fecha = datetime.now().date().isoformat()
            cliente = input("Ingrese el nombre del cliente: ").capitalize()
            productos = input("Ingrese los productos vendidos (separados por coma): ").split(',')
            direccion_envio = input("Ingrese la dirección de envío: ")
            venta = VentaOnline(fecha, cliente, productos, direccion_envio)
            gestor.crear_venta(venta)
        
        elif opcion == '2':
            fecha = datetime.now().date().isoformat()
            cliente = input("Ingrese el nombre del cliente: ")
            productos = input("Ingrese los productos vendidos (separados por coma): ").split(',')
            tienda = input("Ingrese la tienda: ")
            venta = VentaLocal(fecha, cliente, productos, tienda)
            gestor.crear_venta(venta)
        
        elif opcion == '3':
            index = int(input("Ingrese el índice de la venta a leer: "))
            venta = gestor.leer_venta(index)
            if venta:
                print(venta)
        
        elif opcion == '4':
            index = int(input("Ingrese el índice de la venta a actualizar: "))
            tipo = input("Ingrese el tipo de venta (online/local): ").lower()
            fecha = datetime.now().date().isoformat()
            cliente = input("Ingrese el nombre del cliente: ")
            productos = input("Ingrese los productos vendidos (separados por coma): ").split(',')
            
            if tipo == 'online':
                direccion_envio = input("Ingrese la dirección de envío: ")
                nueva_venta = VentaOnline(fecha, cliente, productos, direccion_envio)
            elif tipo == 'local':
                tienda = input("Ingrese la tienda: ")
                nueva_venta = VentaLocal(fecha, cliente, productos, tienda)
            else:
                print("Tipo de venta no válido.")
                continue
            
            gestor.actualizar_venta(index, nueva_venta)
        
        elif opcion == '5':
            index = int(input("Ingrese el índice de la venta a eliminar: "))
            gestor.eliminar_venta(index)
        
        elif opcion == '6':
            break
        
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()