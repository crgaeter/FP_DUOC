# Este será el archivo principal.
# En este archivo uniremos el trabajo de cada uno de los colaboradores.

import time

# =============================================================================
# ANNY - VARIABLES GLOBALES Y ESTRUCTURA BASE (Bastián se encaragará)
# =============================================================================
clientes = {}   # Diccionario unificado en minúsculas
reservas = {}   # Diccionario de reservas
FILAS = 5
COLUMNAS = 8

def mostrar_sala():
    """ Muestra un mapa provisional de la sala de cine """
    print("[ MAPA DE LA SALA DE CINE (5x8) ]")


# =============================================================================
# BASTIÁN - CLIENTES (PARTE A):
# Función para listar clientes y crear clientes pidiendo todos los datos.
# =============================================================================

def CrearUser_Menú():   # Creamos la funcion para crear usuarios
    Rut_Cliente = "" # Variable simple para que funcione el if que sigue
    
    if Rut_Cliente not in clientes: # Condicional para filtrar si el rut esta registrado o no
        print()  # De aquí para abajo es una secuencia que pide un ingreso de datos que se van guardando
        print("|==== Creación de cliente ====|")
        print("Rut: ")
        Rut_Cliente = input(":").upper().strip()
        if Rut_Cliente in clientes:
            print("Rut ya registrado")
            return
        print("Nombre: ")
        Nombre = str(input(":")).upper().strip()
        print("Mail")
        Mail = str(input(":")).upper().strip()
        print("Teléfono: ")
        Télefono = str(input(":"))
        print("Vigencia: ")
        print("S para cliente vigente y N para cliente no vigente")
        Vigencia = str(input(":")).upper().strip()

    clientes[Rut_Cliente] = {          # Así se irán guardando los datos, asociandose deacuerdo al rut.
        "Nombre": Nombre,
        "Mail": Mail,
        "Teléfono": Télefono,
        "Vigencia": Vigencia
    }
    print("¡Cliente registrado con éxito!")
    

def Menú_Clientes_PA():
    while True:     # Bucle infinito, más abajo se especifica con que condición se sale del bucle.
        print()
        print("<|==-- Alta y consulta de clientes --==|>")
        print("1)Crear cliente\n2)Lista de clientes\n3)Salir")
        print("Seleccione una opción")
        opc = int(input(":"))
        if opc == 1:              # Se ejecuta la función para crear usuario.
            CrearUser_Menú()
        elif opc == 2:            # Se libera una lista de los datos de cada cliente asociado al rut, y se recorre con un for.
             if len(clientes) == 0:
                 print("No hay clientes registrados.")
             for Rut, Datos in clientes.items():
                 print("|==Clientes registrados==|")
                 print(f"Rut: {Rut} | Datos: {Datos} ")
        elif opc == 3:
            print("Cerrando gestión de clientes")    # Opción con la cual se sale del bucle y del menú
            print("...")
            time.sleep(1)                             # Simple decoración para crear un retraso simulando un menú normal
            break    # break para quebrar el codigo y terminarlo


# =============================================================================
# HÉCTOR - CLIENTES (PARTE B):
# Función para modificar clientes y eliminar clientes buscando por RUT.  
# =============================================================================

def modificar_cliente():
    """Busca un cliente por RUT y permite cambiar sus datos uno por uno."""
    print("\n--- MODIFICAR CLIENTE ---")
    rut = input("Ingrese el RUT del cliente a modificar: ").strip().upper()

    # Validamos si el RUT existe en nuestra "base de datos"
    if rut not in clientes:
        print("El cliente con ese RUT no existe.")
        return

    # Obtenemos el diccionario actual de ese cliente (Corregido a formato Diccionario)
    datos_actuales = clientes[rut]

    print(f"Modificando a: {datos_actuales['Nombre']}")
    print("(Presione ENTER si no desea cambiar el dato actual)")

    # Pedimos los nuevos datos
    nuevo_nombre = input(f"Nuevo nombre [{datos_actuales['Nombre']}]: ").strip().upper()
    nuevo_telefono = input(f"Nuevo teléfono [{datos_actuales['Teléfono']}]: ").strip()
    nuevo_mail = input(f"Nuevo mail [{datos_actuales['Mail']}]: ").strip().upper()
    nuevo_estado = input(f"¿Vigente? (S/N) [{datos_actuales['Vigencia']}]: ").strip().upper()

    # Si el usuario escribió algo, actualizamos la llave correspondiente
    if nuevo_nombre != "":
        datos_actuales["Nombre"] = nuevo_nombre
    if nuevo_telefono != "":
        datos_actuales["Teléfono"] = nuevo_telefono
    if nuevo_mail != "":
        datos_actuales["Mail"] = nuevo_mail
    if nuevo_estado == "S" or nuevo_estado == "N":
        datos_actuales["Vigencia"] = nuevo_estado

    # Guardamos el diccionario modificado de vuelta
    clientes[rut] = datos_actuales
    print("¡Datos del cliente actualizados correctamente!")


def eliminar_cliente():
    """Borra un cliente del sistema y libera automáticamente sus reservas."""
    print("\n--- ELIMINAR CLIENTE ---")
    rut = input("Ingrese el RUT del cliente a eliminar: ").strip().upper()

    if rut not in clientes:
        print("El cliente con ese RUT no existe.")
        return

    # Regla del enunciado: Al eliminar un cliente, se borran sus reservas
    if rut in reservas:
        del reservas[rut] 
        print("-> Se han liberado los asientos que este cliente tenía reservados.")

    # Borramos al cliente de nuestro diccionario principal
    del clientes[rut]
    print("¡Cliente eliminado del sistema correctamente!")


# =============================================================================
# ANNY - ESTRUCTURA BASE Y MENÚ (Bastián se encargará)
# =============================================================================

# (Espacio reservado para Anny)


# =============================================================================
# CRISTIAN - MÓDULO DE GESTIÓN DE RESERVAS:
# Funciones para reservar, modificar, eliminar y listar reservas.
# =============================================================================

def reservar_asientos():
    """
    Gestiona el proceso de reserva de asientos para los clientes.
    """
    print("\n--- RESERVAR ASIENTOS ---")
    rut = input("Ingrese el RUT del cliente que reserva: ").strip().upper()

    # 1. Filtro de seguridad: ¿Existe el cliente?
    if rut not in clientes:
        print("Error: El cliente no está registrado. Debe crearlo primero.")
        return

    # 2. Filtro de seguridad: ¿Está vigente? (Corregido a formato Diccionario)
    datos_cliente = clientes[rut]
    if datos_cliente["Vigencia"] != "S":
        print("Error: El cliente no está VIGENTE. No puede realizar reservas.")
        return

    mostrar_sala()
    
    asientos_a_reservar = []
    print("Ingrese los números de asiento que desea uno a uno. Para terminar, escriba '0'.")
    
    while True:
        entrada = input("Número de asiento: ").strip()
        
        if not entrada.isdigit():
            print("Por favor, ingrese un número válido.")
            continue
            
        num_asiento = int(entrada)
        
        if num_asiento == 0:
            break
            
        # 3. Filtro: ¿El número está dentro de la sala?
        if num_asiento < 1 or num_asiento > (FILAS * COLUMNAS):
            print("Error: Ese número de asiento no existe en la sala.")
            continue

        # 4. Filtro: ¿Alguien más ya compró este asiento?
        ya_ocupado = False
        for lista_asientos in reservas.values():
            if num_asiento in lista_asientos:
                ya_ocupado = True
                
        if ya_ocupado == True:
            print("Error: Ese asiento ya está reservado por otro cliente.")
            continue

        # 5. Filtro: Evitar que ingrese el mismo número dos veces
        if num_asiento in asientos_a_reservar:
            print("Ya añadiste este asiento a tu lista actual.")
            continue

        asientos_a_reservar.append(num_asiento)

    if len(asientos_a_reservar) == 0:
        print("No se seleccionaron asientos. Reserva cancelada.")
        return

    # GUARDADO FINAL EN EL DICCIONARIO
    if rut in reservas:
        reservas[rut].extend(asientos_a_reservar) 
    else:
        reservas[rut] = asientos_a_reservar 

    print(f"¡Reserva completada con éxito! Asientos asignados: {asientos_a_reservar}")


def modificar_reserva():
    print("\n--- MODIFICAR RESERVA ---")
    rut = input("Ingrese el RUT del cliente para modificar su reserva: ").strip().upper()

    if rut not in clientes or rut not in reservas or len(reservas[rut]) == 0:
        print("El cliente no existe o no tiene reservas activas.")
        return

    print(f"Tus asientos actuales son: {reservas[rut]}")
    
    respaldo_asientos = reservas[rut]
    del reservas[rut]
    
    print("\nSelecciona tus nuevos asientos:")
    mostrar_sala()
    
    nuevos_asientos = []
    while True:
        entrada = input("Número de asiento (0 para terminar): ").strip()
        if not entrada.isdigit():
            continue
        num_asiento = int(entrada)
        
        if num_asiento == 0:
            break
            
        if num_asiento < 1 or num_asiento > 40:
            print("Ese asiento no existe.")
            continue
            
        ya_ocupado = False
        for lista_asientos in reservas.values():
            if num_asiento in lista_asientos:
                ya_ocupado = True
                
        if ya_ocupado:
            print("Asiento ocupado por otra persona.")
            continue
            
        if num_asiento in nuevos_asientos:
            continue
            
        nuevos_asientos.append(num_asiento)

    if len(nuevos_asientos) == 0:
        reservas[rut] = respaldo_asientos
        print("Se mantiene tu reserva original.")
    else:
        reservas[rut] = nuevos_asientos
        print(f"¡Reserva modificada con éxito! Nuevos asientos: {nuevos_asientos}")


def eliminar_reserva():
    print("\n--- ELIMINAR RESERVA ---")
    rut = input("Ingrese el RUT del cliente para cancelar su reserva: ").strip().upper()

    if rut not in reservas:
        print("Este cliente no tiene ninguna reserva registrada.")
        return

    del reservas[rut]
    print("¡La reserva ha sido eliminada y los asientos vuelven a estar disponibles!")


def listar_reservas():
    print("\n--- LISTADO DE RESERVAS ACTIVAS ---")
    
    if len(reservas) == 0:
        print("No hay ninguna reserva registrada en el cine.")
        return

    for rut, lista_asientos in reservas.items():
        # Corregido a formato Diccionario para leer los datos de Bastián
        nombre_cliente = clientes[rut]["Nombre"] 
        print(f"RUT: {rut} | Nombre: {nombre_cliente} | Asientos Reservados: {lista_asientos}")