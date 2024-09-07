from datetime import datetime

class Tarea:
    def __init__(self, titulo, descripcion, fecha_inicio, fecha_vencimiento, etiqueta):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_vencimiento = fecha_vencimiento
        self.etiqueta = etiqueta

    def set_titulo(self):
        new_titulo = input("Ingrese el titulo: \n")
        self.titulo = new_titulo

    def set_desc(self):
        new_desc = input("Ingrese el descripcion: \n")
        self.descripcion = new_desc

    def set_fecha_inicio(self):
        new_fecha_inicio = self.ingresar_fecha(1)
        self.fecha_inicio= new_fecha_inicio

    def set_fecha_venc(self):
        new_fecha_venc = self.ingresar_fecha(2)
        self.fecha_vencimiento = new_fecha_venc

    def set_etiqueta(self):
        new_etiqueta = input("Ingrese la etiqueta: \n")
        self.etiqueta = new_etiqueta

    def ingresar_fecha(self, option):
        while True:
            try:
                if option==1:
                    entrada = input("Ingrese la fecha y hora de inicio (YYYY-MM-DD HH:MM): \n")
                elif option==2:
                    entrada = input("Ingrese la fecha y hora de vencimiento (YYYY-MM-DD HH:MM): \n")
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
# tarea1 = Tarea("Entregar informe", "Preparar el informe mensual para la reunión", "trabajo")

# Mostrar la información de la tarea
# print(tarea1.mostrar_tarea())

# Operaciones del Gestor de Tareas
def crear_tarea():
    print(" -- Creación de Tareas -- \n")

    try:
        tarea_nombre = input("Ingrese el nombre de la tarea: \n")
        tarea_desc = input("Ingrese descripción de la tarea: \n")
        tarea_etiqueta = input("Ingrese etiqueta de la tarea: \n")

        new_tarea = Tarea(tarea_nombre, tarea_desc, "000", "000", tarea_etiqueta)

        new_tarea.ingresar_fecha(1)
        new_tarea.ingresar_fecha(2)

        with open("db.txt", "r") as r_file:
            db = r_file.readlines()

        with open("db.txt", "w") as w_file:
            for tarea in db:
                campos = tarea.split()
                if(campos[0] != tarea_deseada):
                    w_file.write(tarea)

    except:
        print("Ocurrio un problema durante la operación. Por favor, intente nuevamente \n")

    finally:
        print("Tarea creada exitosamente!")

    return

# DUDA: Consultar tarea en base a que???
def consultar_tarea():
    print(" -- Consulta de Tareas -- \n")

    tarea_deseada = input("Ingrese nombre de la tarea deseada: \n")

    try:
        with open("db.txt", "r") as file:
            db = file.readlines()
            for tarea in db:
                campos = tarea.split()

                if(campos[0] == tarea_deseada):
                    new_tarea = Tarea(campos[0], campos[1], campos[2], campos[3],campos[4])
                    new_tarea.mostrar_tarea()
                    break

    except:
        print("Ocurrio un problema durante la operación. Por favor, intente nuevamente \n")

    return

def actualizar_tarea():
    print(" -- Actualización de Tareas -- \n")

    tarea_deseada = input("Ingrese nombre de la tarea a actualizar: \n")

    try:
        with open("db.txt", "r") as r_file:
            db = r_file.readlines()
            for tarea in db:
                campos = tarea.split()

                if(campos[0] == tarea_deseada):
                    new_tarea = Tarea(campos[0], campos[1], campos[2], campos[3],campos[4])

                    print("\t Ingrese 1 para actualizar titulo \n \t Ingrese 2 para actualizar descripción \t")
                    print("\t Ingrese 3 para actualizar fecha de inicio \n \t Ingrese 4 para actualizar fecha de vencimiento \t")
                    print("\t Ingrese 5 para actualizar etiqueta \n")

                    opcion = input("Elija un campo a actualizar: \n")

                    setting_list = [
                        new_tarea.set_titulo, 
                        new_tarea.set_desc, 
                        new_tarea.set_fecha_inicio, 
                        new_tarea.set_fecha_venc,
                        new_tarea.set_etiqueta
                    ]

                    setting_list[opcion]()
                    break

        with open("db.txt", "w") as w_file:
            for tarea in db:
                w_file.write(tarea)
                
    except:
        print("Ocurrio un problema durante la operación. Por favor, intente nuevamente \n")

    return

def eliminar_tarea():
    print(" -- Eliminación de Tareas -- \n")

    tarea_deseada = input("Ingrese nombre de la tarea a eliminar: \n")

    try:
        with open("db.txt", "r") as r_file:
            db = r_file.readlines()

        with open("db.txt", "w") as w_file:
            for tarea in db:
                campos = tarea.split()
                if(campos[0] != tarea_deseada):
                    w_file.write(tarea)

    except:
        print("Ocurrio un problema durante la operación. Por favor, intente nuevamente \n")

    return

# Menu de la aplicación
if __name__ == "__main__":

    exit = False
    opciones_list = [crear_tarea, consultar_tarea, actualizar_tarea, eliminar_tarea]

    print(" ---- Bienvenido al sistema de Gestión de Tareas ---- \n")

    while(not exit):
        print(" --- Operaciones disponibles: --- \n")

        print("\t Ingrese 1 para Crear tarea \n \t Ingrese 2 para Consultar tarea \t")
        print("\t Ingrese 3 para Actualizar tarea \n \t Ingrese 4 para Eliminar tarea \t")
        print("\t Ingrese 5 para salir del sistema \n")

        opcion = input("Elija una operación: \n")

        num_opcion = int(opcion)

        if num_opcion in range(1, 5):
            opciones_list[num_opcion - 1]()

        elif(num_opcion == 5):
            exit = True

        else:
            print("Operación no existente. Por favor, ingrese una opción valida \n")

    print(" ---- Gracias por usar el sistema de Gestión de Tareas. Hasta pronto! ---- ")