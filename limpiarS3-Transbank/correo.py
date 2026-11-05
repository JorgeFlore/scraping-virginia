from os import scandir, getcwd
import os
import win32com.client as win32
from datetime import datetime, timedelta

def envio_correo():  
  
    outlook=win32.Dispatch("Outlook.Application")
       
    mail=outlook.CreateItem(0)

    mail.to='jorge.flores@aguasnuevas.cl;manuel.rodriguez@aguasnuevas.cl'
    mail.Subject='Alerta Limpieza Transbank'
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
     Se ha ejecutado correctamente el bot de Limpieza Transbank en S3. 
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