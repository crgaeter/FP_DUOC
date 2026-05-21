# Diccionario: Sistema de Reservas de Cine G5

Este glosario contiene los métodos, funciones y palabras clave de Python utilizados en el sistema de gestión de reservas de cine. Ayuda a entender el código con términos profesionales.

---

## 1. Métodos para Textos (Strings)
Sirven para limpiar, transformar o validar lo que el usuario escribe por teclado antes de procesarlo.

| Recurso | Nombre Técnico | ¿Qué hace de forma simple? | Ejemplo real en el código |
| :--- | :--- | :--- | :--- |
| **`.strip()`** | Método de String | Borra los espacios en blanco accidentales que el usuario deja al principio o al final de un texto. | `input("...").strip()` *(Evita que guardemos un RUT con espacios invisibles como `" 1234 "`)* |
| **`.upper()`** | Método de String | Convierte todo el texto a **MAYÚSCULAS**. | `rut.upper()` *(Transforma `"12345678-k"` en `"12345678-K"` para estandarizar las búsquedas)* |
| **`.isdigit()`** | Método de String | Pregunta si el texto contiene **únicamente números enteros**. Devuelve `True` o `False`. | `entrada.isdigit()` *(Detecta si el usuario ingresó letras o símbolos en vez de un número de asiento)* |

---

## 2. Métodos para Listas y Diccionarios
Sirven para manipular las "bases de datos" en memoria (los diccionarios `clientes` y `reservas`, y las listas de asientos).

| Recurso | Nombre Técnico | ¿Qué hace de forma simple? | Ejemplo real en el código |
| :--- | :--- | :--- | :--- |
| **`.append()`** | Método de Lista | Agrega **un solo** elemento al final de una lista. | `asientos_a_reservar.append(num_asiento)` *(Mete un asiento seleccionado al "carrito temporal")* |
| **`.extend()`** | Método de Lista | Toma una lista completa y **la fusiona** al final de otra (agrega múltiples elementos a la vez). | `reservas[rut].extend(asientos_a_reservar)` *(Suma los asientos nuevos a los que el cliente ya tenía comprados)* |
| **`.values()`** | Método de Diccionario | Trae solo los **datos guardados** (valores) de un diccionario, ignorando por completo sus llaves (RUTs). | `for lista_asientos in reservas.values():` *(Lo usamos para revisar si un asiento ya está ocupado por cualquier otro cliente)* |
| **`.items()`** | Método de Diccionario | Trae las **parejas completas** (Llave y Valor) de un diccionario al mismo tiempo. | `for rut, lista_asientos in reservas.items():` *(Lo usamos para listar las reservas mostrando a quién le pertenece cada asiento)* |

---

## 3. Funciones Nativas y Comandos del Sistema
Son herramientas globales integradas directamente en el núcleo de Python.

| Recurso | Nombre Técnico | ¿Qué hace de forma simple? | Ejemplo real en el código |
| :--- | :--- | :--- | :--- |
| **`len()`** | Función (*Length*) | Cuenta **cuántos elementos** hay dentro de algo (letras en un texto, elementos en una lista o diccionario). | `if len(reservas) == 0:` *(Si el tamaño del diccionario es cero, significa que no hay ninguna reserva guardada)* |
| **`int()`** | Función | Intenta transformar un texto numérico en un **número matemático real** para poder hacer operaciones numéricas. | `num_asiento = int(entrada)` *(Pasa el texto `"5"` al número entero `5`)* |
| **`del`** | Palabra Clave | **Elimina por completo** una variable, un elemento de una lista o una llave dentro de un diccionario. | `del reservas[rut]` *(Borra la reserva del cliente, liberando sus asientos de forma automática)* |
| **`continue`** | Palabra Clave | Detiene la ejecución actual de un ciclo (`while` o `for`) y **vuelve inmediatamente al inicio** del mismo ciclo. | Se usa cuando el usuario comete un error, para saltarse el resto del código y obligarlo a ingresar el dato de nuevo. |
| **`break`** | Palabra Clave | **Rompe y cierra** el ciclo `while` por completo, permitiendo que el programa continúe con las líneas que estén más abajo. | `if num_asiento == 0: break` *(Termina el bucle de pedir asientos cuando el usuario presiona cero)* |

---

## 💡 Glosario Rápido de Conceptos Básicos
* **Función:** Una herramienta general e independiente a la que le pasas datos entre paréntesis para que realice una tarea (Ej: `int(texto)`).
* **Método:** Una función especial que le pertenece exclusivamente a un tipo de dato (como un texto o una lista) y se invoca poniéndole un punto después a la variable (Ej: `variable.strip()`).
* **Palabra Clave (Keyword):** Comandos reservados por Python que cambian el comportamiento del flujo del código (Ej: `break`, `continue`, `del`).
