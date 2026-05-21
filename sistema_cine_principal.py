# Este será el archivo principal.
# En este archivo uniremos el trabajo de cada uno de los colaboradores.

import time # Solo para simular tiempos de espera en el menú de clientes (Parte A)

# =============================================================================
# VARIABLES GLOBALES TEMPORALES (Estas las definirá Anny)
# =============================================================================
clientes = {}  # Diccionario unificado en minúsculas
reservas = {}  # Diccionario de reservas
FILAS = 5
COLUMNAS = 8

def mostrar_sala():
    """ Función temporal de Anny """
    print("[ MAPA DE LA SALA DE CINE (5x8) ]")

# =============================================================================
# Bastián - Clientes (Parte A):
# Función para listar clientes.
# Función para crear clientes pidiendo todos los datos.
# =============================================================================

#Creamos un diccionario vacío
Clientes = {

}

def CrearUser_Menú ():   #Creamos la funcion para crear usuarios
    Rut_Cliente = "" #Variable simpre para que funcione el if que sigue
    
    if Rut_Cliente not in Clientes: #Condicional para filtrar si el rut esta registrado o no
        print()  # De aquí para abajo es una secuencia que pide un ingreso de datos que se van guardando
        print("|==== Creación de cliente ====|")
        print("Rut: ")
        Rut_Cliente = input(":").upper()
        if Rut_Cliente in Clientes:
            return print("Rut ya registrado")
        print("Nombre: ")
        Nombre = str(input(":")).upper()
        print("Mail")
        Mail = str(input(":")).upper()
        Mail in Clientes
        print("Teléfono: ")
        Télefono = str(input(":"))
        print("Vigencia: ")
        print("S para cliente vigente y N para cliente no vigente")
        Vigencia = str(input(":")).upper()

    
    Clientes [Rut_Cliente] = {          #Así se irán guardando los datos, asociandose deacuerdo al rut.
        "Nombre": Nombre,
        "Mail": Mail,
        "Télefono": Télefono,
        "Vigencia": Vigencia
    }
    

def Menú_Clientes_PA():
    opc = 0           #Variables para las opciones siguientes.
    opc2 = 0
    while True:     #Bucle infinito, más abajo se especifica con que condición se sale del bucle.
        print()
        print("<|==-- Alta y consulta de clientes --==|>")
        print("1)Crear cliente\n2)Lista de clientes\n3)Salir")
        print("Seleccione una opción")
        opc = int(input(":"))
        if opc == 1:              #Se ejecuta la función para crear usuario.
            CrearUser_Menú()
        elif opc == 2:            # Se libera una lista de los datos de cada cliente asociado al rut, y se recorre con un for.
             for Rut, Datos in Clientes.items():
                 print("|==Clientes registrados==|")
                 print(f"Rut: {Rut} | Datos: {Datos} ")


        elif opc == 3:
            print("Cerrando gestión de clientes")    #Opción con la cual se sale del bucle y del menú
            print("...")
            time.sleep(1)                             #Simple decoración para crear un retraso simulando un menú normal
            break    #break para quebrar el codigo y terminarlo

Menú_Clientes_PA()

# =============================================================================
# Héctor - Clientes (Parte B):
# Función para modificar clientes buscando por RUT.  
# Función para eliminar clientes buscando por RUT.
# =============================================================================

# (Espacio reservado para Héctor)


# =============================================================================
# Anny - Estructura Base y Menú:
# Hacer el Menú principal. 
# =============================================================================

# (Espacio reservado para Anny)


# =============================================================================
# Cristian - Módulo de Gestión de Reservas:
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

    # 2. Filtro de seguridad: ¿Está vigente? (Corregido a Diccionario)
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
            
        if num_asiento < 1 or num_asiento > (FILAS * COLUMNAS):
            print("Error: Ese número de asiento no existe en la sala.")
            continue

        ya_ocupado = False
        for lista_asientos in reservas.values():
            if num_asiento in lista_asientos:
                ya_ocupado = True
                
        if ya_ocupado:
            print("Error: Ese asiento ya está reservado por otro cliente.")
            continue

        if num_asiento in asientos_a_reservar:
            print("Ya añadiste este asiento a tu lista actual.")
            continue

        asientos_a_reservar.append(num_asiento)

    if len(asientos_a_reservar) == 0:
        print("No se seleccionaron asientos. Reserva cancelada.")
        return

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
        # Corregido a formato Diccionario
        nombre_cliente = clientes[rut]["Nombre"] 
        print(f"RUT: {rut} | Nombre: {nombre_cliente} | Asientos Reservados: {lista_asientos}")


# =============================================================================
# PRUEBA DEL PROGRAMA (Solo para probar tus funciones hoy)
# =============================================================================
# Menú_Clientes_PA() # Descomenta para probar el menú de Bastián