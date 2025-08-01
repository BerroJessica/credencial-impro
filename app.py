from flask import Flask, render_template
import json
import os
import qrcode
import base64
from io import BytesIO
from datetime import datetime

app = Flask(__name__)

def cargar_datos():
    with open("data.json") as f:
        return json.load(f)

@app.route("/alumno/<id>")
def credencial(id):
    alumnos = cargar_datos()
    alumno = next((a for a in alumnos if a["id"] == id), None)
    if not alumno:
        return "Alumno no encontrado", 404

    ahora = datetime.utcnow().isoformat()
    url_verificacion = f"https://tu-app.onrender.com/verificar/{id}?t={ahora}"

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
