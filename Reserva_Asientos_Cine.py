# ==========================================
# IMPORTACIÓN DE MÓDULOS
# ==========================================
import re # Importamos el módulo de Expresiones Regulares ('re') para buscar y validar patrones de texto (RUT y Mail)

# ==========================================
# CONSTANTES GLOBALES (Variables que no cambian)
# ==========================================
FILAS = 5       # Número de filas de la sala de cine
COLUMNAS = 8    # Número de columnas de la sala de cine

# ==========================================
# ESTRUCTURAS DE DATOS GLOBALES (Bases de datos en memoria)
# ==========================================
clientes = {}  # Diccionario vacío para almacenar clientes. Clave: RUT -> Valor: Diccionario con sus datos (nombre, mail, etc.)
reservas = {}  # Diccionario vacío para las reservas. Clave: RUT -> Valor: Lista con los números de asientos reservados

# 'asientos' es un diccionario generado por "comprensión de diccionarios" (dictionary comprehension).
# Genera parejas clave:valor automáticamente. Ejemplo: {1: None, 2: None, ..., 40: None}
# range(1, 41) va desde el número 1 hasta el 40 (el límite superior 41 es exclusivo, no se incluye).
asientos = {numero: None for numero in range(1, FILAS * COLUMNAS + 1)}


# ==========================================
# FUNCIONES DE UTILIDAD Y VALIDACIÓN
# ==========================================

def limpiar_pantalla():
    """Imprime saltos de línea para simular una limpieza visual de la consola."""
    print("\n" * 2) # Multiplica el string de salto de línea para imprimirlo dos veces


def validar_rut(rut):
    """Valida que el string ingresado cumpla con el formato de un RUT chileno (sin puntos y con guion)."""
    # .strip() elimina espacios en blanco al inicio y final. .upper() convierte las letras (como la 'k') a mayúsculas.
    rut = rut.strip().upper() 
    
    # Si el usuario no ingresó nada (string vacío), retorna None (indica que no es válido)
    if not rut:
        return None 
    
    # .replace(".", "") busca todos los puntos del string y los elimina reemplazándolos por nada
    rut = rut.replace(".", "") 
    
    # re.fullmatch comprueba si TODO el string calza perfectamente con el patrón dado (Expresión Regular)
    # Patrón 1: r"\d{7,8}-[0-9K]" -> 7 u 8 dígitos numéricos, un guion obligatorio, y un dígito del 0 al 9 o una K.
    # Patrón 2: r"\d{7,8}" -> Solo 7 u 8 dígitos numéricos (por si lo ingresan sin guion).
    if re.fullmatch(r"\d{7,8}-[0-9K]", rut) or re.fullmatch(r"\d{7,8}", rut):
        return rut # Si calza con algún patrón, el RUT es válido y se retorna limpio
    return None    # Si no calza, retorna None


def input_rut(prompt="Ingrese RUT: "):
    """Ciclo interactivo que solicita el RUT por teclado hasta que sea válido."""
    while True: # Bucle infinito que solo se romperá cuando se ejecute un 'return'
        rut = input(prompt).strip() # Solicita el dato y limpia espacios extremos
        rut_valido = validar_rut(rut) # Llama a la función de validación anterior
        if rut_valido:
            return rut_valido # Rompe el ciclo y devuelve el RUT validado
        # Si validar_rut devolvió None, el ciclo continúa y muestra el error:
        print("RUT inválido. Debe tener 7 u 8 dígitos, opcionalmente con guion y dígito verificador.")


def validar_mail(mail):
    """Valida si un correo electrónico tiene una estructura básica aceptable (texto@texto.texto)."""
    mail = mail.strip() # Limpia espacios extras
    if not mail:
        return None
    # Expresión regular: 
    # [^@\s]+ -> Uno o más caracteres que NO sean arroba ni espacios
    # @       -> Un arroba obligatorio
    # \.[^@\s]+ -> Un punto obligatorio seguido de caracteres que no sean arroba ni espacios
    if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", mail):
        return mail
    return None


def input_mail(prompt="Ingrese mail: "):
    """Ciclo interactivo que solicita el mail hasta que cumpla el formato correcto."""
    while True:
        mail = input(prompt).strip()
        mail_valido = validar_mail(mail)
        if mail_valido:
            return mail_valido
        print("Mail inválido. Ingrese una dirección con formato correcto.")


def input_vigencia(prompt="¿Cliente vigente? (S/N): "):
    """Solicita una confirmación de tipo Sí o No y la transforma en un valor Booleano (True/False)."""
    while True:
        valor = input(prompt).strip().upper() # Convierte la respuesta a mayúsculas para aceptar 's' o 'S'
        if valor in ["S", "N"]: # Verifica si la respuesta es una de las opciones válidas en la lista
            return valor == "S" # Retorna True si valor es "S", o False si valor es "N"
        print("Respuesta inválida. Ingrese S para sí o N para no.")


# ==========================================
# GESTIÓN DE SALA (VISTA)
# ==========================================

def mostrar_sala():
    """Dibuja en pantalla la matriz de asientos de la sala de cine."""
    print("\n--- Sala de Cine ---\n")
    for fila in range(FILAS): # Itera desde 0 hasta FILAS-1 (0 a 4)
        linea = [] # Lista temporal para construir el texto de la fila actual
        for columna in range(COLUMNAS): # Itera desde 0 hasta COLUMNAS-1 (0 a 7)
            # Calcula el número del asiento actual basado en la fila y columna (Fórmula de matriz a vector indexado en 1)
            numero = fila * COLUMNAS + columna + 1
            
            # Si el asiento tiene asignado un RUT (no es None), significa que está ocupado
            if asientos[numero] is not None:
                linea.append("[XX]") # Agrega indicador de ocupado a la línea
            else:
                # f"[{numero:02d}]" -> Formatea el número para que siempre ocupe 2 dígitos (ej: el 5 pasa a ser '05')
                linea.append(f"[{numero:02d}]") 
        
        # .join une todos los elementos de la lista 'linea' en un solo string, separados por un espacio.
        print(" ".join(linea)) 
    print("\nXX = Asiento reservado")


# ==========================================
# GESTIÓN DE CLIENTES (CRUD)
# ==========================================

def listar_clientes():
    """Muestra en formato de lista todos los clientes almacenados en el sistema."""
    if not clientes: # Si el diccionario 'clientes' está vacío, evalúa a True
        print("No hay clientes registrados.")
        return # Termina la función de forma anticipada
        
    print("\nClientes registrados:")
    # .items() devuelve parejas (clave, valor). En este caso: rut (clave) y datos (diccionario de datos)
    for rut, datos in clientes.items():
        # Operador ternario: asigna "Vigente" si datos['vigencia'] es True, de lo contrario asigna "No vigente"
        # .get("vigencia") busca la clave de forma segura en el diccionario de datos del cliente
        estado_vigencia = "Vigente" if datos.get("vigencia") else "No vigente"
        print(f"- RUT: {rut} | Nombre: {datos['nombre']} | Teléfono: {datos['telefono']} | Mail: {datos['mail']} | {estado_vigencia}")


def crear_cliente():
    """Registra un nuevo cliente pidiendo sus datos por consola."""
    print("\nCrear cliente")
    rut = input_rut() # Solicita y valida el RUT
    
    # Verifica si el RUT ya existe como clave en el diccionario de clientes
    if rut in clientes:
        print("Ya existe un cliente con ese RUT.")
        return # Cancela la creación
        
    nombre = input("Nombre completo: ").strip()
    telefono = input("Teléfono: ").strip()
    mail = input_mail()
    vigencia = input_vigencia()
    
    if not nombre: # Validación básica para evitar strings vacíos
        print("El nombre no puede estar vacío.")
        return
        
    # Agrega el cliente usando el RUT como clave, y asignando un sub-diccionario con sus propiedades
    clientes[rut] = {"nombre": nombre, "telefono": telefono, "mail": mail, "vigencia": vigencia}
    print("Cliente creado correctamente.")


def actualizar_cliente():
    """Modifica los datos de un cliente existente. Si se deja en blanco, mantiene el dato anterior."""
    print("\nModificar cliente")
    rut = input_rut()
    
    if rut not in clientes:
        print("Cliente no encontrado.")
        return
        
    # Muestra el valor actual entre paréntesis para guiar al usuario
    nombre = input(f"Nuevo nombre ({clientes[rut]['nombre']}): ").strip()
    telefono = input(f"Nuevo teléfono ({clientes[rut]['telefono']}): ").strip()
    mail = input(f"Nuevo mail ({clientes[rut]['mail']}): ").strip()
    vigencia_input = input(f"Cliente vigente? (S/N) ({'S' if clientes[rut]['vigencia'] else 'N'}): ").strip().upper()
    
    # Si el usuario escribió algo (no es un string vacío), actualiza la información en el diccionario
    if nombre:
        clientes[rut]["nombre"] = nombre
    if telefono:
        clientes[rut]["telefono"] = telefono
    if mail:
        mail_valido = validar_mail(mail)
        if mail_valido:
            clientes[rut]["mail"] = mail_valido
        else:
            print("Mail inválido, se mantiene el valor anterior.")
    if vigencia_input in ["S", "N"]:
        clientes[rut]["vigencia"] = vigencia_input == "S"
        
    print("Cliente actualizado correctamente.")


def eliminar_cliente():
    """Elimina a un cliente del sistema y libera automáticamente los asientos que tenía reservados."""
    print("\nEliminar cliente")
    rut = input_rut()
    
    if rut not in clientes:
        print("Cliente no encontrado.")
        return
        
    # Si el cliente tiene registros en el diccionario de reservas y la lista de reservas no está vacía:
    if rut in reservas and reservas[rut]:
        for numero in reservas[rut]: # Itera por cada número de asiento que el cliente tenía reservado
            asientos[numero] = None  # Libera el asiento en la sala poniéndolo en None
        del reservas[rut]            # Elimina la clave del cliente del diccionario de reservas usando 'del'
        
    del clientes[rut] # Elimina el registro del cliente del diccionario de clientes
    print("Cliente y reservas asociadas eliminados correctamente.")


# ==========================================
# GESTIÓN DE SELECCIÓN DE ASIENTOS
# ==========================================

def pedir_asientos_disponibles():
    """Pide una lista de asientos separados por comas y valida que cumplan los requisitos de disponibilidad."""
    while True:
        raw = input("Ingrese asientos separados por comas (ej. 1,2,3): ").strip()
        if not raw:
            print("Debe ingresar al menos un asiento.")
            continue # Salta el resto del bucle y vuelve a empezar el 'while'
            
        # Comprensión de listas: divide el string por las comas con .split(","), 
        # limpia los espacios de cada pedazo y descarta elementos vacíos.
        codigos = [asiento.strip() for asiento in raw.split(",") if asiento.strip()]
        
        if not codigos:
            print("Entrada inválida.")
            continue
            
        validos = []       # Lista para acumular los asientos que pasen todas las pruebas
        invalido = False   # Bandera (flag) para rastrear si encontramos algún error en la tanda de asientos
        
        for texto in codigos:
            # .isdigit() comprueba si el string contiene únicamente números enteros positivos
            if not texto.isdigit():
                print(f"Asiento inválido: {texto} (Debe ser un número)")
                invalido = True
                break # Rompe el bucle 'for' actual
                
            numero = int(texto) # Convierte el texto validado a un número entero real
            
            # Prueba 1: Verificar si el número de asiento existe en las claves de nuestro diccionario de la sala
            if numero not in asientos:
                print(f"Asiento inválido: {numero} (No existe en la sala)")
                invalido = True
                break
                
            # Prueba 2: Verificar si el asiento ya está ocupado (tiene un RUT guardado)
            if asientos[numero] is not None:
                print(f"Asiento ocupado: {numero}")
                invalido = True
                break
                
            # Prueba 3: Verificar que el usuario no haya escrito el mismo número dos veces en la misma línea
            if numero in validos:
                print(f"Asiento duplicado en la selección: {numero}")
                invalido = True
                break
                
            # Si pasa todas las pruebas, se añade a la lista temporal de asientos aprobados
            validos.append(numero)
            
        # Si la bandera 'invalido' sigue siendo False, significa que TODA la lista está perfecta
        if not invalido:
            return validos # Retorna la lista de enteros y termina la función


# ==========================================
# GESTIÓN DE RESERVAS
# ==========================================

def reservar_asientos():
    """Asocia asientos disponibles a un cliente registrado y vigente."""
    print("\nReservar asientos")
    rut = input_rut() 
    
    if rut not in clientes: 
        print("Cliente no está registrado. Debe registrarse antes de reservar.")
        return 
        
    if not clientes[rut]["vigencia"]: 
        print("Cliente no vigente. No se puede realizar la reserva.")
        return 
        
    mostrar_sala() # Le muestra la sala al usuario para que vea cuáles están libres
    codigos = pedir_asientos_disponibles() # Obtiene la lista de números enteros validados
    
    for codigo in codigos: 
        asientos[codigo] = rut # En el mapa de la sala, asigna el RUT del cliente a ese asiento
        
    # .setdefault(rut, []) busca la clave 'rut'. Si no existe, la crea con una lista vacía [] como valor por defecto.
    # Luego, .extend(codigos) añade todos los elementos de la lista 'codigos' al final de esa lista de reservas.
    reservas.setdefault(rut, []).extend(codigos) 
    
    # Muestra un mensaje de éxito transformando cada número entero a string mediante un generador, para poder unirlos con comas
    print(f"Reserva realizada para {clientes[rut]['nombre']}. Asientos: {', '.join(str(numero) for numero in codigos)}")


def mostrar_reserva_por_rut():
    """Busca y despliega los asientos reservados de un cliente específico."""
    rut = input_rut() 
    if rut not in clientes: 
        print("Cliente no registrado.")
        return
    if rut not in reservas or not reservas[rut]: 
        print("No tiene reservas activas.")
        return
        
    print(f"Reservas del cliente {clientes[rut]['nombre']}:")
    # sorted(reservas[rut]) ordena de menor a mayor los números de asiento antes de imprimirlos
    print(", ".join(str(numero) for numero in sorted(reservas[rut])))


def listar_reservas():
    """Muestra todas las reservas del cine emparejando los RUT con los nombres de los clientes."""
    # all(...) es una función que devuelve True si absolutamente todas las condiciones internas se cumplen.
    # Aquí verifica si todas las listas de asientos guardadas en reservas.values() están vacías.
    if not reservas or all(not asientos_reservados for asientos_reservados in reservas.values()): 
        print("No hay reservas activas.")
        return
        
    print("\nReservas activas:")
    for rut, asientos_reservados in reservas.items(): 
        if not asientos_reservados: # Si la lista de asientos de este cliente quedó vacía, se la salta
            continue
            
        # .get(rut, {}) busca el RUT en clientes. Si no existe, devuelve un diccionario vacío para evitar que se caiga el programa.
        # El segundo .get("nombre", "Desconocido") busca el nombre dentro de ese resultado.
        nombre = clientes.get(rut, {}).get("nombre", "Desconocido") 
        asientos_texto = ", ".join(str(numero) for numero in sorted(asientos_reservados))
        print(f"- RUT: {rut} | Nombre: {nombre} | Asientos: {asientos_texto}")


def modificar_reserva():
    """Permite añadir nuevos asientos o remover asientos de una reserva existente."""
    print("\nModificar reserva por RUT")
    rut = input_rut()
    if rut not in clientes:
        print("Cliente no registrado.")
        return
    if rut not in reservas or not reservas[rut]:
        print("No tiene reservas activas para modificar.")
        return
        
    actuales = reservas[rut] # Referencia directa a la lista de asientos actuales del cliente
    print(f"Reservas actuales: {', '.join(str(numero) for numero in sorted(actuales))}")
    mostrar_sala()

    # --- SECCIÓN PARA AGREGAR ---
    entrada_agregar = input("Ingrese asientos nuevos a agregar separados por comas (o deje vacío para no agregar): ").strip()
    if entrada_agregar:
        codigos = [asiento.strip() for asiento in entrada_agregar.split(",") if asiento.strip()]
        validos = []
        invalido = False
        for texto in codigos:
            if not texto.isdigit():
                print(f"Asiento inválido: {texto}")
                invalido = True
                break
            numero = int(texto)
            if numero not in asientos:
                print(f"Asiento inválido: {numero}")
                invalido = True
                break
            # Condición especial: Está ocupado si tiene un RUT asignado Y ese RUT NO pertenece al cliente actual
            if asientos[numero] is not None and asientos[numero] != rut:
                print(f"Asiento ocupado por otro cliente: {numero}")
                invalido = True
                break
            if numero in validos:
                print(f"Asiento duplicado en la selección: {numero}")
                invalido = True
                break
            validos.append(numero)
            
        if invalido:
            return # Cancela toda la operación si hubo algún error en la entrada
            
        for numero in validos:
            if numero not in actuales: # Si el usuario ingresó un asiento que ya tenía, simplemente lo ignora
                asientos[numero] = rut # Lo ocupa en la sala
                actuales.append(numero) # Lo añade a la lista del cliente

    # --- SECCIÓN PARA QUITAR ---
    entrada_quitar = input("Ingrese asientos a eliminar de su reserva separados por comas (o deje vacío para mantenerlos): ").strip()
    if entrada_quitar: 
        codigos = [asiento.strip() for asiento in entrada_quitar.split(",") if asiento.strip()]
        invalidos = []
        for texto in codigos:
            # Valida si no es un número o si intenta quitar un asiento que el cliente NO tiene reservado
            if not texto.isdigit() or int(texto) not in actuales:
                invalidos.append(texto)
                
        if invalidos:
            print(f"Estos asientos no están en su reserva: {', '.join(invalidos)}")
            return
            
        for texto in codigos:
            numero = int(texto)
            asientos[numero] = None # Libera el asiento en la sala
            actuales.remove(numero) # Remueve el elemento exacto de la lista mediante .remove()

    reservas[rut] = actuales # Guarda los cambios de vuelta en el diccionario de reservas
    print(f"Reserva modificada. Asientos actuales: {', '.join(str(numero) for numero in sorted(actuales))}")


def eliminar_reserva():
    """Libera de golpe todos los asientos de un cliente en particular, vaciando su lista de reservas."""
    print("\nEliminar reserva por RUT")
    rut = input_rut()
    if rut not in clientes:
        print("Cliente no registrado.")
        return
    if rut not in reservas or not reservas[rut]:
        print("No tiene reservas activas.")
        return
        
    confirmacion = input("¿Está seguro de eliminar toda la reserva? (S/N): ").strip().upper()
    if confirmacion != "S":
        print("Operación cancelada.")
        return
        
    for codigo in reservas[rut]:
        asientos[codigo] = None # Vacía cada asiento en la sala
    reservas[rut] = [] # Deja la lista del cliente vacía
    print("Reserva eliminada correctamente.")


# ==========================================
# MENÚ Y FLUJO PRINCIPAL
# ==========================================

def menu_principal():
    """Imprime el menú de opciones disponibles en la terminal."""
    print("\n====================================")
    print(" SISTEMA DE RESERVA DE CINE")
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


def main():
    """Controlador principal del programa. Ejecuta el bucle del menú y deriva la acción según el caso."""
    while True:
        menu_principal()
        opcion = input("Seleccione una opción: ").strip()
        
        # Estructura de control condicional clásica (if-elif-else) para actuar según la opción tipeada
        if opcion == "1":
            crear_cliente()
        elif opcion == "2":
            listar_clientes()
        elif opcion == "3":
            actualizar_cliente()
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
            print("Gracias por usar el sistema de reservas. Hasta luego.")
            break # Rompe el 'while True' saliendo de la función main y finalizando el programa
        else:
            print("Opción inválida, intente de nuevo.")


# Patrón estándar de Python. Comprueba si este archivo se está ejecutando directamente desde la consola.
# Si es así (__name__ toma el valor de "__main__"), arranca la ejecución llamando a la función main().
if __name__ == "__main__":
    main()