import requests
from datetime import *
from utils import credenciales
import os
import base64

correos=credenciales.listar_correos()

documetos=""
archivos_recibidos=list()


def correo(mensaje, empresa, screenshots_dict):
    for i in correos:
        print(i[0])
        notificar(i[0],mensaje,empresa, screenshots_dict)   


def notificar(email, mensaje, empresa, screenshots_dict):
 
    url = 'http://indiana/WebApiSmtpSOA/SOA/SendNotificacionEmail'
    fecha = datetime.now().strftime("%d-%m-%Y")

    imagenes_html = ""
    imagen_base64 = ""
    for screenshot_path, screenshot_msg in screenshots_dict.items():
        if os.path.exists(screenshot_path):
            with open(screenshot_path, "rb") as img_file:
                imagen_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            imagenes_html += f"<p>{screenshot_msg}</p><img src='data:image/png;base64,{imagen_base64}' style='max-width:600px;'><br>"
                
    mensaje_final = f"<p>{mensaje}</p><br>{imagenes_html}" if imagenes_html else f"<p>{mensaje}</p><br><p>No se adjuntaron imagenes.</p>"
    
    data = {
        "Request": [{
                        "from": "RPA@aguasnuevas.cl",
                        "To": [{"Email": email} ],
                        "CC": [],
                        "Fecha": fecha,
                        "TipoAlerta": "Alerta Ejecución Descarga BCI",
                        "Template": "TemplAlerta9.html",
                        "Asunto": "BCI "+fecha+" "+empresa+"",
                        # "Mensaje": f"{mensaje}<br><br>{imagen_html}",
                        "Mensaje": mensaje_final
                    }]
    }
    requests.post(url,json=data)