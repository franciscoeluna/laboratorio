import json
from datetime import datetime
from venta import Venta

class GestorVentas:
    def __init__(self, archivo):
        self.archivo = archivo
        self.ventas = self.cargar_ventas()

    def cargar_ventas(self):
        try:
            with open(self.archivo, 'r') as file:
                ventas = json.load(file)
                if isinstance(ventas, dict):
                    return ventas
                else:
                    return {}
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def guardar_ventas(self):
        with open(self.archivo, 'w') as file:
            json.dump(self.ventas, file, indent=4)

    def generar_id_venta(self):
        return datetime.now().strftime('%Y%m%d%H%M%S%f')

    def crear_venta(self, venta):
        try:
            if not isinstance(venta, Venta):
                raise ValueError("El objeto no es una instancia de la clase Venta.")
            id_venta = self.generar_id_venta()
            self.ventas[id_venta] = venta.to_dict()
            self.guardar_ventas()
        except Exception as e:
            print(f"Error al crear la venta: {e}")

    def leer_venta(self, id_venta):
        try:
            return self.ventas[id_venta]
        except KeyError:
            print("Venta no encontrada.")
            return None

    def actualizar_venta(self, id_venta, nueva_venta):
        try:
            if not isinstance(nueva_venta, Venta):
                raise ValueError("El objeto no es una instancia de la clase Venta.")
            if id_venta not in self.ventas:
                raise KeyError("La venta con el ID especificado no existe.")
            self.ventas[id_venta] = nueva_venta.to_dict()
            self.guardar_ventas()
        except KeyError:
            print("Venta no encontrada.")
        except Exception as e:
            print(f"Error al actualizar la venta: {e}")

    def eliminar_venta(self, id_venta):
        try:
            if id_venta not in self.ventas:
                raise KeyError("La venta con el ID especificado no existe.")
            del self.ventas[id_venta]
            self.guardar_ventas()
        except KeyError:
            print("Venta no encontrada.")
        except Exception as e:
            print(f"Error al eliminar la venta: {e}")

    def buscar_ventas_por_fecha(self, fecha):
        ventas_encontradas = []
        for id_venta, venta in self.ventas.items():
            venta_fecha = datetime.strptime(venta['fecha'], "%Y-%m-%d").strftime("%d/%m/%Y")
            if venta_fecha == fecha:
                ventas_encontradas.append((id_venta, venta))
        return ventas_encontradas
