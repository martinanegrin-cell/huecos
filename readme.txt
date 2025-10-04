git init
git add .
git commit -m "Primera versión"
git branch -M main
git remote add origin https://github.com/martinanegrin-cell/huecos.git
git push -u origin main


git config --global user.name "martina"


ddn5c8gkw646kr4

git pull git@github.com:martinanegrin-cell/huecos.git


ssh-keygen -t ed25519 -C "martina.negrin@bue.edu.ar"



The key fingerprint is:
SHA256:7Kv0c4XjAvhcldPso/QFjVMHpqjxtLXZN31K62iCqIk martina.negrin@bue.edu.ar
The key's randomart image is:
+--[ED25519 256]--+
|              o. |
|           . o. .|
|        . o+o+ . |
|       . =+o*+. .|
|     .  S.o+ooo.+|
|    . ... + +..+o|
|     o.+.+ = oo  |
|   . o+.+.= oo   |
|  E o...o+ o. .  |
+----[SHA256]-----+


import os
import random
import tempfile
from flask import Flask, send_file, render_template_string
from pypdf import PdfReader, PdfWriter

app = Flask(__name__)

PDF_FOLDER = "pdfs"

HTML = """
<!doctype html>
<html>
  <head>
    <title>HUECOSRefugios</title>
  </head>
  <body style="font-family:sans-serif; text-align:center; padding-top:100px;">
    <h2>Generar un fanizine</h2>
    <form action="/generar" method="post">
      <button type="submit" style="padding:10px 20px; font-size:16px;">🎲 Crear Fanzine</button>
    </form>
  </body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/generar", methods=["POST"])
def generar():
    archivos = [os.path.join(PDF_FOLDER, f) for f in sorted(os.listdir(PDF_FOLDER)) if f.endswith(".pdf")]

    if len(archivos) != 12:
        return f"Error: Debe haber exactamente 12 archivos PDF en la carpeta '{PDF_FOLDER}'"

    random.shuffle(archivos)
    salida = PdfWriter()

    for archivo in archivos:
        try:
            lector = PdfReader(archivo)
            if len(lector.pages) == 0:
                return f"Error: {archivo} no contiene páginas."
            salida.add_page(lector.pages[0])
        except Exception as e:
            return f"Error procesando {archivo}: {str(e)}"

    # Usamos un archivo temporal (más seguro que BytesIO en servidores)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        salida.write(temp)
        temp_path = temp.name

    return send_file(temp_path, as_attachment=True, download_name="resultado.pdf")

if __name__ == "__main__":
    app.run(debug=True)
    
    
    

import os
import random
from flask import Flask, send_file, render_template_string
from PyPDF import PdfReader, PdfWriter
from io import BytesIO

app = Flask(__name__)

# Carpeta donde vos cargás los PDFs de 1 página
PDF_FOLDER = "pdfs"

HTML = """
<!doctype html>
<html>
  <head>
    <title>Generador de PDF Aleatorio</title>
  </head>
  <body style="font-family:sans-serif; padding:30px;">
    <h2>Tramar de los huecos un refugio</h2>
    <p>Hacé clic para generar fanzine.</p>
    <form method="get" action="/generar">
      <button type="submit">Tramar de los huecos un refugio</button>
    </form>
  </body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/generar")
def generar():
    archivos = [os.path.join(PDF_FOLDER, f) for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]

    if len(archivos) == 0:
        return "No hay PDFs en el servidor."

    random.shuffle(archivos)
    salida = PdfWriter()

    for archivo in archivos:
        lector = PdfReader(archivo)
        if len(lector.pages) != 1:
            return f"El archivo {archivo} no tiene exactamente 1 página"
        salida.add_page(lector.pages[0])

    buffer = BytesIO()
    salida.write(buffer)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="tramardeloshuecosunrefugio.pdf")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


