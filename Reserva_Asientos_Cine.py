import re # Importamos el módulo re para validar el formato del RUT

FILAS = 5
COLUMNAS = 8

clientes = {}
reservas = {}
asientos = {numero: None for numero in range(1, FILAS * COLUMNAS + 1)}


def limpiar_pantalla():
    print("\n" * 2)


def validar_rut(rut): # Función para validar el formato del RUT
    rut = rut.strip().upper() # Limpiamos espacios y convertimos a mayúsculas para estandarizar
    if not rut:
        return None 
    rut = rut.replace(".", "") # Eliminamos puntos si el usuario los ingresa
    if re.fullmatch(r"\d{7,8}-[0-9K]", rut) or re.fullmatch(r"\d{7,8}", rut):
        return rut
    return None


def input_rut(prompt="Ingrese RUT: "): # Función para solicitar el RUT al usuario y validar su formato
    while True:
        rut = input(prompt).strip()
        rut_valido = validar_rut(rut)
        if rut_valido:
            return rut_valido
        print("RUT inválido. Debe tener 7 u 8 dígitos, opcionalmente con guion y dígito verificador.")


def validar_mail(mail):
    mail = mail.strip()
    if not mail:
        return None
    if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", mail):
        return mail
    return None


def input_mail(prompt="Ingrese mail: "):
    while True:
        mail = input(prompt).strip()
        mail_valido = validar_mail(mail)
        if mail_valido:
            return mail_valido
        print("Mail inválido. Ingrese una dirección con formato correcto.")


def input_vigencia(prompt="¿Cliente vigente? (S/N): "):
    while True:
        valor = input(prompt).strip().upper()
        if valor in ["S", "N"]:
            return valor == "S"
        print("Respuesta inválida. Ingrese S para sí o N para no.")


def mostrar_sala(): # Función para mostrar el estado actual de la sala de cine en formato de lista de listas
    print("\n--- Sala de Cine ---\n")
    for fila in range(FILAS):
        linea = []
        for columna in range(COLUMNAS):
            numero = fila * COLUMNAS + columna + 1
            if asientos[numero] is not None:
                linea.append("[XX]")
            else:
                linea.append(f"[{numero:02d}]")
        print(" ".join(linea))
    print("\nXX = Asiento reservado")


def listar_clientes(): # Función para listar todos los clientes registrados en el sistema, mostrando su RUT, nombre y teléfono
    if not clientes:
        print("No hay clientes registrados.")
        return
    print("\nClientes registrados:")
    for rut, datos in clientes.items():
        estado_vigencia = "Vigente" if datos.get("vigencia") else "No vigente"
        print(f"- RUT: {rut} | Nombre: {datos['nombre']} | Teléfono: {datos['telefono']} | Mail: {datos['mail']} | {estado_vigencia}")


def crear_cliente(): #
    print("\nCrear cliente")
    rut = input_rut()
    if rut in clientes:
        print("Ya existe un cliente con ese RUT.")
        return
    nombre = input("Nombre completo: ").strip()
    telefono = input("Teléfono: ").strip()
    mail = input_mail()
    vigencia = input_vigencia()
    if not nombre:
        print("El nombre no puede estar vacío.")
        return
    clientes[rut] = {"nombre": nombre, "telefono": telefono, "mail": mail, "vigencia": vigencia}
    print("Cliente creado correctamente.")


def actualizar_cliente(): # Función para modificar los datos de un cliente existente, permitiendo cambiar su nombre y teléfono
    print("\nModificar cliente")
    rut = input_rut()
    if rut not in clientes:
        print("Cliente no encontrado.")
        return
    nombre = input(f"Nuevo nombre ({clientes[rut]['nombre']}): ").strip()
    telefono = input(f"Nuevo teléfono ({clientes[rut]['telefono']}): ").strip()
    mail = input(f"Nuevo mail ({clientes[rut]['mail']}): ").strip()
    vigencia_input = input(f"Cliente vigente? (S/N) ({'S' if clientes[rut]['vigencia'] else 'N'}): ").strip().upper()
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


def eliminar_cliente(): # Función para eliminar un cliente del sistema y sus reservas asociadas
    print("\nEliminar cliente")
    rut = input_rut()
    if rut not in clientes:
        print("Cliente no encontrado.")
        return
    if rut in reservas and reservas[rut]:
        for numero in reservas[rut]:
            asientos[numero] = None
        del reservas[rut]
    del clientes[rut]
    print("Cliente y reservas asociadas eliminados correctamente.")

def pedir_asientos_disponibles(): # Función para solicitar al usuario que ingrese los números de los asientos que desea reservar, validando que existan y estén disponibles
    while True:
        raw = input("Ingrese asientos separados por comas (ej. 1,2,3): ").strip()
        if not raw:
            print("Debe ingresar al menos un asiento.")
            continue
        codigos = [asiento.strip() for asiento in raw.split(",") if asiento.strip()]
        if not codigos:
            print("Entrada inválida.")
            continue
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
            if asientos[numero] is not None:
                print(f"Asiento ocupado: {numero}")
                invalido = True
                break
            if numero in validos:
                print(f"Asiento duplicado en la selección: {numero}")
                invalido = True
                break
            validos.append(numero)
        if not invalido:
            return validos

# Gestión de Reservas: Funciones para reservar asientos, mostrar reservas por RUT, listar todas las reservas, modificar reservas y eliminar reservas, interactuando con el sistema de clientes y el estado de la sala para mantener la coherencia de los datos.
def reservar_asientos(): # Función para reservar asientos para un cliente, solicitando su RUT y los números de los asientos que desea reservar
    print("\nReservar asientos")
    rut = input_rut()
    if rut not in clientes: # Verificamos que el cliente esté registrado antes de permitir la reserva
        print("Cliente no está registrado. Deebe registrarse antes de reservar.")
        return
    if not clientes[rut]["vigencia"]: # Verificamos que el cliente esté vigente antes de permitir la reserva
        print("Cliente no vigente. No se puede realizar la reserva.")
        return
    mostrar_sala()
    codigos = pedir_asientos_disponibles()
    for codigo in codigos:
        asientos[codigo] = rut
    reservas.setdefault(rut, []).extend(codigos)
    print(f"Reserva realizada para {clientes[rut]['nombre']}. Asientos: {', '.join(str(numero) for numero in codigos)}")


def mostrar_reserva_por_rut(): # Función para mostrar los asientos reservados por un cliente específico, solicitando su RUT y mostrando los números de los asientos que tiene reservados
    rut = input_rut()
    if rut not in clientes:
        print("Cliente no registrado.")
        return
    if rut not in reservas or not reservas[rut]:
        print("No tiene reservas activas.")
        return
    print(f"Reservas del cliente {clientes[rut]['nombre']}:")
    print(", ".join(str(numero) for numero in sorted(reservas[rut])))


def listar_reservas(): # Función para mostrar todas las reservas activas
    if not reservas or all(not asientos_reservados for asientos_reservados in reservas.values()):
        print("No hay reservas activas.")
        return
    print("\nReservas activas:")
    for rut, asientos_reservados in reservas.items():
        if not asientos_reservados:
            continue
        nombre = clientes.get(rut, {}).get("nombre", "Desconocido")
        asientos_texto = ", ".join(str(numero) for numero in sorted(asientos_reservados))
        print(f"- RUT: {rut} | Nombre: {nombre} | Asientos: {asientos_texto}")


def modificar_reserva(): # Función para modificar una reserva existente, permitiendo al cliente agregar o eliminar asientos de su reserva actual, y actualizando el estado de la sala y las reservas del cliente en el sistema
    print("\nModificar reserva por RUT")
    rut = input_rut()
    if rut not in clientes:
        print("Cliente no registrado.")
        return
    if rut not in reservas or not reservas[rut]:
        print("No tiene reservas activas para modificar.")
        return
    actuales = reservas[rut]
    print(f"Reservas actuales: {', '.join(str(numero) for numero in sorted(actuales))}")
    mostrar_sala()

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
            return
        for numero in validos:
            if numero not in actuales:
                asientos[numero] = rut
                actuales.append(numero)

    entrada_quitar = input("Ingrese asientos a eliminar de su reserva separados por comas (o deje vacío para mantenerlos): ").strip()
    if entrada_quitar:
        codigos = [asiento.strip() for asiento in entrada_quitar.split(",") if asiento.strip()]
        invalidos = []
        for texto in codigos:
            if not texto.isdigit() or int(texto) not in actuales:
                invalidos.append(texto)
        if invalidos:
            print(f"Estos asientos no están en su reserva: {', '.join(invalidos)}")
            return
        for texto in codigos:
            numero = int(texto)
            asientos[numero] = None
            actuales.remove(numero)

    reservas[rut] = actuales
    print(f"Reserva modificada. Asientos actuales: {', '.join(str(numero) for numero in sorted(actuales))}")


def eliminar_reserva(): # Función para eliminar completamente una reserva, solicitando el RUT del cliente y eliminando todos los asientos reservados por ese cliente, actualizando el estado de la sala y las reservas del cliente en el sistema
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
        asientos[codigo] = None
    reservas[rut] = []
    print("Reserva eliminada correctamente.")


def menu_principal(): # Función para mostrar el menú principal del sistema de reservas, permitiendo al usuario seleccionar las diferentes opciones disponibles para gestionar clientes y reservas
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


def main(): # Función principal que ejecuta el programa, mostrando el menú y gestionando las opciones seleccionadas por el usuario para interactuar con el sistema de reservas
    while True:
        menu_principal()
        opcion = input("Seleccione una opción: ").strip()
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
            break
        else:
            print("Opción inválida, intente de nuevo.")


if __name__ == "__main__":
    main()
