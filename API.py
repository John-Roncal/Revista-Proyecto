from fastapi import FastAPI, HTTPException
import pyodbc
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template

app = FastAPI()

# Conexión a SQLServer
def conectar_db():
    try:
        conexion = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=LAPTOP-R58HSL2K;"
            "DATABASE=RevistaBD;"
            "Trusted_Connection=yes;"
        )
        return conexion
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")

# Plantilla de correo
email_template = """
<html>
<body>
    <h1>Hola {{ empresa }},</h1>
    <p>Nos complace ofrecerle nuestra promoción especial para su empresa.</p>
    <p>Precio: {{ precio }}</p>
    <p>Otro texto que no cambia...</p>
</body>
</html>
"""

@app.post("/enviar-correos/")
async def enviar_correos():
    conexion = conectar_db()
    cursor = conexion.cursor()
    try:
        # Obtener los datos de la base de datos
        cursor.execute("SELECT Empresa, Correo FROM Clientes")
        clientes = cursor.fetchall()

        # Enviar correos
        for empresa, correo in clientes:
            template = Template(email_template)
            cuerpo_correo = template.render(empresa=empresa, precio="100 USD")  # Precio fijo o dinámico

            msg = MIMEMultipart()
            msg['From'] = 'dante.elefante.xyz@gmail.com'
            msg['To'] = correo
            msg['Subject'] = f"Promoción especial para {empresa}"
            msg.attach(MIMEText(cuerpo_correo, 'html'))

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()  # Habilita TLS
                server.login('dante.elefante.xyz@gmail.com', 'ChipiElQueLoLea.')
                server.send_message(msg)

        return {"mensaje": "Correos enviados exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conexion.close()