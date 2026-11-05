import smtplib
import win32com.client as win32
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from time import sleep



def envio_correo(empresa, ruta,nombre_carpeta,empresas):
       
    ruta_recibida=ruta
    contenido = os.listdir(ruta_recibida)
    lista_archivos = []
    for rut in empresas:
        if i == rut :
            print(i)

    for fichero in contenido:
        if os.path.isfile(os.path.join(ruta_recibida, fichero)) :
            lista_archivos.append(fichero)
        print(lista_archivos)
        outlook=win32.Dispatch("Outlook.Application")

        adjuntos=[]
        for i in lista_archivos:
            adjuntos.append(ruta+nombre_carpeta+'\\'+empresas+'\\'+i)
        mail=outlook.CreateItem(0)
        mail.to='jorge.flores@aguasnuevas.cl'
        for attachment in adjuntos:
            mail.Attachments.Add(attachment)
        mail.Subject='Información de Carga Universos'+nombre_carpeta+' '+empresa
        mail.HTMLbody =r"""<div>
        <table>
        <tbody>
        <tr>
        </tr>
        <tr>
        <td>
        <table width="100%" style="height:58px">
        <tbody>
        <tr>
        <td style="width:850px;text-align:left"><strong>Información de Pagos BCI """+ nombre_carpeta +""" """+empresa+""" <br>
        </strong></td>
        </tr>
        </tbody>
        </table>
        <hr>
        <table style="height:49px;width:100%">
        <tbody>
        <tr>
        <td style="width:850px;text-align:justify">
        <table cellspacing="0" cellpadding="0" style="border:none">
        <tbody>
        <tr>
        <td style="width:848px;font-family:Arial;font-size:12px;text-align:justify">Estimado usuario,
        <br>
        Se ha ejecutado correctamente el bot de descarga de información de pagos BCI de """+empresa+""". Se adjuntan los archivos correspondientes. 
        </td>
        </tr>
        </tbody>
        </table>
        </td>
        </tr>
        </tbody>
        </table>
        <table>
        </table>
        </td>
        </tr>
        </tbody>
        </table>
        </div>"""
        mail.Send()