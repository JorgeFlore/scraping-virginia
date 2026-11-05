from os import scandir, getcwd
import os
import win32com.client as win32
from datetime import datetime, timedelta
from os import makedirs, path, getcwd


ruta_archivos = r"C:\Rendicion\bestado\descargados"

def envio_correo():  
    
    adjuntos=[]
    
    fecha_actual = datetime.now()+timedelta(days=-1)
    fecha_actual = str(fecha_actual.strftime("%Y-%m-%d"))
    format = fecha_actual.replace("-","")
    contenido = os.listdir(ruta_archivos)
    lista_archivos = []
    print(format)
    for fichero in contenido:
        if os.path.isfile(os.path.join(ruta_archivos, fichero)):
            lista_archivos.append(fichero)
    print(lista_archivos)
    
    
    outlook=win32.Dispatch("Outlook.Application")
  
    
    for i in lista_archivos:
        adjuntos.append(ruta_archivos+'\\'+i)
    mail=outlook.CreateItem(0)
    mail.cc='manuel.rodriguez@aguasnuevas.cl;fabian.cabrera@aguasnuevas.cl;jorge.flores@aguasnuevas.cl;eduardo.gajardo@aguasnuevas.cl;'
    #mail.cc='jorge.flores@aguasnuevas.cl'
    mail.to=''
    for attachment in adjuntos:
        mail.Attachments.Add(attachment)
    #mail.Attachments.Add(lista)
    mail.Subject='Alerta envío Archivo Boton de pago Banco Estado (QA SFTP)'
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
    <td style="width:850px;text-align:left"><strong>
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
    Se ha ejecutado correctamente el bot de descarga Boton de Pago Banco Estado. Se adjuntan los archivos correspondientes. 
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