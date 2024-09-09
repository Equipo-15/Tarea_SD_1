from datetime import datetime
import json
import logging
import os

class Tarea:
    ETIQUETAS_PREDEFINIDAS = ["Trabajo", "Personal", "Urgente", "Reunión", "Estudio"]
    ESTADOS = ["En progreso", "Completada"]

    def __init__(self, titulo=None, descripcion=None, fecha_inicio=None, fecha_vencimiento=None, etiqueta=None):
        if not titulo:
            self.titulo = self.ingresar_dato("Título")
            self.descripcion = self.ingresar_dato("Descripción")
            self.fecha_inicio = self.ingresar_fecha("inicio")
            self.fecha_vencimiento = self.ingresar_fecha("vencimiento")
            self.etiqueta = self.seleccionar_etiqueta()

        else:
            self.titulo = titulo
            self.descripcion = descripcion
            self.fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M')
            self.fecha_vencimiento = datetime.strptime(fecha_vencimiento, '%Y-%m-%d %H:%M')
            self.etiqueta = etiqueta


    def get_titulo(self):
        return self.titulo
    
    def get_desc(self):
        return self.descripcion
    
    def get_fecha_inicio(self):
        return self.fecha_inicio.strftime('%Y-%m-%d %H:%M')
    
    def get_fecha_venc(self):
        return self.fecha_vencimiento.strftime('%Y-%m-%d %H:%M')
    
    def get_etiqueta(self):
        return self.etiqueta

    def set_titulo(self):
        new_titulo = input("Ingrese el titulo: \n")
        self.titulo = new_titulo

    def set_desc(self):
        new_desc = input("Ingrese el descripcion: \n")
        self.descripcion = new_desc

    def set_fecha_inicio(self):
        new_fecha_inicio = self.ingresar_fecha(1)
        self.fecha_inicio = new_fecha_inicio

    def set_fecha_venc(self):
        new_fecha_venc = self.ingresar_fecha(2)
        self.fecha_vencimiento = new_fecha_venc

    def set_etiqueta(self):
        new_etiqueta = input("Ingrese la etiqueta: \n")
        self.etiqueta = new_etiqueta

    #
    def ingresar_dato(self, dato):
        entrada = input(f"Ingresar {dato}: ")
        return entrada
    #
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
    #
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

    #
    def mostrar_tarea(self):
        fecha_inicio_formateada = self.fecha_inicio.strftime('%Y-%m-%d %H:%M')
        fecha_vencimiento_formateada = self.fecha_vencimiento.strftime('%Y-%m-%d %H:%M')
        return (f"Título: {self.titulo}\n"
                f"Descripción: {self.descripcion}\n"
                f"Fecha de Inicio: {fecha_inicio_formateada}\n"
                f"Fecha de Vencimiento: {fecha_vencimiento_formateada}\n"
                f"Etiqueta: {self.etiqueta}")

    #
    def guardar_en_archivo(self, usuario, logger):
        try:
            archivo = f"{usuario}_tareas.txt"
            with open(archivo, 'a') as file:
                file.write(f"{self.titulo}|{self.descripcion}|"
                           f"{self.fecha_inicio.strftime('%Y-%m-%d %H:%M')}|"
                           f"{self.fecha_vencimiento.strftime('%Y-%m-%d %H:%M')}|"
                           f"{self.etiqueta}\n")
            logger.info("Tarea guardada en archivo")
        except:
            logger.warning("Ocurrio un problema al guardar la tarea")
            print("Ocurrio un problema guardando la tarea. Por favor, intente nuevamente \n")

    def mostrar_etiquetas(logger):
        try:
            print("Etiquetas actuales:")
            for etiqueta in Tarea.ETIQUETAS_PREDEFINIDAS:
                print(f"- {etiqueta}")
            logger.info("Etiquetas mostradas")
        except:
            logger.warning("Ocurrio un problema al mostrar las etiquetas")
            print("Ocurrio un problema durante la operación. Por favor, intente nuevamente \n")

    # Función para agregar una etiqueta
    def agregar_etiqueta(etiqueta, logger):
        try:
            if etiqueta not in Tarea.ETIQUETAS_PREDEFINIDAS:
                Tarea.ETIQUETAS_PREDEFINIDAS.append(etiqueta)
                logger.info(f"Etiqueta {etiqueta} agregada")
                print(f"Etiqueta '{etiqueta}' agregada con éxito.")
            else:
                print(f"La etiqueta '{etiqueta}' ya existe.")

        except:
            logger.warning("Ocurrio un problema al agregar las etiquetas")
            print("Ocurrio un problema durante la operación. Por favor, intente nuevamente \n")            

    # Función para eliminar una etiqueta
    def eliminar_etiqueta(etiqueta, logger):
        try:
            if etiqueta in Tarea.ETIQUETAS_PREDEFINIDAS:
                Tarea.ETIQUETAS_PREDEFINIDAS.remove(etiqueta)
                logger.info(f"Etiqueta {etiqueta} eliminada")
                print(f"Etiqueta '{etiqueta}' eliminada con éxito.")
            else:
                print(f"La etiqueta '{etiqueta}' no existe.")
        
        except:
            logger.warning("Ocurrio un problema al eliminar las etiquetas")
            print("Ocurrio un problema durante la operación. Por favor, intente nuevamente \n")

    @staticmethod
    def editar_etiqueta(logger):
        print("\n--- Menú de edición de Etiquetas ---")
        print("1. Mostrar etiquetas")
        print("2. Agregar etiqueta")
        print("3. Eliminar etiqueta")
        print("4. salir")
        opcion = input("Elija una operación: \n")

        if opcion == "1" :
            print("Etiquetas existentes:\n")
            Tarea.mostrar_etiquetas(logger)
        elif opcion == "2":
            etiqueta = input("Ingrese nombre de nueva etiqueta:")
            Tarea.agregar_etiqueta(etiqueta, logger)
        elif opcion == "3":
            etiqueta = input("Ingrese nombre de a eliminar:")
            Tarea.eliminar_etiqueta(etiqueta, logger)
        elif opcion == "3":
            print("volviendo a menú\n")
    
    #
    @staticmethod
    def eliminar_tarea(usuario, titulo, logger):
        archivo = f"{usuario}_tareas.txt"

        try:
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
                logger.info(f"Tarea {titulo} eliminada")
                print("Tarea eliminada con éxito.")
        except:
            logger.warning("Ocurrio un problema durante la eliminación de la tarea")
            print("Ocurrio un problema durante la operación. Por favor, intente nuevamente \n")

    #
    @staticmethod
    def modificar_tarea(usuario, titulo, logger):
        archivo = f"{usuario}_tareas.txt"

        try:
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
                    logger.info(f"Tarea {titulo} modificada")
                print("Tarea modificada con éxito.")
            else:
                print("No se encontró la tarea con ese título.")
        except:
            logger.warning("Ocurrio un problema al modificar la tarea")
            print("Ocurrio un problema durante la operación. Por favor, intente nuevamente \n")
    
    #
    @staticmethod
    def cambiar_estado(usuario, titulo, logger):
        archivo = f"{usuario}_tareas.txt"

        try:
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
                logger.info(f"Estado de tarea {titulo} cambiado")
                print("Estado de la tarea cambiado con éxito.")
            else:
                print("No se encontró la tarea con ese título.")

        except:
            logger.warning("Ocurrio un problema al modificar la tarea")
            print("Ocurrio un problema durante la operación. Por favor, intente nuevamente \n")

    @staticmethod
    def filtrar_tarea(usuario, logger):
        archivo = f"{usuario}_tareas.txt"
        if not os.path.exists(archivo):
            print("No hay tareas para modificar el estado.")
            return
        
        print(" -- Filtrado de Tareas -- \n")

        print("\t Ingrese 1 para filtrar según titulo \n \t Ingrese 2 para filtrar según descripción \t")
        print("\t Ingrese 3 para filtrar según fecha de inicio \n \t Ingrese 4 para filtrar según fecha de vencimiento \t")
        print("\t Ingrese 5 para filtrar según etiqueta \n")

        opcion = input("Elija un campo para aplicar filtro: \n")

        filtro = input("Elija el filtro a aplicar (campo igual a): \n")

        try:
            with open(archivo, "r") as file:
                db = file.readlines()
                for tarea in db:
                    campos = tarea.strip("\n").split("|")

                    if(campos[int(opcion) - 1] == filtro):
                        new_tarea = Tarea(campos[0], campos[1], campos[2], campos[3], campos[4])
                        print("* \t" + new_tarea.mostrar_tarea() + "\n")
            logger.info("Tareas mostradas con filtros aplicados")

        except:
            logger.warning("Ocurrio un problema al filtrar las tareas")
            print("Ocurrio un problema durante la operación. Por favor, intente nuevamente \n")
    
    @staticmethod
    def mostrar_tareas_usuario(usuario, logger):
        try:
            archivo = f"{usuario}_tareas.txt"
            if os.path.exists(archivo):
                print(f"Tareas de {usuario}:")
                with open(archivo, 'r') as file:
                    tareas = file.readlines()
                    for tarea in tareas:
                        titulo, descripcion, fecha_inicio, fecha_vencimiento, etiqueta = tarea.strip().split("|")
                        print(f"Título: {titulo}\nDescripción: {descripcion}\n"
                            f"Fecha de Inicio: {fecha_inicio}\nFecha de Vencimiento: {fecha_vencimiento}\nEtiqueta: {etiqueta}\n")
                logger.info(f"Tareas del usuario {usuario} impresas en consola")
            else:
                print(f"El usuario {usuario} no tiene tareas guardadas.")
        except:
            logger.warning("No se logro mostrar la tarea")
            print("Ocurrio un problema durante la operación. Por favor, intente nuevamente \n")

#
def cargar_credenciales(archivo):
    with open(archivo, 'r') as f:
        return json.load(f)

#
def verificar_credenciales(usuario, contrasena, archivo):
    credenciales = cargar_credenciales(archivo)
    return credenciales.get(usuario) == contrasena

# Función para guardar credenciales en un archivo JSON
def guardar_credenciales(credenciales, archivo):
    with open(archivo, 'w') as f:
        json.dump(credenciales, f)

#
def agregar_credenciales(usuario, contrasena, archivo):
    credenciales = cargar_credenciales(archivo)
    credenciales[usuario] = contrasena
    guardar_credenciales(credenciales, archivo)

# Menú interactivo
def menu_credenciales():
    logging.basicConfig(filename="tarea1.log",
                        filemode="a",
                        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
                        datefmt="%Y-%m-%d %H:%M",
                        level=logging.DEBUG)
    
    logger = logging.getLogger(__name__)
    
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
            
            try:
                if verificar_credenciales(usuario, contrasena, archivo):
                    logger.info(f"Ingreso de usuario {usuario}")
                    print("Acceso concedido")
                    #mostrar menú con usuario logeado
                    menu(usuario, logger)
                    break
                else:
                    print(f"Acceso denegado")
            
            except:
                logger.warning(f"Ocurrio un problema al ingresar al usuario {usuario} ")
                print("Ocurrio un problema durante el ingreso.\n")

        
        elif opcion == '2':
            try:
                usuario = input("Ingresa el nuevo usuario: ")
                contrasena = input("Ingresa la nueva contraseña: ")
                agregar_credenciales(usuario, contrasena, archivo)
                logger.info(f"Creación de usuario {usuario}")
                print("Credenciales agregadas exitosamente")
            except:
                logger.warning("Ocurrio un problema al crear usuario")
                print("Ocurrio un problema durante la creación.\n")
        
        elif opcion == '3':
            print("Saliendo del programa...")
            break
        
        else:
            print("Opción no válida, por favor selecciona una opción correcta.")

"""
#----------------------------------
# Operaciones del Gestor de Tareas
def crear_tarea():
    print(" -- Creación de Tareas -- \n")

    try:
        tarea_nombre = input("Ingrese el nombre de la tarea: \n")
        tarea_desc = input("Ingrese descripción de la tarea: \n")
        tarea_etiqueta = input("Ingrese etiqueta de la tarea: \n")

        new_tarea = Tarea(tarea_nombre, tarea_desc, "000", "000", tarea_etiqueta)

        new_tarea.set_fecha_inicio()
        new_tarea.set_fecha_venc()

        new_tarea_string = new_tarea.get_titulo() + "/" + new_tarea.get_desc() + "/" + new_tarea.get_fecha_inicio()
        new_tarea_string = new_tarea_string + "/" + new_tarea.get_fecha_venc() + "/" + new_tarea.get_etiqueta() + "\n"

        with open("db.txt", "r") as r_file:
            db = r_file.readlines()
            db.append(new_tarea_string)

        with open("db.txt", "w") as w_file:
            for tarea in db:
                w_file.write(tarea)

        print("Tarea creada exitosamente! \n")

    except:
        print("Ocurrio un problema durante la operación. Por favor, intente nuevamente \n")

    return

# DUDA: Consultar tarea en base a que???
def consultar_tarea():
    print(" -- Consulta de Tareas -- \n")

    tarea_deseada = input("Ingrese nombre de la tarea deseada: \n")

    try:
        with open("db.txt", "r") as file:
            db = file.readlines()
            for tarea in db:
                campos = tarea.split("/")
                campos[4] = campos[4].strip("\n")

                if(campos[0] == tarea_deseada):
                    new_tarea = Tarea(campos[0], campos[1], campos[2], campos[3],campos[4])
                    print("\n" + new_tarea.mostrar_tarea() + "\n")
                    break

    except:
        print("Ocurrio un problema durante la operación. Por favor, intente nuevamente \n")

    return

# DUDA: Actualizar un campo de tarea por llamada, o iterar indefinidamente como en el menu?
def actualizar_tarea():
    print(" -- Actualización de Tareas -- \n")

    tarea_deseada = input("Ingrese nombre de la tarea a actualizar: \n")

    try:
        with open("db.txt", "r") as r_file:
            db = r_file.readlines()
            i = 0
            for tarea in db:
                campos = tarea.split("/")

                if(campos[0] == tarea_deseada):
                    new_tarea = Tarea(campos[0], campos[1], campos[2], campos[3], campos[4])

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

                    setting_list[int(opcion) - 1]()
                    break
                
                else:
                    i += 1

            new_tarea_string = new_tarea.get_titulo() + "/" + new_tarea.get_desc() + "/" + new_tarea.get_fecha_inicio()
            new_tarea_string = new_tarea_string + "/" + new_tarea.get_fecha_venc() + "/" + new_tarea.get_etiqueta() + "\n"

            db[i] = new_tarea_string

        with open("db.txt", "w") as w_file:
            for tarea in db:
                w_file.write(tarea)
                
    except:
        print("Ocurrio un problema durante la operación. Por favor, intente nuevamente \n")

    return

# DUDA: Un criterio a la vez, o pueden ser varios?
# DUDA: Unico filtro "igual a" o mas filtro aplicables, como "menor a" o "mayor a"?
def filtrar_tarea():
    print(" -- Filtrado de Tareas -- \n")

    print("\t Ingrese 1 para filtrar según titulo \n \t Ingrese 2 para filtrar según descripción \t")
    print("\t Ingrese 3 para filtrar según fecha de inicio \n \t Ingrese 4 para filtrar según fecha de vencimiento \t")
    print("\t Ingrese 5 para filtrar según etiqueta \n")

    opcion = input("Elija un campo para aplicar filtro: \n")

    filtro = input("Elija el filtro a aplicar (campo igual a): \n")

    try:
        with open("db.txt", "r") as file:
            db = file.readlines()
            for tarea in db:
                campos = tarea.split("/")
                campos[4] = campos[4].strip("\n")

                if(campos[int(opcion) - 1] == filtro):
                    new_tarea = Tarea(campos[0], campos[1], campos[2], campos[3],campos[4])
                    print("* \t" + new_tarea.mostrar_tarea() + "\n")

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
                campos = tarea.split("/")
                if(campos[0] != tarea_deseada):
                    w_file.write(tarea)

    except:
        print("Ocurrio un problema durante la operación. Por favor, intente nuevamente \n")

    return



    #otro menu
    def otro():
        if __name__ == "__main__":

            exit = False
            opciones_list = [crear_tarea, consultar_tarea, actualizar_tarea, filtrar_tarea, eliminar_tarea]

            print(" ---- Bienvenido al sistema de Gestión de Tareas ---- \n")

            while(not exit):
                print(" --- Operaciones disponibles: --- \n")

                print("\t Ingrese 1 para Crear tarea \n \t Ingrese 2 para Consultar tarea \t")
                print("\t Ingrese 3 para Actualizar tarea \n \t Ingrese 4 para Filtar tareas \t")
                print("\t Ingrese 5 para Eliminar tarea \n \t Ingrese 6 para salir del sistema \t")

                opcion = input("Elija una operación: \n")

                num_opcion = int(opcion)

                if num_opcion in range(1, 6):
                    opciones_list[num_opcion - 1]()

                elif(num_opcion == 6):
                    exit = True

                else:
                    print("Operación no existente. Por favor, ingrese una opción valida \n")

"""

#
def menu(usuario, logger):
    while True:
        print(" ---- Bienvenido al sistema de Gestión de Tareas ---- \n")
        print(" --- Operaciones disponibles: --- \n")

        print("\t Ingrese 1 para Crear tarea \n \t Ingrese 2 para Consultar tarea \t")
        print("\t Ingrese 3 para Actualizar tarea \n \t Ingrese 4 para Filtar tareas \t")
        print("\t Ingrese 5 para Eliminar tarea \n \t Ingrese 6 para modificar estado \t")
        print("\t Ingrese 7 para modificar etiquetas \n \t Ingrese 8 para salir del sistema \t")
        opcion = input("Elija una operación: \n")

        if opcion == "1":
            tarea = Tarea()
            tarea.guardar_en_archivo(usuario, logger)
        elif opcion == "2":
            Tarea.mostrar_tareas_usuario(usuario, logger)
        elif opcion == "3":
            titulo = input("Ingrese el título de la tarea que desea modificar: ")
            Tarea.modificar_tarea(usuario, titulo, logger)
        elif opcion == "4":
            #filtrar
            Tarea.filtrar_tarea(usuario, logger)
        elif opcion == "5":
            titulo = input("Ingrese el título de la tarea que desea eliminar: ")
            Tarea.eliminar_tarea(usuario, titulo, logger)
        elif opcion == "6":
            titulo = input("Ingrese el título de la tarea que desea modifar el estado: ")
            Tarea.cambiar_estado(usuario, titulo, logger)
        elif opcion == "7":
            Tarea.editar_etiqueta(logger)
        elif opcion == "8":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

archivo = 'credenciales.json'
credenciales = cargar_credenciales(archivo)

usuario = menu_credenciales()
