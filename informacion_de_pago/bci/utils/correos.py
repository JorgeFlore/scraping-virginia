import smtplib
import win32com.client as win32
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from time import sleep

#ruta='C:\\Users\\\manuel.rodriguez\\Desktop\\Scraping\\Información de pago\\BCI\\descargas\\09-07-2024\\ADA'



#ruta = 'C:\\Users\\manuel.rodriguez\\Desktop\\Scraping\\Información de pago\\BCI\\descargas\\09-07-2024\\ADA\\'

def envio_correo(ruta,nombre_carpeta,empresa):
    ruta_recibida=ruta+nombre_carpeta+'\\'+empresa
    #sleep(7)
    contenido = os.listdir(ruta_recibida)
    
    lista_archivos = []
    for fichero in contenido:
        if os.path.isfile(os.path.join(ruta_recibida, fichero)):
            lista_archivos.append(fichero)
    print(lista_archivos)

    #ruta_adjunto = 'E:\myfile.txt'
    #nombre_adjunto = 'E:\myfile.txt'
    #archivo_adjunto = open(ruta_adjunto, 'rb')
    #
    #adjunto_MIME = MIMEBase('application', 'octet-stream')
    #adjunto_MIME.set_payload((archivo_adjunto).read())
    #adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s"%nombre_adjunto)
    #lista_archivos=list(filter(os.path.isfile, os.listdir()))

    outlook=win32.Dispatch("Outlook.Application")
    #correos=['manuel.rodriguez.sandoval2@gmail.com','manuel.rodriguez@aguasnuevas.cl']
    #lista_archivos
    adjuntos=[]
    for i in lista_archivos:
        adjuntos.append(ruta+nombre_carpeta+'\\'+empresa+'\\'+i)


    mail=outlook.CreateItem(0)

    #print(os.listdir())

    #for i in correos:
        #mail.To=correos:
    #mail.to='romina.cinto@aguasnuevas.cl;griselda.aburto@aguasnuevas.cl'
    #mail.to='manuel.rodriguez@aguasnuevas.cl;jorge.flores@aguasnuevas.cl'
    #mail.cc='manuel.rodriguez@aguasnuevas.cl;jorge.flores@aguasnuevas.cl;fabian.cabrera@aguasnuevas.cl;rodrigo.endara@aguasnuevas.cl'


    for attachment in adjuntos:
        mail.Attachments.Add(attachment)

    #mail.Attachments.Add(lista)

    mail.Subject='Información de Pagos BCI '+nombre_carpeta+' '+empresa

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