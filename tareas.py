from datetime import datetime
import json
import os

class Tarea:
    ETIQUETAS_PREDEFINIDAS = ["Trabajo", "Personal", "Urgente", "Reunión", "Estudio"]
    ESTADOS = ["En progreso", "Completada"]

    def __init__(self, titulo=None, descripcion=None, fecha_inicio=None, fecha_vencimiento=None, etiqueta=None, nombre_archivo=None, fila_archivo=None):
        if not titulo:
            self.titulo = self.ingresar_dato("Título")
            self.descripcion = self.ingresar_dato("Descripción")
            self.fecha_inicio = self.ingresar_fecha("inicio")
            self.fecha_vencimiento = self.ingresar_fecha("vencimiento")
            self.etiqueta = self.seleccionar_etiqueta()
            self.nombre_archivo = self.ingresar_dato("Nombre de archivo")
            self.fila_archivo = self.ingresar_dato("Fila")
        else:
            self.titulo = titulo
            self.descripcion = descripcion
            self.fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M')
            self.fecha_vencimiento = datetime.strptime(fecha_vencimiento, '%Y-%m-%d %H:%M')
            self.etiqueta = etiqueta
            self.nombre_archivo = nombre_archivo
            self.fila_archivo = fila_archivo

    def ingresar_dato(self, dato):
        entrada = input(f"Ingresar {dato}: ")
        return entrada

    def ingresar_fecha(self, option):
        while True:
            try:
                if option == "inicio":
                    entrada = input("Ingrese la fecha y hora de inicio (YYYY-MM-DD HH:MM): ")
                elif option == "vencimiento":
                    entrada = input("Ingrese la fecha y hora de vencimiento (YYYY-MM-DD HH:MM): ")
                fecha = datetime.strptime(entrada, '%Y-%m-%d %H:%M')
                return fecha
            except ValueError:
                print("Formato de fecha y hora incorrecto. Por favor, ingrese la fecha en el formato 'YYYY-MM-DD HH:MM'.")

    def seleccionar_etiqueta(self):
        print("\n--- Selección de Etiquetas ---")
        for i, etiqueta in enumerate(Tarea.ETIQUETAS_PREDEFINIDAS, start=1):
            print(f"{i}. {etiqueta}")
        print(f"{len(Tarea.ETIQUETAS_PREDEFINIDAS) + 1}. Ingresar una etiqueta personalizada")

        while True:
            opcion = input("Seleccione una opción: ")

            if opcion.isdigit():
                opcion = int(opcion)

                if 1 <= opcion <= len(Tarea.ETIQUETAS_PREDEFINIDAS):
                    return Tarea.ETIQUETAS_PREDEFINIDAS[opcion - 1]
                elif opcion == len(Tarea.ETIQUETAS_PREDEFINIDAS) + 1:
                    return self.ingresar_dato("Etiqueta personalizada")
                else:
                    print("Opción no válida, intente de nuevo.")
            else:
                print("Entrada inválida, debe ingresar un número.")

    def mostrar_tarea(self):
        fecha_inicio_formateada = self.fecha_inicio.strftime('%Y-%m-%d %H:%M')
        fecha_vencimiento_formateada = self.fecha_vencimiento.strftime('%Y-%m-%d %H:%M')
        return (f"Título: {self.titulo}\n"
                f"Descripción: {self.descripcion}\n"
                f"Fecha de Inicio: {fecha_inicio_formateada}\n"
                f"Fecha de Vencimiento: {fecha_vencimiento_formateada}\n"
                f"Etiqueta: {self.etiqueta}\n"
                f"Nombre de archivo: {self.nombre_archivo}\n"
                f"Fila: {self.fila_archivo}")

    def guardar_en_archivo(self, usuario):
        archivo = f"{usuario}_tareas.txt"
        with open(archivo, 'a') as file:
            file.write(f"{self.titulo}|{self.descripcion}|"
                       f"{self.fecha_inicio.strftime('%Y-%m-%d %H:%M')}|"
                       f"{self.fecha_vencimiento.strftime('%Y-%m-%d %H:%M')}|"
                       f"{self.etiqueta}|{self.nombre_archivo}|{self.fila_archivo}\n")

    @staticmethod
    def eliminar_tarea(usuario, titulo):
        archivo = f"{usuario}_tareas.txt"
        if not os.path.exists(archivo):
            print("No hay tareas que eliminar.")
            return

        with open(archivo, 'r') as file:
            tareas = file.readlines()

        tareas_modificadas = [tarea for tarea in tareas if not tarea.startswith(titulo + "|")]

        if len(tareas) == len(tareas_modificadas):
            print("No se encontró la tarea con ese título.")
        else:
            with open(archivo, 'w') as file:
                file.writelines(tareas_modificadas)
            print("Tarea eliminada con éxito.")

    @staticmethod
    def modificar_tarea(usuario, titulo):
        archivo = f"{usuario}_tareas.txt"
        if not os.path.exists(archivo):
            print("No hay tareas para modificar.")
            return

        with open(archivo, 'r') as file:
            tareas = file.readlines()

        tareas_modificadas = []
        tarea_encontrada = False
        for tarea in tareas:
            if tarea.startswith(titulo + "|"):
                print("Modificando tarea...")
                nueva_tarea = Tarea()  # Crear una nueva tarea con los datos modificados
                tarea_encontrada = True
                tareas_modificadas.append(f"{nueva_tarea.titulo}|{nueva_tarea.descripcion}|"
                                          f"{nueva_tarea.fecha_inicio.strftime('%Y-%m-%d %H:%M')}|"
                                          f"{nueva_tarea.fecha_vencimiento.strftime('%Y-%m-%d %H:%M')}|"
                                          f"{nueva_tarea.etiqueta}|{nueva_tarea.nombre_archivo}|{nueva_tarea.fila_archivo}\n")
            else:
                tareas_modificadas.append(tarea)

        if tarea_encontrada:
            with open(archivo, 'w') as file:
                file.writelines(tareas_modificadas)
            print("Tarea modificada con éxito.")
        else:
            print("No se encontró la tarea con ese título.")
    
    @staticmethod
    def cambiar_estado(usuario, titulo):
        archivo = f"{usuario}_tareas.txt"
        if not os.path.exists(archivo):
            print("No hay tareas para modificar el estado.")
            return

        with open(archivo, 'r') as file:
            tareas = file.readlines()

        tareas_modificadas = []
        tarea_encontrada = False
        for tarea in tareas:
            datos = tarea.strip().split("|")
            if datos[0] == titulo:
                print("\n--- Cambiar Estado ---")
                for i, estado in enumerate(Tarea.ESTADOS, start=1):
                    print(f"{i}. {estado}")
                opcion = input("Seleccione el nuevo estado: ")

                if opcion.isdigit() and 1 <= int(opcion) <= len(Tarea.ESTADOS):
                    nuevo_estado = Tarea.ESTADOS[int(opcion) - 1]
                    datos[5] = nuevo_estado  # Actualizar el estado en los datos
                    tarea_encontrada = True
                    tareas_modificadas.append("|".join(datos) + "\n")
                else:
                    print("Opción no válida, el estado no fue cambiado.")
                    return
            else:
                tareas_modificadas.append(tarea)

        if tarea_encontrada:
            with open(archivo, 'w') as file:
                file.writelines(tareas_modificadas)
            print("Estado de la tarea cambiado con éxito.")
        else:
            print("No se encontró la tarea con ese título.")

def cargar_credenciales(archivo):
    with open(archivo, 'r') as f:
        return json.load(f)

def verificar_credenciales(usuario, contrasena, archivo):
    credenciales = cargar_credenciales(archivo)
    return credenciales.get(usuario) == contrasena

def mostrar_tareas_usuario(usuario):
    archivo = f"{usuario}_tareas.txt"
    if os.path.exists(archivo):
        print(f"Tareas de {usuario}:")
        with open(archivo, 'r') as file:
            tareas = file.readlines()
            for tarea in tareas:
                titulo, descripcion, fecha_inicio, fecha_vencimiento, etiqueta, nombre_archivo, fila_archivo = tarea.strip().split("|")
                print(f"Título: {titulo}\nDescripción: {descripcion}\n"
                      f"Fecha de Inicio: {fecha_inicio}\nFecha de Vencimiento: {fecha_vencimiento}\n"
                      f"Etiqueta: {etiqueta}\nNombre de archivo: {nombre_archivo}\nFila: {fila_archivo}\n")
    else:
        print(f"El usuario {usuario} no tiene tareas guardadas.")

# Función para guardar credenciales en un archivo JSON
def guardar_credenciales(credenciales, archivo):
    with open(archivo, 'w') as f:
        json.dump(credenciales, f)

def agregar_credenciales(usuario, contrasena, archivo):
    credenciales = cargar_credenciales(archivo)
    credenciales[usuario] = contrasena
    guardar_credenciales(credenciales, archivo)

# Menú interactivo
def menu_credenciales():
    archivo = 'credenciales.json'
    
    while True:
        print("\n--- Menú de Credenciales ---")
        print("1. Verificar credenciales")
        print("2. Agregar credenciales")
        print("3. Salir")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == '1':
            usuario = input("Ingresa el usuario: ")
            contrasena = input("Ingresa la contraseña: ")
            if verificar_credenciales(usuario, contrasena, archivo):
                print("Acceso concedido")
                #mostrar menú con usuario logeado
                menu(usuario)
                break
            else:
                print("Acceso denegado")
        
        elif opcion == '2':
            usuario = input("Ingresa el nuevo usuario: ")
            contrasena = input("Ingresa la nueva contraseña: ")
            agregar_credenciales(usuario, contrasena, archivo)
            print("Credenciales agregadas exitosamente")
        
        elif opcion == '3':
            print("Saliendo del programa...")
            break
        
        else:
            print("Opción no válida, por favor selecciona una opción correcta.")

def menu(usuario):
    while True:
        print("\n--- Menú de Tareas ---")
        print("1. Ver tareas")
        print("2. Agregar nueva tarea")
        print("3. Modificar tarea")
        print("4. Eliminar tarea")
        print("5. Modificar estado")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_tareas_usuario(usuario)
        elif opcion == "2":
            tarea = Tarea()
            tarea.guardar_en_archivo(usuario)
        elif opcion == "3":
            titulo = input("Ingrese el título de la tarea que desea modificar: ")
            Tarea.modificar_tarea(usuario, titulo)
        elif opcion == "4":
            titulo = input("Ingrese el título de la tarea que desea eliminar: ")
            Tarea.eliminar_tarea(usuario, titulo)
        elif opcion == "5":
            titulo = input("Ingrese el título de la tarea que desea modifar el estado: ")
            Tarea.cambiar_estado(usuario, titulo)
        elif opcion == "6":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

archivo = 'credenciales.json'
credenciales = cargar_credenciales(archivo)

usuario = menu_credenciales()
