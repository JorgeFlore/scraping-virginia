from os import scandir, getcwd
import os
import win32com.client as win32
from datetime import datetime, timedelta

def envio_correo():  
    ruta_archivos="\\\\columbia\\cargas_masivas\\recaudacion_pac_pat\\"
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
    mensaje = "Los archivos movidos son: <br>"
    print(format)
    contador = 0
    for fichero in contenido:
        if os.path.isfile(os.path.join(ruta_archivos, fichero)):
            #lista_archivos.append(fichero)
            mensaje += f"{fichero}    '<br>"
            contador +=1
    print(contador)
    
    
    outlook=win32.Dispatch("Outlook.Application")
        #correos=['manuel.rodriguez.sandoval2@gmail.com','manuel.rodriguez@aguasnuevas.cl']
        #lista_archivos
  
    
    #for i in lista_archivos:
        #if (format in i):
       # adjuntos.append(ruta_archivos+'\\'+i)
    mail=outlook.CreateItem(0)
    #print(os.listdir())
    #for i in correos:
        #mail.To=correos:
    
    mail.to='jorge.flores@aguasnuevas.cl;manuel.rodriguez@aguasnuevas.cl'
    #mail.cc='manuel.rodriguez@aguasnuevas.cl;jorge.flores@aguasnuevas.cl;fabian.cabrera@aguasnuevas.cl;rodrigo.endara@aguasnuevas.cl; eduardo.gajardo@aguasnuevas.cl; '
    #mail.to='romina.cinto@aguasnuevas.cl;griselda.aburto@aguasnuevas.cl'
    #mail.cc='manuel.rodriguez@aguasnuevas.cl;jorge.flores@aguasnuevas.cl;fabian.cabrera@aguasnuevas.cl;rodrigo.endara@aguasnuevas.cl'
    for attachment in adjuntos:
        mail.Attachments.Add(attachment)
    #mail.Attachments.Add(lista)
    mail.Subject='Alerta Limpieza S3 y PAC-PAT'
    mail.HTMLbody =f"""<div>
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
     Se ha ejecutado correctamente el bot de Limpieza S3 y PAC-PAT. Se movieron {contador} archivos. 
    <br>
    {mensaje}
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