# ==============================================================================
# CONSTANTES GLOBALES (Configuración fija del cine)
# ==============================================================================
# Definimos el tamaño de la sala de cine como variables fijas.
FILAS = 5       
COLUMNAS = 8    

# ==============================================================================
# ESTRUCTURAS DE DATOS GLOBALES (Nuestra Base de Datos en memoria)
# ==============================================================================
# 'clientes' será un diccionario. 
# Clave: El RUT del cliente (ej: "12345678-9")
# Valor: Una lista con sus datos en orden fijo: [Nombre, Teléfono, Mail, Vigencia]
clientes = {}  

# 'reservas' será un diccionario para saber qué asientos tiene cada persona.
# Clave: El RUT del cliente.
# Valor: Una lista de números enteros con sus asientos (ej: [1, 2, 3])
reservas = {}  

# 'sala' será una LISTA DE LISTAS (Matriz).
# Al inicio, la creamos vacía y la llenaremos con los números de asiento del 1 al 40.
sala = []
contador_asiento = 1

# Usamos un ciclo para crear cada una de las 5 filas
for f in range(FILAS):
    fila_actual = [] # Creamos una lista vacía para la fila actual
    # Usamos otro ciclo para meter los 8 asientos en esa fila
    for c in range(COLUMNAS):
        fila_actual.append(contador_asiento) # Guardamos el número de asiento
        contador_asiento = contador_asiento + 1 # Incrementamos para el siguiente asiento
    sala.append(fila_actual) # Guardamos la fila completa dentro de la sala


# ==============================================================================
# FUNCIONES DE VISUALIZACIÓN
# ==============================================================================

def mostrar_sala():
    """
    Recorre la lista de listas 'sala' y la dibuja en la pantalla[cite: 51, 52].
    Si el asiento está reservado, en su lugar imprime [XX][cite: 55].
    """
    print("\n--- Sala de Cine ---")
    
    # Recorremos cada fila de la sala
    for fila in sala:
        linea_texto = "" # Aquí acumularemos los asientos de la fila para imprimirlos juntos
        
        # Recorremos cada asiento dentro de esa fila
        for asiento in fila:
            # Para saber si este asiento está ocupado, revisamos si su número
            # está dentro de alguna de las listas de asientos del diccionario 'reservas'.
            ocupado = False
            for lista_asientos in reservas.values():
                if asiento in lista_asientos:
                    ocupado = True
            
            # Si está ocupado, dibujamos [XX], si no, dibujamos el número formateado [cite: 55]
            if ocupado == True:
                linea_texto = linea_texto + "[XX] "
            else:
                # El truco de abajo añade un "0" al inicio si el número es menor a 10 (ej: 5 -> "05") [cite: 57]
                if asiento < 10:
                    linea_texto = linea_texto + "[0" + str(asiento) + "] "
                else:
                    linea_texto = linea_texto + "[" + str(asiento) + "] "
                    
        print(linea_texto) # Imprime la fila completa en una sola línea de la consola
    print("XX = Asiento reservado\n")


# ==============================================================================
# FUNCIONES DE GESTIÓN DE CLIENTES (CRUD) [cite: 14]
# ==============================================================================

def crear_cliente():
    """Solicita los datos del usuario y los guarda en el diccionario 'clientes'[cite: 15, 16]."""
    print("\n--- CREAR CLIENTE ---")
    rut = input("Ingrese RUT (con guion y sin puntos, ej: 12345678-K): ").strip().upper()
    
    # Validación básica: No dejar el RUT vacío 
    if rut == "":
        print("El RUT no puede estar vacío.")
        return # Con 'return' salimos inmediatamente de la función sin guardar nada
        
    # Regla: No permitir RUTs duplicados [cite: 23, 63]
    if rut in clientes:
        print("Error: Ya existe un cliente registrado con este RUT.")
        return

    # Pedimos el resto de datos utilizando .strip() para borrar espacios accidentales al inicio/final [cite: 82]
    nombre = input("Ingrese Nombre Completo: ").strip()
    telefono = input("Ingrese Teléfono: ").strip()
    mail = input("Ingrese Correo Electrónico: ").strip()
    
    # Validación de Vigencia (Bucle que insiste hasta que el usuario responda S o N) [cite: 22]
    while True:
        vigencia_input = input("¿El cliente está vigente? (S/N): ").strip().upper()
        if vigencia_input == "S" or vigencia_input == "N":
            break # Si es correcto, rompe el bucle 'while'
        print("Opción inválida. Escriba solo S o N.")

    # Guardamos los datos en el diccionario usando el RUT como la Clave [cite: 10]
    # El Valor será una lista con los 4 datos en orden
    clientes[rut] = [nombre, telefono, mail, vigencia_input]
    print("¡Cliente creado exitosamente!")


def listar_clientes():
    """Muestra en pantalla todos los clientes que están en el diccionario[cite: 24, 25]."""
    print("\n--- LISTA DE CLIENTES REGISTRADOS ---")
    
    # Si el diccionario está vacío, avisa al usuario
    if len(clientes) == 0:
        print("No hay clientes registrados en el sistema.")
        return

    # Recorremos el diccionario. 'rut' toma la clave y 'datos' toma la lista de valores
    for rut, datos in clientes.items():
        # Traducimos la "S" o "N" a algo más legible para la lista
        if datos[3] == "S":
            estado = "Vigente"
        else:
            estado = "No Vigente"
            
        print(f"RUT: {rut} | Nombre: {datos[0]} | Teléfono: {datos[1]} | Mail: {datos[2]} | Estado: {estado}")


def modificar_cliente():
    """Busca un cliente por RUT y permite cambiar sus datos uno por uno[cite: 26, 27]."""
    print("\n--- MODIFICAR CLIENTE ---")
    rut = input("Ingrese el RUT del cliente a modificar: ").strip().upper()

    # Validamos si el RUT existe en nuestra "base de datos"
    if rut not in clientes:
        print("El cliente con ese RUT no existe.")
        return

    # Obtenemos la lista actual de ese cliente para mostrar sus valores viejos
    datos_actuales = clientes[rut]

    print(f"Modificando a: {datos_actuales[0]}")
    print("(Presione ENTER si no desea cambiar el dato actual)")

    # Pedimos los nuevos datos
    nuevo_nombre = input(f"Nuevo nombre [{datos_actuales[0]}]: ").strip()
    nuevo_telefono = input(f"Nuevo teléfono [{datos_actuales[1]}]: ").strip()
    nuevo_mail = input(f"Nuevo mail [{datos_actuales[2]}]: ").strip()
    nuevo_estado = input(f"¿Vigente? (S/N) [{datos_actuales[3]}]: ").strip().upper()

    # Si el usuario escribió algo (no es un texto vacío ""), actualizamos la posición correspondiente
    if nuevo_nombre != "":
        datos_actuales[0] = nuevo_nombre
    if nuevo_telefono != "":
        datos_actuales[1] = nuevo_telefono
    if nuevo_mail != "":
        datos_actuales[2] = nuevo_mail
    if nuevo_estado == "S" or nuevo_estado == "N":
        datos_actuales[3] = nuevo_estado

    # Guardamos la lista modificada de vuelta en el diccionario
    clientes[rut] = datos_actuales
    print("¡Datos del cliente actualizados correctamente!")


def eliminar_cliente():
    """Borra un cliente del sistema y libera automáticamente sus reservas[cite: 28, 29, 30]."""
    print("\n--- ELIMINAR CLIENTE ---")
    rut = input("Ingrese el RUT del cliente a eliminar: ").strip().upper()

    if rut not in clientes:
        print("El cliente con ese RUT no existe.")
        return

    # Regla del enunciado: Al eliminar un cliente, se borran sus reservas [cite: 30, 71]
    if rut in reservas:
        del reservas[rut] # Borramos la clave del cliente en el diccionario de reservas
        print("-> Se han liberado los asientos que este cliente tenía reservados.")

    # Borramos al cliente de nuestro diccionario principal
    del clientes[rut]
    print("¡Cliente eliminado del sistema correctamente!")

# ==============================================================================
# MÓDULO DE CRISTIAN: GESTIÓN DE RESERVAS 
# ==============================================================================

    print("\n--- RESERVAR ASIENTOS ---")
def reservar_asientos():
        """
    Gestiona el proceso de reserva de asientos para los clientes.
    
    Aplica filtros de seguridad independientes para validar que el cliente exista,
    esté vigente y que los asientos seleccionados estén disponibles. 
    
    Implementa un "carrito temporal" mediante la lista 'asientos_a_reservar' 
    para acumular y validar las selecciones una a una, asegurando que la 
    reserva original no se modifique hasta que todo el proceso sea correcto.
    """
    rut = input("Ingrese el RUT del cliente que reserva: ").strip().upper()

    # 1. Filtro de seguridad: ¿Existe el cliente?
    if rut not in clientes:
        print("Error: El cliente no está registrado. Debe crearlo primero.")
        return

    # 2. Filtro de seguridad: ¿Está vigente?
    datos_cliente = clientes[rut]
    if datos_cliente[3] != "S":
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
    print("\n--- LISTADO DE RESERVAS ACTIVAS ---")
    
    if len(reservas) == 0:
        print("No hay ninguna reserva registrada en el cine.")
        return

    for rut, lista_asientos in reservas.items():
        # Buscamos el nombre del cliente en el otro diccionario usando su RUT
        nombre_cliente = clientes[rut][0] 
        print(f"RUT: {rut} | Nombre: {nombre_cliente} | Asientos Reservados: {lista_asientos}")

# FIN GESTIÓN DE RESERVAS

# ==============================================================================
# CONTROLADOR PRINCIPAL (Menú)
# ==============================================================================

def main():
    """Bucle principal que mantiene vivo el programa y gestiona las opciones de la consola[cite: 59, 72]."""
    while True:
        # Desplegamos el menú visual interactivo en la terminal [cite: 58, 61]
        print("====================================")
        print("    SISTEMA DE RESERVA DE CINE")
        print("====================================")
        print("1. Crear cliente")
        print("2. Listar clientes")
        print("3. Modificar cliente")
        print("4. Eliminar cliente")
        print("5. Reservar asientos")
        print("6. Modificar reserva")
        print("7. Eliminar reserva")
        print("8. Listar reservas")
        print("9. Imprimir sala")
        print("10. Salir")
        print("====================================")
        
        opcion = input("Seleccione una opción (1-10): ").strip() # [cite: 60, 82]
        
        # Evaluamos la opción elegida mediante condicionales básicos (if-elif-else) [cite: 80]
        if opcion == "1":
            crear_cliente()
        elif opcion == "2":
            listar_clientes()
        elif opcion == "3":
            modificar_cliente()
        elif opcion == "4":
            eliminar_cliente()
        elif opcion == "5":
            reservar_asientos()
        elif opcion == "6":
            modificar_reserva()
        elif opcion == "7":
            eliminar_reserva()
        elif opcion == "8":
            listar_reservas()
        elif opcion == "9":
            mostrar_sala()
        elif opcion == "10":
            print("Gracias por utilizar nuestro sistema de reservas. ¡Hasta luego!")
            break # Rompe el ciclo 'while True' infinito y el programa termina
        else:
            print("Opción inválida. Por favor, digite un número entre 1 y 10.\n")


# Este bloque asegura que el programa inicie de inmediato al ejecutar el archivo
if __name__ == "__main__":
    main()