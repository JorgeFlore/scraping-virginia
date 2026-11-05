import win32com.client

def enviar_correo_fin_empresa(empresa, destinatarios, rutas_descarga, cantidad_archivos, adjuntos=None, cc=None):
    outlook = win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)

    mail.To = ";".join(destinatarios)
    if cc:
        mail.CC = ";".join(cc)
    mail.Subject = f"✅ Proceso finalizado Descarga Decretos- Empresa {empresa}"

    cuerpo = f"Estimados,\n\nEl proceso descarga Decretos Concesiones y Exticiones ha finalizado correctamente  para la empresa: {empresa}.\n\n"

    for tipo in rutas_descarga:
        ruta = rutas_descarga[tipo]
        cantidad = cantidad_archivos.get(tipo, 0)
        cuerpo += f"Tipo documento: {tipo}\nRuta descarga: {ruta}\nArchivos descargados: {cantidad}\n\n"

    cuerpo += "Saludos,\nScript RPA"
    mail.Body = cuerpo

    if adjuntos:
        for archivo in adjuntos:
            mail.Attachments.Add(archivo)

    mail.Send()
    print(f"📧 Correo enviado para la empresa: {empresa}")
