import requests
import base64
from datetime import *
from utils import credenciales
import os


correos=credenciales.listar_correos()

documetos=""
archivos_recibidos=list()
def correo(mensaje,empresa, ruta_imagen = None):

    for i in correos:
        print(i[0])
        notificar(i[0],mensaje,empresa, ruta_imagen)   



def notificar(email,mensaje,empresa, ruta_imagen = None):
 
    url = 'http://indiana/WebApiSmtpSOA/SOA/SendNotificacionEmail'
    fecha = datetime.now().strftime("%d-%m-%Y")
    imagen_base64 = ""

    if ruta_imagen and os.path.exists(ruta_imagen):
        try:
            with open(ruta_imagen, "rb") as img_file:
                imagen_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        except Exception as img_error:
            print(f"Error al leer la imagen: {img_error}")
    
    mensaje_html = f"""
    <html>
        <body>
            <p><b>Empresa:</b> {empresa}</p>
            <p><b>Fecha:</b> {fecha}</p>
            <p><b>Detalle:</b> {mensaje}</p>
            {f'<img src="data:image/png;base64,{imagen_base64}" alt="Captura de error" style="max-width:600px;">' if imagen_base64 else ''}
        </body>
    </html>
    """

    data = {
        "Request": [{
                        "from": "RPA@aguasnuevas.cl",
                        "To": [{"Email": email} ],
                        "CC": [],
                        "Fecha": fecha,
                        "TipoAlerta": "Alerta Ejecución Factoring XML",
                        "Template": "TemplAlerta9.html",
                        "Asunto": "Factoring XML "+fecha+" "+empresa+"",
                        "Mensaje": mensaje_html,
                        #"TablaReporte": "<p>"+archivo+"</p>",             
                    }]
    }
    requests.post(url,json=data)


