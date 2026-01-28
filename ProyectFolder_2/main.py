import json
import os
import csv

ARCHIVO = "gastos.json"
gastos = []

# -----------------------------
# PERSISTENCIA
# -----------------------------

def cargar_gastos():
    global gastos
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            gastos = json.load(f)
    else:
        gastos = []

CATEGORIAS = [
    "Comida",
    "Transporte",
    "Servicios",
    "Alquiler",
    "Deudas",
    "Salud",
    "Educación",
    "Entretenimiento",
    "Ropa",
    "Mascotas",
    "Ahorro",
    "Otros"
]

def guardar_gastos():
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(gastos, f, indent=4)

# -----------------------------
# VALIDACIONES
# -----------------------------

def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        else:
            print("No puede estar vacío.")

def pedir_categoria():
    while True:
        print("\nCategorías disponibles:")
        for i, c in enumerate(CATEGORIAS, start=1):
            print(f"{i}. {c}")

        opcion = input("Seleccione categoría: ")

        if opcion.isdigit():
            opcion = int(opcion)
            if 1 <= opcion <= len(CATEGORIAS):
                return CATEGORIAS[opcion - 1]

        print("Selección inválida.")

def pedir_monto(mensaje):
    while True:
        try:
            monto = float(input(mensaje))
            if monto > 0:
                return monto
            else:
                print("El monto debe ser mayor a 0.")
        except:
            print("Ingrese un número válido.")

# -----------------------------
# OPERACIONES
# -----------------------------

def registrar_gasto():
    monto = pedir_monto("Monto del gasto: ")
    categoria = pedir_categoria()
    descripcion = pedir_texto("Descripción: ")

    gasto = {
        "monto": monto,
        "categoria": categoria,
        "descripcion": descripcion
    }

    gastos.append(gasto)
    guardar_gastos()
    print("Gasto registrado.\n")

def mostrar_gastos():
    if len(gastos) == 0:
        print("No hay gastos registrados.\n")
        return

    for i, g in enumerate(gastos, start=1):
        print(f"\nGasto {i}")
        print("Monto:", g["monto"])
        print("Categoría:", g["categoria"])
        print("Descripción:", g["descripcion"])

def eliminar_gasto():
    if len(gastos) == 0:
        print("No hay gastos para eliminar.")
        return

    mostrar_gastos()

    while True:
        opcion = input("Ingrese número de gasto a eliminar: ")

        if opcion.isdigit():
            opcion = int(opcion)
            if 1 <= opcion <= len(gastos):
                eliminado = gastos.pop(opcion - 1)
                guardar_gastos()
                print("Gasto eliminado:")
                print(eliminado)
                return

        print("Selección inválida.")

def editar_gasto():
    if len(gastos) == 0:
        print("No hay gastos para editar.")
        return

    mostrar_gastos()

    while True:
        opcion = input("Ingrese número de gasto a editar: ")

        if opcion.isdigit():
            opcion = int(opcion)
            if 1 <= opcion <= len(gastos):
                gasto = gastos[opcion - 1]

                print("\nDejar vacío para mantener valor actual.")

                nuevo_monto = input(f"Monto actual ({gasto['monto']}): ")
                if nuevo_monto != "":
                    try:
                        nuevo_monto = float(nuevo_monto)
                        if nuevo_monto > 0:
                            gasto["monto"] = nuevo_monto
                    except:
                        print("Monto inválido. Se mantiene.")

                print(f"Categoría actual: {gasto['categoria']}")
                cambiar = input("¿Cambiar categoría? (s/n): ").lower()
                if cambiar == "s":
                    gasto["categoria"] = pedir_categoria()

                nueva_desc = input(f"Descripción actual ({gasto['descripcion']}): ")
                if nueva_desc != "":
                    gasto["descripcion"] = nueva_desc

                guardar_gastos()
                print("Gasto actualizado.")
                return

        print("Selección inválida.")

def total_gastado():
    total = sum(g["monto"] for g in gastos)
    print("Total gastado:", total)

def total_por_categoria():
    categoria = pedir_categoria()
    total = 0

    for g in gastos:
        if g["categoria"] == categoria:
            total += g["monto"]

    print(f"Total en {categoria}: {total}")

def exportar_csv():
    if len(gastos) == 0:
        print("No hay gastos para exportar.")
        return

    with open("gastos.csv", "w", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["monto", "categoria", "descripcion"])

        for g in gastos:
            writer.writerow([g["monto"], g["categoria"], g["descripcion"]])

    print("Gastos exportados a gastos.csv")

# -----------------------------
# MENU
# -----------------------------

def menu():
    cargar_gastos()

    while True:
        print("\n--- CONTROL DE GASTOS ---")
        print("1. Registrar gasto")
        print("2. Mostrar gastos")
        print("3. Total gastado")
        print("4. Total por categoría")
        print("5. Exportar a CSV")
        print("6. Eliminar gasto")
        print("7. Editar gasto")
        print("8. Salir")

        opcion = input("Seleccione opción: ")

        if opcion == "1":
            registrar_gasto()
        elif opcion == "2":
            mostrar_gastos()
        elif opcion == "3":
            total_gastado()
        elif opcion == "4":
            total_por_categoria()
        elif opcion == "5":
            exportar_csv()
        elif opcion == "6":
            eliminar_gasto()
        elif opcion == "7":
            editar_gasto()
        elif opcion == "8":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

menu()
