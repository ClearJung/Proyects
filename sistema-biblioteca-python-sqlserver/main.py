import pyodbc
import hashlib
from datetime import date
import re

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
# -------------------------
# CONEXION A SQL SERVER
# -------------------------

conexion = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=BibliotecaDB;"
    "Trusted_Connection=yes;"
)

cursor = conexion.cursor()

# -------------------------
# FUNCIONES
# -------------------------

def login():
    usuario = input("Usuario: ").strip()
    password = input("Contraseña: ").strip()

    password_hash = hash_password(password)

    cursor.execute("""
        SELECT rol FROM UsuariosSistema
        WHERE usuario = ? AND password = ?
    """, (usuario, password_hash))

    fila = cursor.fetchone()

    if fila:
        print("Login exitoso.")
        return fila[0]   
    else:
        print("Credenciales incorrectas.")
        return None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def registrar_libro():
    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()

    if titulo == "":
        print("Título no puede estar vacío.")
        return
    
    if not re.search(r"[A-Za-z0-9]", titulo):
        print("El título debe contener al menos una letra o número.")
        return


    if autor == "":
        print("Autor no puede estar vacío.")
        return

    if not any(c.isalpha() for c in autor):
        print("Autor debe contener letras.")
        return

    if len(titulo) > 100 or len(autor) > 100:
        print("Texto demasiado largo.")
        return

    cursor.execute(
        "SELECT * FROM Libros WHERE titulo = ? AND autor = ?",
        titulo, autor
    )
    if cursor.fetchone():
        print("Ese libro ya está registrado.")
        return

    codigo = generar_codigo_libro()

    cursor.execute(
        "INSERT INTO Libros (codigo, titulo, autor, disponible) VALUES (?, ?, ?, 1)",
        codigo, titulo, autor
    )
    conexion.commit()
    print(f"Libro registrado con código: {codigo}")

def mostrar_libros():
    cursor.execute("SELECT * FROM Libros")
    libros = cursor.fetchall()

    if not libros:
        print("No hay libros.")
        return

    for l in libros:
        estado = "Disponible" if l[3] else "Prestado"
        print(f"{l[0]} | {l[1]} | {l[2]} | {estado}")

def registrar_usuario():
    usuario = input("Usuario: ").strip()
    password = input("Contraseña: ").strip()
    rol = input("Rol (admin/bibliotecario): ").strip().lower()

    if usuario == "" or password == "" or rol == "":
        print("Campos obligatorios.")
        return

    if rol not in ["admin", "bibliotecario"]:
        print("Rol inválido.")
        return

    cursor.execute("""
        SELECT 1 FROM UsuariosSistema WHERE usuario = ?
    """, (usuario,))

    if cursor.fetchone():
        print("Ese usuario ya existe.")
        return

    password_hash = hash_password(password)

    cursor.execute("""
        INSERT INTO UsuariosSistema (usuario, password, rol)
        VALUES (?, ?, ?)
    """, (usuario, password_hash, rol))

    conexion.commit()
    print("Usuario registrado correctamente.")



def mostrar_usuarios():
    cursor.execute("""
        SELECT usuario, rol
        FROM UsuariosSistema
    """)

    usuarios = cursor.fetchall()

    print("\n--- USUARIOS DEL SISTEMA ---")
    for u in usuarios:
        print(f"{u[0]} | {u[1]}")


def registrar_lector():
    nombre = input("Nombre lector: ").strip()
    dni = input("DNI (8 dígitos): ").strip()

    if nombre == "" or dni == "":
        print("Campos obligatorios.")
        return

    
    if nombre.isdigit():
        print("El nombre no puede ser solo números.")
        return

    
    if not dni.isdigit() or len(dni) != 8:
        print("El DNI debe tener exactamente 8 números.")
        return

    
    cursor.execute("""
        SELECT 1 FROM Lectores WHERE dni = ?
    """, (dni,))

    if cursor.fetchone():
        print("Ya existe un lector con ese DNI.")
        return

    cursor.execute("""
        INSERT INTO Lectores (nombre, dni)
        VALUES (?, ?)
    """, (nombre, dni))

    conexion.commit()
    print("Lector registrado correctamente.")



def mostrar_lectores():
    cursor.execute("SELECT id, nombre, dni FROM Lectores")
    lectores = cursor.fetchall()

    print("\n--- LECTORES ---")
    for l in lectores:
        print(f"ID:{l[0]} | {l[1]} | DNI:{l[2]}")


def prestar_libro():

    mostrar_libros()
    codigo = input("Código del libro: ").strip()

    cursor.execute("""
        SELECT disponible FROM Libros
        WHERE codigo = ?
    """, (codigo,))

    libro = cursor.fetchone()

    if not libro:
        print("Libro no existe.")
        return

    if libro[0] == 0:
        print("Libro no disponible.")
        return

    mostrar_lectores()
    lector_id = input("ID del lector: ").strip()

    if not lector_id.isdigit():
        print("ID inválido.")
        return

    cursor.execute("""
        SELECT id FROM Lectores
        WHERE id = ?
    """, (lector_id,))

    if not cursor.fetchone():
        print("Lector no existe.")
        return

    cursor.execute("""
        INSERT INTO Prestamos (codigo, id_lector, fecha_prestamo, devuelto)
        VALUES (?, ?, ?, 0)
    """, (codigo, lector_id, date.today()))

    cursor.execute("""
        UPDATE Libros
        SET disponible = 0
        WHERE codigo = ?
    """, (codigo,))

    conexion.commit()
    print("Préstamo registrado correctamente.")

def devolver_libro():

    mostrar_prestamos_activos()
    prestamo_id = input("ID del préstamo: ").strip()

    if not prestamo_id.isdigit():
        print("ID inválido.")
        return

    cursor.execute("""
        SELECT codigo
        FROM Prestamos
        WHERE id = ? AND devuelto = 0
    """, (prestamo_id,))

    fila = cursor.fetchone()

    if not fila:
        print("Préstamo no encontrado.")
        return

    codigo = fila[0]

    cursor.execute("""
        UPDATE Prestamos
        SET devuelto = 1
        WHERE id = ?
    """, (prestamo_id,))

    cursor.execute("""
        UPDATE Libros
        SET disponible = 1
        WHERE codigo = ?
    """, (codigo,))

    conexion.commit()
    print("Libro devuelto correctamente.")


def generar_codigo_libro():
    cursor.execute("""
        SELECT TOP 1 codigo
        FROM Libros
        ORDER BY codigo DESC
    """)

    fila = cursor.fetchone()

    if not fila:
        return "LIB-0001"

    ultimo = fila[0]          
    numero = int(ultimo.split("-")[1]) + 1
    return f"LIB-{numero:04d}"


def mostrar_prestamos_activos():
    cursor.execute("""
        SELECT 
            p.id,
            l.titulo,
            le.nombre,
            p.fecha_prestamo
        FROM Prestamos p
        JOIN Libros l ON p.codigo = l.codigo
        JOIN Lectores le ON p.id_lector = le.id
        WHERE p.devuelto = 0
    """)

    prestamos = cursor.fetchall()

    if not prestamos:
        print("No hay préstamos activos.")
        return

    print("\n--- PRÉSTAMOS ACTIVOS ---")
    for p in prestamos:
        print(f"ID:{p[0]} | {p[1]} | {p[2]} | {p[3]}")

def eliminar_libro():
    mostrar_libros()
    codigo = input("Código libro a eliminar: ").strip()

    cursor.execute("""
        SELECT 1 FROM Libros WHERE codigo = ?
    """, (codigo,))

    if not cursor.fetchone():
        print("Libro no existe.")
        return

    cursor.execute("""
        DELETE FROM Libros WHERE codigo = ?
    """, (codigo,))

    conexion.commit()
    print("Libro eliminado correctamente.")


def eliminar_usuario():
    mostrar_usuarios()
    usuario = input("Usuario a eliminar: ").strip()

    cursor.execute("""
        SELECT 1 FROM UsuariosSistema WHERE usuario = ?
    """, (usuario,))

    if not cursor.fetchone():
        print("Usuario no existe.")
        return

    cursor.execute("""
        DELETE FROM UsuariosSistema WHERE usuario = ?
    """, (usuario,))

    conexion.commit()
    print("Usuario eliminado correctamente.")

def eliminar_lector():
    mostrar_lectores()
    lector_id = input("ID lector a eliminar: ").strip()

    if not lector_id.isdigit():
        print("ID inválido.")
        return

    cursor.execute("""
        SELECT 1 FROM Lectores WHERE id = ?
    """, (lector_id,))

    if not cursor.fetchone():
        print("Lector no existe.")
        return

    cursor.execute("""
        DELETE FROM Lectores WHERE id = ?
    """, (lector_id,))

    conexion.commit()
    print("Lector eliminado correctamente.")



# -------------------------
# MENU
# -------------------------

def menu(rol):
    while True:

        print("\n--- MENU ---")

        if rol == "admin":
            print("1. Registrar libro")
            print("2. Mostrar libros")
            print("3. Registrar usuario")
            print("4. Mostrar usuarios")
            print("5. Prestar libro")
            print("6. Devolver libro")
            print("7. Registrar lector")
            print("8. Mostrar lectores")
            print("9. Eliminar libro")
            print("10. Eliminar usuario")
            print("11. Eliminar lector")
            print("12. Salir")

        else:
            print("1. Mostrar libros")
            print("2. Prestar libro")
            print("3. Devolver libro")
            print("4. Salir")

        opcion = input("Opción: ")

        if rol == "admin":

            if opcion == "1":
                registrar_libro()
            elif opcion == "2":
                mostrar_libros()
            elif opcion == "3":
                registrar_usuario()
            elif opcion == "4":
                mostrar_usuarios()
            elif opcion == "5":
                prestar_libro()
            elif opcion == "6":
                devolver_libro()
            elif opcion == "7":
                registrar_lector() 
            elif opcion == "8":
                mostrar_lectores()
            elif opcion == "9":
                eliminar_libro()    
            elif opcion == "10":
                eliminar_usuario()
            elif opcion == "11":
                eliminar_lector()
            elif opcion == "12":
                break

        else:

            if opcion == "1":
                mostrar_libros()
            elif opcion == "2":
                prestar_libro()
            elif opcion == "3":
                devolver_libro()
            elif opcion == "4":
                break


# -------------------------
# EJECUCION
# -------------------------

rol = login()

if rol:
    menu(rol)

conexion.close()

