from os import scandir, getcwd
import os
import win32com.client as win32
from datetime import datetime, timedelta

def envio_correo():  
    ruta_archivos="C:/B.Estado - Compra Aqui/descargados/"
    adjuntos=[]
    #def listar_archivos(ruta):
    #    return [arch.name for arch in scandir(ruta) if arch.is_file()]
    #
    #
    #pac=listar_archivos(ruta_archivos)
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
        #correos=['manuel.rodriguez.sandoval2@gmail.com','manuel.rodriguez@aguasnuevas.cl']
        #lista_archivos
  
    
    for i in lista_archivos:
        #if (format in i):
        adjuntos.append(ruta_archivos+'\\'+i)
    mail=outlook.CreateItem(0)
    #print(os.listdir())
    #for i in correos:
        #mail.To=correos:
    
    mail.to='romina.cinto@aguasnuevas.cl;griselda.aburto@aguasnuevas.c;karol.alvarado@aguasnuevas.cl;diego.morales@aguasnuevas.cl'
    mail.cc='manuel.rodriguez@aguasnuevas.cl;jorge.flores@aguasnuevas.cl; eduardo.gajardo@aguasnuevas.cl '
    #mail.to='romina.cinto@aguasnuevas.cl;griselda.aburto@aguasnuevas.cl'
    #mail.cc='manuel.rodriguez@aguasnuevas.cl;jorge.flores@aguasnuevas.cl;'
    for attachment in adjuntos:
        mail.Attachments.Add(attachment)
    #mail.Attachments.Add(lista)
    mail.Subject='Alerta descarga Boton de pago Banco Estado Compra Aqui'
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
    Se ha ejecutado correctamente el bot de descarga Boton de Pago del Banco Estado Compra Aqui. Se adjuntan los archivos correspondientes. 
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