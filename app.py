import os
import random
from flask import Flask, send_file, render_template_string
from pikepdf import Pdf
from io import BytesIO

app = Flask(__name__)

PDF_FOLDER = "pdfs"

HTML = """
<!doctype html>
<html>
  <head>
    <title>Tramar de los huecos un refugio</title>
  </head>
  <body style="font-family:sans-serif; text-align:center; padding-top:100px;">
    <h2>Tramar de los huecos un refugio   </h2>
    <form action="/generar" method="post">
      <button type="submit" style="padding:10px 20px; font-size:16px;">🎲 Hacé clic para generar fanzine.</button>
    </form>
 
    <p style="margin-top:50px; font-size:14px; color:gray;">
      Realizado por Martina Negrin Barcellos. colaboradorx: Brigit Zapata Munoz - Escuela de Arte y Patrimonio - UNSAM - Maestría en Practicas Artisticas Contemporaneas -
Taller de escrituras I. Practicas de desgobierno ficcional - docente: val flores

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

    if len(archivos)  == 0:
        return "No hay PDFs en el servidor."
        
    random.shuffle(archivos)

    salida = Pdf.new()

    for archivo in archivos:
        with Pdf.open(archivo) as pdf:
            if len(pdf.pages) != 1:
                return f"Error: {archivo} no tiene exactamente una página"
            salida.pages.append(pdf.pages[0])

    buffer = BytesIO()
    salida.save(buffer)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="Tramardeloshuecosunrefugio.pdf")

if __name__ == "__main__":
    app.run(debug=True)


