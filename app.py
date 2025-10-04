import os
import random
from flask import Flask, send_file, render_template_string
from PyPDF2 import PdfReader, PdfWriter
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

