import requests
from datetime import *
from utils import credenciales

correos=credenciales.listar_correos()

def correo(mensaje,empresa):
    for i in correos:
        print(i[0])
        notificar(i[0],mensaje,empresa)   

def notificar(email,mensaje,empresa):
 
    url = 'http://indiana/WebApiSmtpSOA/SOA/SendNotificacionEmail'
    fecha = datetime.now().strftime("%d-%m-%Y")
    data = {
        "Request": [{
                        "from": "RPA@aguasnuevas.cl",
                        "To": [{"Email": email} ],
                        "CC": [],
                        "Fecha": fecha,
                        "TipoAlerta": "Alerta Ejecución Boletas de Honorarios <br>",
                        "Template": "TemplAlerta9.html",
                        "Asunto": "Boletas de honorarios "+fecha+" "+empresa+"",
                        "Mensaje": mensaje,
                        #"TablaReporte":documentos,             
                    }]
    }
    requests.post(url,json=data)