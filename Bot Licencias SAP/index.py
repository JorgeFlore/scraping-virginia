#libraries you'll need 
import win32com.client
from time import sleep
import win32com.client as win32
from pywinauto import Application
import convertir_excel
import correos
from glob import glob
import pyautogui
import os

ruta=r"C:\Scraping\Bot Licencias SAP\archivos"


for archivo in glob(ruta+'\\*'):
    os.remove(archivo)

try:
    app = Application().start(r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe")
    sleep(5)
    sap_gui_auto = win32com.client.GetObject("SAPGUI")

    application = sap_gui_auto.GetScriptingEngine
    #connection = application.OpenConnection("SAP QA", True)
    connection = application.OpenConnection("SAP Produccion", True)
    connection2 = application.Children(0)
    sleep(2)
    session = connection2.Children(0)
    print(connection)

    session.findById("wnd[0]/usr/txtRSYST-BNAME").text = "bot_rpa_v2"
    #session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = "Bot08012025."
    session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = "Bot_rpa2102.."
    session.findById("wnd[0]").sendVKey(0)

    session.findById("wnd[0]").maximize
    session.findById("wnd[0]/tbar[0]/okcd").text = "USMM"
    session.findById("wnd[0]").sendVKey(0)
    sleep(2)

    session.findById("wnd[0]/tbar[1]/btn[18]").press()  # Botón "Lista completa"
    session.findById("wnd[0]").maximize()
    sleep(2)
    session.findById("wnd[0]/usr/cntlSLIM_USER_CONTAINER/shellcont/shell").pressToolbarContextButton("&MB_EXPORT")

    session.findById("wnd[0]/usr/cntlSLIM_USER_CONTAINER/shellcont/shell").selectContextMenuItem("&PC")

    session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[3,0]").select()
    session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[3,0]").setFocus()


    session.findById("wnd[1]/tbar[0]/btn[0]").press()

    session.findById("wnd[1]/usr/ctxtDY_PATH").text = ruta

    session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = "usuarios.htm"
    session.findById("wnd[1]/usr/ctxtDY_FILENAME").caretPosition = 12

    session.findById("wnd[1]").sendVKey(0)

    convertir_excel.obtener_csv()
    sleep(2)
    asunto="Reporte Finalización Bot Licencias SAP"
    mensaje="Se ha ejecutado correctamente el Bot de licencias SAP"  
    convertir_excel.obtener_csv()
    sleep(2)
    asunto="Reporte Finalización Bot Licencias SAP"
    mensaje="Se ha ejecutado correctamente el Bot de licencias SAP."  
    correos.envio_correo(asunto,mensaje)
    session.findById("wnd[0]").close()

    
    session.findById("wnd[1]/usr/btnSPOP-OPTION1").press()
    pyautogui.hotkey('alt','f4')
    
  
except Exception as e:
    asunto="Error Bot Licencias SAP"
    mensaje="Ha ocurrido un error en la ejecución del Bot Licencias SAP, favor ejecutar nuevamente. "+str(e)
    session.findById("wnd[0]").close()

    sleep(5)
    #session.findById("wnd[1]/usr/btnSPOP-OPTION1").press()
    pyautogui.hotkey('alt','f4')
    correos.envio_correo(asunto,mensaje)
    
