import re # Importamos el módulo re para validar el formato del RUT

FILAS = ["A", "B", "C", "D", "E"]
COLUMNAS = list(range(1, 9))

clientes = {}
reservas = {}
asientos = {f"{fila}{columna}": None for fila in FILAS for columna in COLUMNAS}


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


def mostrar_sala(): # Función para mostrar el estado actual de la sala de cine, indicando qué asientos están libres y cuáles están reservados
    print("\nEstado de la sala de cine:")
    encabezado = "    " + "  ".join(str(col).rjust(2) for col in COLUMNAS)
    print(encabezado)
    for fila in FILAS:
        linea = [fila]
        for columna in COLUMNAS:
            codigo = f"{fila}{columna}"
            linea.append(" X" if asientos[codigo] else " O")
        print(" ".join(element.rjust(2) for element in linea))
    print("\nLeyenda: O = libre, X = reservado")


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


def eliminar_cliente(): # Función para eliminar un cliente del sistema, asegurándose de que no tenga reservas activas antes de permitir la eliminación    
    print("\nEliminar cliente")
    rut = input_rut()
    if rut not in clientes:
        print("Cliente no encontrado.")
        return
    if rut in reservas and reservas[rut]:
        print("No se puede eliminar el cliente porque tiene reservas activas.")
        return
    del clientes[rut]
    print("Cliente eliminado correctamente.")


def pedir_asientos_disponibles(): # Función para solicitar al usuario que ingrese los códigos de los asientos que desea reservar, validando que existan y estén disponibles
    while True:
        raw = input("Ingrese asientos separados por comas (ej. A1,B2): ").strip().upper()
        if not raw:
            print("Debe ingresar al menos un asiento.")
            continue
        codigos = [asiento.strip() for asiento in raw.split(",") if asiento.strip()]
        if not codigos:
            print("Entrada inválida.")
            continue
        validos = []
        invalido = False
        for codigo in codigos:
            if codigo not in asientos:
                print(f"Asiento inválido: {codigo}")
                invalido = True
                break
            if asientos[codigo] is not None:
                print(f"Asiento ocupado: {codigo}")
                invalido = True
                break
            if codigo in validos:
                print(f"Asiento duplicado en la selección: {codigo}")
                invalido = True
                break
            validos.append(codigo)
        if not invalido:
            return validos


def reservar_asientos(): # Función para reservar asientos para un cliente, solicitando su RUT y los códigos de los asientos que desea reservar, y actualizando el estado de la sala y las reservas del cliente en el sistema
    print("\nReservar asientos")
    rut = input_rut()
    if rut not in clientes:
        print("Cliente no está registrado. Registre el cliente antes de reservar.")
        return
    mostrar_sala()
    codigos = pedir_asientos_disponibles()
    for codigo in codigos:
        asientos[codigo] = rut
    reservas.setdefault(rut, []).extend(codigos)
    print(f"Reserva realizada para {clientes[rut]['nombre']}. Asientos: {', '.join(codigos)}")


def mostrar_reserva_por_rut(): # Función para mostrar los asientos reservados por un cliente específico, solicitando su RUT y mostrando los códigos de los asientos que tiene reservados
    rut = input_rut()
    if rut not in clientes:
        print("Cliente no registrado.")
        return
    if rut not in reservas or not reservas[rut]:
        print("No tiene reservas activas.")
        return
    print(f"Reservas del cliente {clientes[rut]['nombre']}:")
    print(", ".join(reservas[rut]))


def modificar_reserva(): # Función para modificar una reserva existente, permitiendo al cliente agregar o eliminar asientos de su reserva actual, y actualizando el estado de la sala y las reservas del cliente en el sistema
    print("\nModificar reserva por RUT")
    rut = input_rut()
    if rut not in clientes:
        print("Cliente no registrado.")
        return
    if rut not in reservas or not reservas[rut]:
        print("No tiene reservas activas para modificar.")
        return
    print(f"Reservas actuales: {', '.join(reservas[rut])}")
    opcion = input("Desea [A]gregar o [E]liminar asientos? ").strip().upper()
    if opcion == "A":
        mostrar_sala()
        nuevos = pedir_asientos_disponibles()
        for codigo in nuevos:
            asientos[codigo] = rut
        reservas[rut].extend(nuevos)
        print(f"Se agregaron los asientos: {', '.join(nuevos)}")
    elif opcion == "E":
        while True:
            salida = input("Ingrese el/los asientos a eliminar separados por comas: ").strip().upper()
            if not salida:
                print("Debe ingresar al menos un asiento.")
                continue
            codigos = [asiento.strip() for asiento in salida.split(",") if asiento.strip()]
            invalidos = [c for c in codigos if c not in reservas.get(rut, [])]
            if invalidos:
                print(f"Estos asientos no están en su reserva: {', '.join(invalidos)}")
                continue
            for codigo in codigos:
                asientos[codigo] = None
                reservas[rut].remove(codigo)
            print(f"Asientos eliminados: {', '.join(codigos)}")
            break
    else:
        print("Opción inválida. Sólo A o E.")


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
    print("\n=== Sistema de Reservas de Sala de Cine ===")
    print("1. Crear cliente")
    print("2. Listar clientes")
    print("3. Modificar cliente")
    print("4. Eliminar cliente")
    print("5. Mostrar sala")
    print("6. Reservar asientos")
    print("7. Mostrar reserva por RUT")
    print("8. Modificar reserva por RUT")
    print("9. Eliminar reserva por RUT")
    print("0. Salir")


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
            mostrar_sala()
        elif opcion == "6":
            reservar_asientos()
        elif opcion == "7":
            mostrar_reserva_por_rut()
        elif opcion == "8":
            modificar_reserva()
        elif opcion == "9":
            eliminar_reserva()
        elif opcion == "0":
            print("Gracias por usar el sistema de reservas. Hasta luego.")
            break
        else:
            print("Opción inválida, intente de nuevo.")


if __name__ == "__main__":
    main()
