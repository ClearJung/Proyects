import json
import os

ARCHIVO = "estudiantes.json"
estudiantes = []

# -----------------------------
# PERSISTENCIA
# -----------------------------

def cargar_estudiantes():
    global estudiantes
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            estudiantes = json.load(f)
    else:
        estudiantes = []

def guardar_estudiantes():
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(estudiantes, f, indent=4)

# -----------------------------
# VALIDACIONES
# -----------------------------

def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        else:
            print("No puede estar vacío.")

def pedir_nota(mensaje):
    while True:
        try:
            nota = float(input(mensaje))
            if 0 <= nota <= 20:
                return nota
            else:
                print("La nota debe estar entre 0 y 20.")
        except:
            print("Ingrese un número válido.")

def pedir_notas():
    notas = []
    for i in range(3):
        nota = pedir_nota(f"Ingrese nota {i+1}: ")
        notas.append(nota)
    return notas

# -----------------------------
# LOGICA
# -----------------------------

def calcular_promedio(notas):
    return sum(notas) / len(notas)

def obtener_estado(promedio):
    if promedio >= 11:
        return "Aprobado"
    else:
        return "Desaprobado"

# -----------------------------
# OPERACIONES
# -----------------------------

def registrar_estudiante():
    nombre = pedir_texto("Nombre del estudiante: ")
    carrera = pedir_texto("Carrera: ")
    notas = pedir_notas()
    promedio = calcular_promedio(notas)
    estado = obtener_estado(promedio)

    estudiante = {
        "nombre": nombre,
        "carrera": carrera,
        "notas": notas,
        "promedio": promedio,
        "estado": estado
    }

    estudiantes.append(estudiante)
    guardar_estudiantes()
    print("Estudiante guardado correctamente.\n")

def mostrar_estudiantes():
    if len(estudiantes) == 0:
        print("No hay estudiantes registrados.\n")
        return

    for i, e in enumerate(estudiantes, start=1):
        print(f"\nEstudiante {i}")
        print("Nombre:", e["nombre"])
        print("Carrera:", e["carrera"])
        print("Notas:", e["notas"])
        print("Promedio:", round(e["promedio"], 2))
        print("Estado:", e["estado"])

# -----------------------------
# MENU
# -----------------------------

def menu():
    cargar_estudiantes()

    while True:
        print("\n--- MENÚ ---")
        print("1. Registrar estudiante")
        print("2. Mostrar estudiantes")
        print("3. Salir")

        opcion = input("Seleccione opción: ")

        if opcion == "1":
            registrar_estudiante()
        elif opcion == "2":
            mostrar_estudiantes()
        elif opcion == "3":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")

menu()
