# =============================================================================
# ARCHIVO PRINCIPAL - SISTEMA DE GESTIÓN DE CINE
# En este archivo uniremos el trabajo de cada uno de los colaboradores.
# =============================================================================

import time

# =============================================================================
# VARIABLES GLOBALES
# =============================================================================
reservas = {}
clientes = {} # Estandarizado
filas = 5
columnas = 8
sala = []
total_de_asientos = filas * columnas
contador = 1

# Matriz de la sala
for f in range(filas):
    fila = []
    for c in range(columnas):
        fila.append(str(contador))
        contador += 1
    sala.append(fila)


def mostrar_sala():
    """ Muestra el mapa de la sala reflejando asientos libres y ocupados (XX) """
    print("\n        PANTALLA \n")
    for fila in sala:
        fila_mostrar = []
        for asiento in fila:
            num = int(asiento)
            # Verificamos si el asiento está en el listado de alguna reserva
            esta_reservado = False
            for lista in reservas.values():
                if num in lista:
                    esta_reservado = True
                    break
            
            # Si está reservado mostramos XX, si no, alineamos el número a 2 dígitos
            if esta_reservado:
                fila_mostrar.append("XX")
            else:
                fila_mostrar.append(f"{num:02d}")
        print(" ".join(fila_mostrar))
    print("\n( XX = Asiento Ocupado )")


# =============================================================================
# BASTIÁN - CLIENTES (PARTE A):
# Función para listar clientes y crear clientes pidiendo todos los datos.
# =============================================================================

def crear_user_menu():   # Nombre estandarizado 
    """ Permite el registro de nuevos usuarios en el sistema """
    print()  
    print("|==== Creación de cliente ====|")
    print("Rut (sin puntos ni guion): ")
    rut_cliente = input(":").upper().strip() # Estandarizado
    
    if rut_cliente in clientes:
        print("Rut ya registrado")
        return
        
    print("Nombre: ")
    nombre = input(":").upper().strip()
    print("Mail:")
    mail = input(":").upper().strip()
    print("Teléfono: ")
    telefono = input(":").strip()
    print("Vigencia: ")
    print("S para cliente vigente y N para cliente no vigente")
    vigencia = input(":").upper().strip()

    # Se guardan los datos estructurados en un sub-diccionario unificado
    clientes[rut_cliente] = {          
        "nombre": nombre,
        "mail": mail,
        "telefono": telefono,
        "vigencia": vigencia
    }
    print("¡Cliente registrado con éxito!")
    

def menu_clientes_pa():   # Nombre estandarizado a snake_case
    """ Submenú para el alta y consulta rápida de clientes """
    while True:     
        print()
        print("<|==-- Alta y consulta de clientes --==|>")
        print("1) Crear cliente\n2) Lista de clientes\n3) Salir")
        print("Seleccione una opción")
        try:
            opc = int(input(":"))
        except ValueError:
            print("Por favor, ingrese un número válido.")
            continue
            
        if opc == 1:              
            crear_user_menu()
        elif opc == 2:            
            if len(clientes) == 0:
                print("No hay clientes registrados.")
            for rut, datos in clientes.items():
                print("|== Clientes registrados ==|")
                print(f"Rut: {rut} | Datos: {datos} ")
        elif opc == 3:
            print("Cerrando")    
            print("...")
            time.sleep(1)
            break                             


# =============================================================================
# HÉCTOR - CLIENTES (PARTE B):
# Función para modificar clientes y eliminar clientes buscando por RUT.  
# =============================================================================

def modificar_cliente():
    """ Busca un cliente por RUT y permite cambiar sus datos uno por uno """
    print("\n--- MODIFICAR CLIENTE ---")
    rut = input("Ingrese el RUT del cliente a modificar: ").strip().upper()

    # Validamos si el RUT existe en la base de datos
    if rut not in clientes:
        print("El cliente con ese RUT no existe.")
        return

    # Obtenemos el diccionario actual de ese cliente (Corregido de Lista a Diccionario)
    datos_actuales = clientes[rut]

    print(f"Modificando a: {datos_actuales['nombre']}")
    print("(Presione ENTER si no desea cambiar el dato actual)")

    # Pedimos los nuevos datos respetando la estructura de Bastián
    nuevo_nombre = input(f"Nuevo nombre [{datos_actuales['nombre']}]: ").strip().upper()
    nuevo_telefono = input(f"Nuevo teléfono [{datos_actuales['telefono']}]: ").strip()
    nuevo_mail = input(f"Nuevo mail [{datos_actuales['mail']}]: ").strip().upper()
    nuevo_estado = input(f"¿Vigente? (S/N) [{datos_actuales['vigencia']}]: ").strip().upper()

    # Si el usuario escribió algo, actualizamos la llave correspondiente
    if nuevo_nombre != "":
        datos_actuales["nombre"] = nuevo_nombre
    if nuevo_telefono != "":
        datos_actuales["telefono"] = nuevo_telefono
    if nuevo_mail != "":
        datos_actuales["mail"] = nuevo_mail
    if nuevo_estado == "S" or nuevo_estado == "N":
        datos_actuales["vigencia"] = nuevo_estado

    # Guardamos el diccionario modificado de vuelta
    clientes[rut] = datos_actuales
    print("¡Datos del cliente actualizados correctamente!")


def eliminar_cliente():
    """ Borra un cliente del sistema y libera automáticamente sus reservas """
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


def menu_clientes_pb():
    """ Submenú integrador para las opciones de modificación y eliminación """
    while True:
        print()
        print("<|==-- Modificar y Eliminar Clientes --==|>")
        print("1) Modificar datos de cliente\n2) Eliminar cliente de la base de datos\n3) Salir al menú principal")
        try:
            opc = int(input(":"))
        except ValueError:
            print("Por favor, ingrese un número válido.")
            continue
            
        if opc == 1:
            modificar_cliente()
        elif opc == 2:
            eliminar_cliente()
        elif opc == 3:
            break


# =============================================================================
# CRISTIAN - MÓDULO DE GESTIÓN DE RESERVAS:
# Funciones para reservar, modificar, eliminar y listar reservas.
# =============================================================================

def reservar_asientos():
    """ Gestiona el proceso de reserva de asientos para los clientes """
    print("\n--- RESERVAR ASIENTOS ---")
    rut = input("Ingrese el RUT del cliente que reserva: ").strip().upper()

    # 1. Filtro de seguridad: ¿Existe el cliente?
    if rut not in clientes:
        print("Error: El cliente no está registrado. Debe crearlo primero.")
        return

    # 2. Filtro de seguridad: ¿Está vigente?
    datos_cliente = clientes[rut]
    if datos_cliente["vigencia"] != "S":
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
        if num_asiento < 1 or num_asiento > total_de_asientos:
            print("Error: Ese número de asiento no existe en la sala.")
            continue

        # 4. Filtro: ¿Alguien más ya compró este asiento?
        ya_ocupado = False
        for lista_asientos in reservas.values():
            if num_asiento in lista_asientos:
                ya_ocupado = True
                
        if ya_ocupado:
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
    """ Permite liberar asientos anteriores y reasignar nuevos """
    print("\n--- MODIFICAR RESERVA ---")
    rut = input("Ingrese el RUT del cliente para modificar su reserva: ").strip().upper()

    if rut not in clientes or rut not in reservas or len(reservas[rut]) == 0:
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
            
        if num_asiento < 1 or num_asiento > total_de_asientos:
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


def eliminar_reserva():
    """ Elimina la clave del cliente en el diccionario de reservas """
    print("\n--- ELIMINAR RESERVA ---")
    rut = input("Ingrese el RUT del cliente para cancelar su reserva: ").strip().upper()

    if rut not in reservas:
        print("Este cliente no tiene ninguna reserva registrada.")
        return

    del reservas[rut]
    print("¡La reserva ha sido eliminada y los asientos vuelven a estar disponibles!")


def listar_reservas():
    """ Muestra todas las reservas cruzando el RUT con el diccionario de Clientes """
    print("\n--- LISTADO DE RESERVAS ACTIVAS ---")
    
    if len(reservas) == 0:
        print("No hay ninguna reserva registrada en el cine.")
        return

    for rut, lista_asientos in reservas.items():
        # Buscamos el nombre del cliente usando la clave semántica (ahora en minúsculas)
        nombre_cliente = clientes[rut]["nombre"] 
        print(f"RUT: {rut} | Nombre: {nombre_cliente} | Asientos Reservados: {lista_asientos}")


# =============================================================================
# MENÚ PRINCIPAL - CRUD SEPARADO
# =============================================================================

def menu_clientes():
    """Menú CRUD: 1-Ingresar, 2-Listar, 3-Modificar, 4-Eliminar, 5-Volver."""
    while True:
        print()
        print("<|==-- Gestión de Clientes (CRUD) --==|>")
        print("1) Ingresar cliente")
        print("2) Listar clientes")
        print("3) Modificar cliente")
        print("4) Eliminar cliente")
        print("5) Volver al menú principal")
        try:
            opc = int(input(":"))
        except ValueError:
            print("Por favor, ingrese un número válido.")
            continue

        if opc == 1:
            crear_user_menu()
        elif opc == 2:
            if len(clientes) == 0:
                print("No hay clientes registrados.")
            else:
                for rut, datos in clientes.items():
                    print("|== Clientes registrados ==|")
                    print(f"Rut: {rut} | Datos: {datos} ")
        elif opc == 3:
            modificar_cliente()
        elif opc == 4:
            eliminar_cliente()
        elif opc == 5:
            break


def menu_principal():
    """ Orquestador principal que une todos los módulos funcionales """
    while True:
        print("\n" + "="*40)
        print("     SISTEMA DE RESERVAS CINE")
        print("="*40)
        print("1. Gestión de Clientes (CRUD)")
        print("2. Reservar Asientos")
        print("3. Modificar Reserva")
        print("4. Eliminar Reserva")
        print("5. Listar Reservas Activas")
        print("6. Visualizar Sala de Cine")
        print("0. Salir del Sistema")
        print("="*40)
        
        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("Error: Por favor, ingrese un número válido.")
            continue
            
        if opcion == 1:
            menu_clientes()
        elif opcion == 2:
            reservar_asientos()
        elif opcion == 3:
            modificar_reserva()
        elif opcion == 4:
            eliminar_reserva()
        elif opcion == 5:
            listar_reservas()
        elif opcion == 6:
            mostrar_sala()
        elif opcion == 0:
            print("¡Gracias por utilizar el sistema de cine unificado! Saliendo...")
            break
        else:
            print("Opción inválida. Intente un número del menú.")
# Ejecución del programa
if __name__ == "__main__":
    menu_principal()