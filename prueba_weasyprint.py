from weasyprint import HTML

html = """
<html>
  <body>
    <h1>PRUEBA WEASYPRINT</h1>
    <p>Si ves la imagen, TODO está bien.</p>
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/React-icon.svg/512px-React-icon.svg.png">
  </body>
</html>
"""

HTML(string=html).write_pdf("prueba.pdf")
print("PDF generado")
