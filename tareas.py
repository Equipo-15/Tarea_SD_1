from datetime import datetime

class Tarea:
    def __init__(self, titulo, descripcion, etiqueta):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_inicio = self.ingresar_fecha(1)  # Llamada a la función durante la creación
        self.fecha_vencimiento = self.ingresar_fecha(2)  # Llamada a la función durante la creación
        self.etiqueta = etiqueta

    def ingresar_fecha(self, option):
        while True:
            try:
                if option==1:
                    entrada = input("Ingrese la fecha y hora de inicio (YYYY-MM-DD HH:MM): ")
                elif option==2:
                    entrada = input("Ingrese la fecha y hora de vencimiento (YYYY-MM-DD HH:MM): ")
                fecha = datetime.strptime(entrada, '%Y-%m-%d %H:%M')
                return fecha
            except ValueError:
                print("Formato de fecha y hora incorrecto. Por favor, ingrese la fecha en el formato 'YYYY-MM-DD HH:MM'.")

    def mostrar_tarea(self):
        fecha_inicio_formateada = self.fecha_vencimiento.strftime('%Y-%m-%d %H:%M')
        fecha_vencimiento_formateada = self.fecha_vencimiento.strftime('%Y-%m-%d %H:%M')
        return (f"Título: {self.titulo}\n"
                f"Descripción: {self.descripcion}\n"
                f"Fecha de Inicio: {fecha_inicio_formateada}\n"
                f"Fecha de Vencimiento: {fecha_vencimiento_formateada}\n"
                f"Etiqueta: {self.etiqueta}")

# Crear una instancia de Tarea
tarea1 = Tarea("Entregar informe", "Preparar el informe mensual para la reunión", "trabajo")

# Mostrar la información de la tarea
print(tarea1.mostrar_tarea())