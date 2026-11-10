import requests
from datetime import *
from utils import credenciales
import os
import base64
import logging

correos=credenciales.listar_correos()

documetos=""
archivos_recibidos=list()


def correo(mensaje,empresa, screenshot_path=None):
    for i in correos:
        print(i[0])
        notificar(i[0],mensaje,empresa, screenshot_path)   


def notificar(email,mensaje,empresa,screenshot_path = None):
 
    url = 'http://indiana/WebApiSmtpSOA/SOA/SendNotificacionEmail'
    fecha = datetime.now().strftime("%d-%m-%Y")

    # if archivo is None:
    #     archivo = "No se adjunto archivo"
    

    imagen_base64 = ""
    if screenshot_path and os.path.exists(screenshot_path):
        with open(screenshot_path, "rb") as img_file:
            imagen_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            
    imagen_html = f'<img src="data:image/png;base64,{imagen_base64}" style="max-width:600px;">' if imagen_base64 else "No se adjunto imagen."
    
    data = {
        "Request": [{
                        "from": "RPA@aguasnuevas.cl",
                        "To": [{"Email": email} ],
                        "CC": [],
                        "Fecha": fecha,
                        "TipoAlerta": "Alerta Ejecución Descarga Universo PAT",
                        "Template": "TemplAlerta9.html",
                        "Asunto": "Universo PAT "+fecha+" "+empresa+"",
                        "Mensaje": f"{mensaje}<br><br>{imagen_html}",
                        # "TablaReporte": f"<p>{archivo}</p>",
                    }]
    }
    try:
        r = requests.post(url, json=data, timeout=30)
        r.raise_for_status()
    except Exception as e:  # noqa: BLE001 - un correo fallido no debe detener la carga
        logging.error(f"No se pudo enviar el correo a {email}: {e}")


