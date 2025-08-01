from flask import Flask, render_template, request, redirect
import json
import qrcode
import base64
from io import BytesIO
from datetime import datetime
import os

app = Flask(__name__)

def cargar_datos():
    with open("data.json") as f:
        return json.load(f)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/buscar", methods=["POST"])
def buscar():
    rut = request.form.get("rut")
    alumnos = cargar_datos()
    alumno = next((a for a in alumnos if a["rut"] == rut), None)
    if alumno:
        return redirect(f"/alumno/{alumno['id']}")
    return "RUT no encontrado", 404

@app.route("/alumno/<id>")
def credencial(id):
    alumnos = cargar_datos()
    alumno = next((a for a in alumnos if a["id"] == id), None)
    if not alumno:
        return "Alumno no encontrado", 404

    url_verificacion = f"https://credencial-impro.onrender.com/verificar/{id}"

    qr = qrcode.make(url_verificacion)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render_template("alumno.html", alumno=alumno, qr=qr_base64)

@app.route("/verificar/<id>")
def verificar(id):
    alumnos = cargar_datos()
    alumno = next((a for a in alumnos if a["id"] == id), None)
    if not alumno:
        return "Alumno no encontrado", 404
    return render_template("verificador.html", alumno=alumno)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
