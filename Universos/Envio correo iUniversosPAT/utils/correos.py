import win32com.client as win32
import os
from time import sleep
import pandas as pd
import numpy as np
import openpyxl


def envio_correo(ruta,empresa,rut):
    ruta_recibida=ruta
    
    contenido = os.listdir(ruta_recibida)
    lista_archivos = []
    tabla_html = '<table border="1", bordercolor="black", cellspacing="0">'
    for fichero in contenido:
        xlsx_file = ruta_recibida+fichero
        
        if os.path.isfile(os.path.join(ruta_recibida, fichero)) and rut in fichero:
            lista_archivos.append(fichero)
            if fichero.endswith('.xlsx'): 
                wb = openpyxl.load_workbook(xlsx_file)
                sheet = wb.active
                for i, row in enumerate(sheet.iter_rows(values_only=True)):
                    if None in row:
                        continue
                    if i == 0:
        # Aplicar estilo diferente a la primera fila
                        tabla_html += '<tr style="background-color: #007b91; color:  white;"><strong>'
                    else:
                        tabla_html += '<tr>'
                    for cell in row:
                        tabla_html += f'<td style="text-align: center;">{cell}</td>'
                    tabla_html += '</tr>'
                tabla_html+='</table>'
                print(tabla_html)
    print(lista_archivos)


    outlook=win32.Dispatch("Outlook.Application")
    
    adjuntos=[]
    for i in lista_archivos:
        adjuntos.append(ruta+i)


    mail=outlook.CreateItem(0)

    mail.to='griselda.aburto@aguasnuevas.cl;karol.alvarado@aguasnuevas.cl'
    mail.cc='jorge.flores@aguasnuevas.cl;manuel.rodriguez@aguasnuevas.cl;rodrigo.endara@aguasnuevas.cl;fabian.cabrera@aguasnuevas.cl'
    #mail.to='jorge.flores@aguasnuevas.cl'
    for attachment in adjuntos:
        mail.Attachments.Add(attachment)

    #mail.Attachments.Add(lista)

    mail.Subject='Información de Carga de Universos PAT  '+empresa

    mail.HTMLbody =r"""<div>
    <table>
    <tbody>
    <tr>
    <td>
    <table width="100%" style="height:58px">
    <tbody><tr>
    <td style="width:850px;text-align:left"> 
    </tr>
    <tr>
    <td style="width:850px;text-align:left"><strong>Información de Carga de Universos PAT de """ +""" """+empresa+""" <br>
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
    Se ha ejecutado correctamente el bot de descarga de información de Carga de Universos PAT de """+empresa+""". Se adjuntan los archivos correspondientes. 
    </td>
    <br>
    <td>
    </td>
    </tr>
    <br>
    <tr>
    """+tabla_html+""" 
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