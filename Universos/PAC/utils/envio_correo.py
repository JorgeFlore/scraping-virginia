import requests
from datetime import *
from utils import credenciales


correos=credenciales.listar_correos()

documetos=""
archivos_recibidos=list()
def correo(mensaje,empresa,archivo):

    for i in correos:
        print(i[0])
        notificar(i[0],mensaje,empresa,archivo)   




def notificar(email,mensaje,empresa,archivo):
 
    url = 'http://indiana/WebApiSmtpSOA/SOA/SendNotificacionEmail'
    fecha = datetime.now().strftime("%d-%m-%Y")
    data = {
        "Request": [{
                        "from": "RPA@aguasnuevas.cl",
                        "To": [{"Email": email} ],
                        "CC": [],
                        "Fecha": fecha,
                        "TipoAlerta": "Alerta Ejecución Descarga Universo PAC",
                        "Template": "TemplAlerta9.html",
                        "Asunto": "Universo PAC "+fecha+" "+empresa+"",
                        "Mensaje": mensaje,
                        "TablaReporte": "<p>"+archivo+"</p>",             
                    }]
    }
    requests.post(url,json=data)


