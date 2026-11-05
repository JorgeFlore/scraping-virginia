import smtplib
import win32com.client as win32
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from time import sleep


def envio_correo(asunto,mensaje):
    ruta_recibida=r'C:\Scraping\Bot Licencias SAP\archivos'

    contenido = os.listdir(ruta_recibida)
    
    lista_archivos = []
    for fichero in contenido:
        if os.path.isfile(os.path.join(ruta_recibida, fichero)) and fichero.endswith('.csv'):
            lista_archivos.append(fichero)



    outlook=win32.Dispatch("Outlook.Application")
    
    adjuntos=[]
    for i in lista_archivos:
        adjuntos.append(ruta_recibida+"\\"+i)


    mail=outlook.CreateItem(0)


    #mail.to='manuel.rodriguez@aguasnuevas.cl;jorge.flores@aguasnuevas.cl;fabian.cabrera@aguasnuevas.cl'
    mail.cc='manuel.rodriguez@aguasnuevas.cl'
    error=asunto[0:5]
    print(error)
    if asunto[0:5]!="Error":

        for attachment in adjuntos:
            mail.Attachments.Add(attachment)
            
        mail.Subject=asunto
    
        mail.HTMLbody ="""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <style>
                                body { font-family: Arial, sans-serif; line-height: 1.6; }
                                h3 { color: #0d0d0d; }
                                p { color: #0d0d0d; }
                                .highlight { background-color: #ffff99; font-weight: bold; }
                            </style>
                        </head>
                        <body>
                            <p>Estimado usuario,</p>
                            <p>"""+mensaje+"""</p>
                        </body>
                        </html>
                        """
    
    
        mail.Send()
    
    else:

    #mail.Attachments.Add(lista)

        mail.Subject=asunto

        mail.HTMLbody ="""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <style>
                                body { font-family: Arial, sans-serif; line-height: 1.6; }
                                h3 { color: #0d0d0d; }
                                p { color:  #ff0000; }
                                .highlight { background-color: #ffff99; font-weight: bold; }
                            </style>
                        </head>
                        <body>
                            <p>Estimado usuario,</p>
                            <p>"""+mensaje+"""</p>
                        </body>
                        </html>
                        """


        mail.Send()