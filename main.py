"""
PROGRAMACIÓN WEB - EXAMEN (TA_EX-7)
Felipe Álvarez Valle

Aplicación Flask con un menú principal y dos ejercicios:
  - Ejercicio 1: compra de tarros de pintura con descuento según la edad
  - Ejercicio 2: inicio de sesión con dos usuarios registrados (juan, pepe)
"""

from flask import Flask, render_template, request

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Datos del ejercicio 1
# ---------------------------------------------------------------------------
PRECIO_TARRO = 9000      # valor de cada tarro de pintura
DESCUENTO_JOVEN = 15     # % para edades entre 18 y 30 años (ambas incluidas)
DESCUENTO_ADULTO = 25    # % para edades mayores a 30 años
EDAD_MAXIMA = 120

# ---------------------------------------------------------------------------
# Datos del ejercicio 2: usuarios registrados
# (en una aplicación real las contraseñas se guardan cifradas,
#  nunca en texto plano)
# ---------------------------------------------------------------------------
USUARIOS = {
    "juan": {"contrasena": "admin", "rol": "Administrador"},
    "pepe": {"contrasena": "user", "rol": "Usuario"},
}


# ---------------------------------------------------------------------------
# Funciones del ejercicio 1
# ---------------------------------------------------------------------------
def obtener_porcentaje_descuento(edad):
    """Devuelve el porcentaje de descuento que corresponde según la edad."""
    if edad > 30:
        return DESCUENTO_ADULTO
    if edad >= 18:
        return DESCUENTO_JOVEN
    return 0


def validar_compra(nombre, edad, cantidad):
    """Devuelve un mensaje de error, o None si los datos están bien."""
    if not nombre:
        return "Debes ingresar tu nombre."
    if not 0 <= edad <= EDAD_MAXIMA:
        return f"La edad debe estar entre 0 y {EDAD_MAXIMA} años."
    if cantidad < 1:
        return "Debes comprar al menos 1 tarro de pintura."
    return None


def calcular_compra(nombre, edad, cantidad):
    """Calcula los totales de la compra y los devuelve en un diccionario."""
    total_sin_descuento = cantidad * PRECIO_TARRO
    porcentaje = obtener_porcentaje_descuento(edad)
    descuento = round(total_sin_descuento * porcentaje / 100)
    total_a_pagar = total_sin_descuento - descuento
    return {
        "nombre": nombre,
        "total_sin_descuento": total_sin_descuento,
        "porcentaje": porcentaje,
        "descuento": descuento,
        "total_a_pagar": total_a_pagar,
    }


@app.template_filter("pesos")
def formato_pesos(valor):
    """Filtro de plantillas: muestra un monto en pesos (67500 -> $67.500)."""
    return "$" + f"{valor:,}".replace(",", ".")


# ---------------------------------------------------------------------------
# Funciones del ejercicio 2
# ---------------------------------------------------------------------------
def verificar_usuario(nombre, contrasena):
    """Devuelve el mensaje de bienvenida, o el de error si no coinciden."""
    usuario = USUARIOS.get(nombre)
    if usuario and usuario["contrasena"] == contrasena:
        return f"Bienvenido {usuario['rol']} {nombre}"
    return "Usuario o contraseña incorrectos"


# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Menú principal con los dos botones."""
    return render_template("index.html")


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    """GET muestra el formulario; POST recibe los datos y calcula."""
    resultado = None
    error = None
    datos = {}

    if request.method == "POST":
        datos = request.form
        nombre = request.form.get("nombre", "").strip()
        try:
            edad = int(request.form["edad"])
            cantidad = int(request.form["cantidad"])
        except (KeyError, ValueError):
            error = "La edad y la cantidad deben ser números enteros."
        else:
            error = validar_compra(nombre, edad, cantidad)
            if error is None:
                resultado = calcular_compra(nombre, edad, cantidad)

    return render_template(
        "ejercicio1.html", resultado=resultado, error=error, datos=datos
    )


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    """GET muestra el formulario; POST verifica usuario y contraseña."""
    mensaje = None
    nombre = ""

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        contrasena = request.form.get("contrasena", "")
        mensaje = verificar_usuario(nombre, contrasena)

    return render_template("ejercicio2.html", mensaje=mensaje, nombre=nombre)


if __name__ == "__main__":
    app.run(debug=True)
