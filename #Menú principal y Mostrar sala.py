#Menú principal y Mostrar sala

import time
reservas = {}
FILAS = 5
COLUMNAS = 8
sala = []
Total_de_asientos = FILAS * COLUMNAS
contador = 1

for f in range(FILAS):
    fila = []
    for c in range(COLUMNAS):
        fila.append(str(contador))
        contador += 1
    sala.append(fila)



def mostrar_sala():
        print("\n       PANTALLA \n")
        for fila in sala:
            print(" ".join(fila))

    

# Este será el archivo principal.
# En este archivo uniremos el trabajo de cada uno de los colaboradores.


# =============================================================================
# Bastián - Clientes (Parte A):
# Función para lista clientes.
# Función para crea clientes pidiendo todos los datos.
# =============================================================================

import time

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
        Nombre = (input(":")).upper()
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
            print("Cerrando")    #Opción con la cual se sale del bucle y del menú
            print("...")
            time.sleep(1)
            break                             #Simple decoración para crear un retraso simulando un menú normal



# =============================================================================
# Héctor - Clientes (Parte B):
# Función para modifica clientes buscando por RUT.  
# Función para elimina clientes buscando por RUT.
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
    Gestiona el proceso de reserva de asientos para lo clientes.
    
    Aplica filtros de seguridad independientes para validar que el client exista,
    esté vigente y que los asientos seleccionados estén disponibles. 
    
    Implementa un "carrito temporal" mediante la lista 'asientos_a_reservar' 
    para acumular y validar las selecciones una a una, asegurando que la 
    reserva original no se modifique hasta que todo el proceso sea correcto.
    """
    print("\n--- RESERVAR ASIENTOS ---")
    rut = input("Ingrese el RUT del cliente que reserva: ").strip().upper()

    # 1. Filtro de seguridad: ¿Existe el cliente?
    if rut not in Clientes:
        print("Error: El cliente no está registrado. Debe crearlo primero.")
        return

    # 2. Filtro de seguridad: ¿Está vigente?
    datos_cliente = Clientes[rut]
    if datos_cliente["Vigencia"] != "S":
        print("Error: El cliente no está VIGENTE. No puede realizar reservas.")
        return

    mostrar_sala()
    
    asientos_a_reservar = []
    print("Ingrese los números de asiento que desea uno a uno. Para terminar, escriba '0'.")
    
    # Bucle para pedir asientos hasta que el usuario escriba 0
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

        # Si todo está OK, lo metemos al carrito temporal
        asientos_a_reservar.append(num_asiento)

    if len(asientos_a_reservar) == 0:
        print("No se seleccionaron asientos. Reserva cancelada.")
        return

    # GUARDADO FINAL EN EL DICCIONARIO
    if rut in reservas:
        reservas[rut].extend(asientos_a_reservar) # Suma a lo que ya tenía
    else:
        reservas[rut] = asientos_a_reservar # Crea su primera reserva

    print(f"¡Reserva completada con éxito! Asientos asignados: {asientos_a_reservar}")

# ==============================================================================

def modificar_reserva():
    """
    Permite a un cliente modificar su reserva actual de asientos.
    El cliente ingresa su RUT, se valida que exista y tenga reservas activas.
    Luego, se muestra su reserva actual y se le da la opción de seleccionar nuevos asientos.

    Para evitar conflictos, la reserva original se elimina temporalmente durante el proceso de selección.
    Si el cliente no selecciona nuevos asientos, se le devuelve su reserva original.
    """
    print("\n--- MODIFICAR RESERVA ---")
    rut = input("Ingrese el RUT del cliente para modificar su reserva: ").strip().upper()

    if rut not in Clientes or rut not in reservas or len(reservas[rut]) == 0:
        print("El cliente no existe o no tiene reservas activas.")
        return

    print(f"Tus asientos actuales son: {reservas[rut]}")
    
    # El truco maestro: borramos su reserva temporalmente para liberar los asientos en la pantalla
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

    # Si se arrepiente y no elige nada, le devolvemos su respaldo
    if len(nuevos_asientos) == 0:
        reservas[rut] = respaldo_asientos
        print("Se mantiene tu reserva original.")
    else:
        reservas[rut] = nuevos_asientos
        print(f"¡Reserva modificada con éxito! Nuevos asientos: {nuevos_asientos}")

# ==============================================================================

def eliminar_reserva():
    """
    Permite a un cliente eliminar completamente su reserva de asientos.
    El cliente ingresa su RUT, se valida que exista y tenga reservas activas.
    Al eliminar la reserva, los asientos quedan automáticamente libres para otro clientes.
    No es necesario un proceso complejo, ya que al eliminar la llave del diccionario 'reservas',
    se liberan todos los asientos asociados a ese cliente.
    """

    print("\n--- ELIMINAR RESERVA ---")
    rut = input("Ingrese el RUT del cliente para cancelar su reserva: ").strip().upper()

    if rut not in reservas:
        print("Este cliente no tiene ninguna reserva registrada.")
        return

    # Con solo borrar la llave del diccionario, los asientos quedan libres automáticamente
    del reservas[rut]
    print("¡La reserva ha sido eliminada y los asientos vuelven a estar disponibles!")

# ==============================================================================

def listar_reservas():
    """
    Muestra un listado de todas las reservas activas en el cine.
    Para cada reserva, se muestra el RUT del cliente, su nombre (obtenido del diccionario clientes') y los asientos que ha reservado.
    Si no hay reservas, se muestra un mensaje indicando que no hay ninguna reserva registrada.
    Esta función es útil para tener una visión general de todas las reservas actuales en el cine.
    """

    print("\n--- LISTADO DE RESERVAS ACTIVAS ---")
    
    if len(reservas) == 0:
        print("No hay ninguna reserva registrada en el cine.")
        return

    for rut, lista_asientos in reservas.items():
        # Buscamos el nombre del cliente en el otro diccionario usando su RUT
        nombre_cliente =Clientes[rut][0] 
        print(f"RUT: {rut} | Nombre: {nombre_cliente} | Asientos Reservados: {lista_asientos}")
"""
Fin Gestión de Reservas
"""
def Menú_principal():
    opcion = 0
    while opcion != 8:
        print()
        print("|==-- Menú principal --==|")
        print("1)Alta y consulta d clientes\n2)Modificar/Elimina clientes\n3)Reserva asientos\n4)Modificar reservas\n5)Eliminar reservas")
        print("6)Listar reservas\n7)Imprimir sala\n8)Salir")
        opcion = int(input(":"))
        match opcion:
            case 1:
                Menú_Clientes_PA()
            case 2:
                print()
            case 3:
                reservar_asientos()
            case 4:
                modificar_reserva()
            case 5:
                eliminar_reserva()
            case 6:
                listar_reservas()
            case 7:
                mostrar_sala()
            case 8:
                print("Cerrando aplicación")
                print("...")
                time.sleep(1)       
Menú_principal()


        
