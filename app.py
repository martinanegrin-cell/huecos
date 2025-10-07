import os
import random
from flask import Flask, send_file, render_template_string
from pikepdf import Pdf
from io import BytesIO

app = Flask(__name__)

PDF_FOLDER = "pdfs"
PORTADA = "portada.pdf"
ULTIMA = "ultima.pdf"

HTML = """
<!doctype html>
<html>
  <head>
    <title>Tramar de los huecos un refugio</title>
    <style>
      body {
        background-color: #000000;
        color: #ff69b4;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        text-align: center;
        padding-top: 100px;
      }
      h2 {
        color: #ff69b4;
        font-weight: bold;
      }
      button {
        padding: 12px 25px;
        font-size: 16px;
        background-color: #ff69b4;
        color: black;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
      }
      button:hover {
        background-color: #ff85c1;
      }
      p {
        margin-top: 50px;
        font-size: 14px;
        color: #ff69b4;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
      }
    </style>
  </head>
  <body>
    <h2>Tramar de los huecos un refugio</h2>
    <form action="/generar" method="post">
      <button type="submit" style="padding:20px 40px; font-size:30px;">
        🎲 Hacé clic para generar fanzine 🎲
      </button>
    </form>

    <p style="margin-top:50px; font-size:14px; color:gray;">
      Realizado por Martina Negrin Barcellos. colaboradorx: Brigit Zapata Muñoz - Escuela de Arte y Patrimonio - UNSAM - Maestría en Prácticas Artísticas Contemporáneas -
      Taller de escrituras I. Prácticas de desgobierno ficcional - docente: val flores
    </p>
  </body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/generar", methods=["POST"])
def generar():
    archivos = [os.path.join(PDF_FOLDER, f) for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]

    if len(archivos) == 0:
        return "No hay PDFs en el servidor."
        
    random.shuffle(archivos)

    salida = Pdf.new()

    # --- Agregar portada ---
    if os.path.exists(PORTADA):
        with Pdf.open(PORTADA) as p:
            salida.pages.extend(p.pages)
    else:
        return "Error: No se encontró el archivo 'portada.pdf'"

    # --- Agregar las páginas aleatorias ---
    for archivo in archivos:
        with Pdf.open(archivo) as pdf:
            if len(pdf.pages) != 1:
                return f"Error: {archivo} no tiene exactamente una página"
            salida.pages.append(pdf.pages[0])

    # --- Agregar última página ---
    if os.path.exists(ULTIMA):
        with Pdf.open(ULTIMA) as u:
            salida.pages.extend(u.pages)
    else:
        return "Error: No se encontró el archivo 'ultima.pdf'"

    # --- Guardar resultado ---
    buffer = BytesIO()
    salida.save(buffer)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="Tramardeloshuecosunrefugio.pdf")

if __name__ == "__main__":
    app.run(debug=True)


