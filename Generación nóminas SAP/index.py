import win32com.client
from time import sleep
import win32com.client as win32
from pywinauto import Application
from glob import glob
import pyautogui
import os


#ruta=r"C:\pruebas"



try:
    app = Application().start(r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe")
    sleep(5)
    sap_gui_auto = win32com.client.GetObject("SAPGUI")

    application = sap_gui_auto.GetScriptingEngine
    connection = application.OpenConnection("SAP QA", True)
    connection2 = application.Children(0)
    sleep(2)
    session = connection2.Children(0)
    print(connection)
    sleep(2)
    session.findById("wnd[0]").maximize
    session.findById("wnd[0]/usr/txtRSYST-BNAME").text = "bot_rpa_v2"
    #sleep(1)
    session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = "Bot08012025.."
    #Bot08012025.. qa
    #Bot_rpa0403.. prod
    session.findById("wnd[0]").sendVKey(0)
    
    session.findById("wnd[0]").maximize
    session.findById("wnd[0]/tbar[0]/okcd").text = "fbl1n"
    session.findById("wnd[0]").sendVKey(0)
    session.findById("wnd[0]").maximize
    session.findById("wnd[0]/usr/ctxtKD_BUKRS-LOW").text = "ATA"
    pyautogui.hotkey('f8')
    session.findById("wnd[0]/tbar[1]/btn[38]").press
    sleep(2)
except Exception as e:
    print(e)
    
    
    # Redimensionar la ventana de trabajo
session.findById("wnd[0]").resizeWorkingPane(233, 57, False)  # Cambiar tamaño de la ventana

# Hacer clic en el botón "Fijar filtros" (botón con ID 'btn[38]')
session.findById("wnd[0]/tbar[1]/btn[38]").press()

# Hacer clic en el botón de búsqueda
session.findById("wnd[1]/usr/btnB_SEARCH").press()

# Buscar "cuenta de mayor"
session.findById("wnd[2]/usr/txtGD_SEARCHSTR").text = "cuenta de mayor"
session.findById("wnd[2]/usr/txtGD_SEARCHSTR").caretPosition = 15
session.findById("wnd[2]").sendVKey(0)  # Presionar tecla Enter

# Aplicar la búsqueda
session.findById("wnd[1]/usr/btnAPP_WL_SING").press()

# Hacer clic en el botón de búsqueda nuevamente
session.findById("wnd[1]/usr/btnB_SEARCH").press()

# Buscar "nombre del usuario"
session.findById("wnd[2]/usr/txtGD_SEARCHSTR").text = "nombre del usuario"
session.findById("wnd[2]/usr/txtGD_SEARCHSTR").caretPosition = 18
session.findById("wnd[2]").sendVKey(0)  # Presionar tecla Enter

# Aplicar la búsqueda
session.findById("wnd[1]/usr/btnAPP_WL_SING").press()

# Hacer clic en el botón de búsqueda nuevamente
session.findById("wnd[1]/usr/btnB_SEARCH").press()

# Buscar "bloqueo de pago"
session.findById("wnd[2]/usr/txtGD_SEARCHSTR").text = "bloqueo de pago"
session.findById("wnd[2]/usr/txtGD_SEARCHSTR").caretPosition = 15
session.findById("wnd[2]").sendVKey(0)  # Presionar tecla Enter

# Aplicar la búsqueda
session.findById("wnd[1]/usr/btnAPP_WL_SING").press()

# Confirmar la acción con el botón "Aceptar"
session.findById("wnd[1]/tbar[0]/btn[0]").press()

# Fijar filtro en "Cuenta de mayor"
session.findById("wnd[1]/usr/ssub%_SUBSCREEN_FREESEL:SAPLSSEL:1105/btn%_%%DYN001_%_APP_%-VALU_PUSH").press()
session.findById("wnd[2]/usr/tabsTAB_STRIP/tabpNOSV").select()
session.findById("wnd[2]/usr/tabsTAB_STRIP/tabpNOSV/ssubSCREEN_HEADER:SAPLALDB:3030/tblSAPLALDBSINGLE_E/ctxtRSCSEL_255-SLOW_E[1,0]").text = "11030005"
session.findById("wnd[2]/usr/tabsTAB_STRIP/tabpNOSV/ssubSCREEN_HEADER:SAPLALDB:3030/tblSAPLALDBSINGLE_E/ctxtRSCSEL_255-SLOW_E[1,0]").caretPosition = 8
session.findById("wnd[2]").sendVKey(0)

# Fijar filtro en "Cuenta contable"
session.findById("wnd[2]/usr/tabsTAB_STRIP/tabpNOSV/ssubSCREEN_HEADER:SAPLALDB:3030/tblSAPLALDBSINGLE_E/ctxtRSCSEL_255-SLOW_E[1,1]").text = "21020004"
session.findById("wnd[2]/usr/tabsTAB_STRIP/tabpNOSV/ssubSCREEN_HEADER:SAPLALDB:3030/tblSAPLALDBSINGLE_E/ctxtRSCSEL_255-SLOW_E[1,1]").setFocus()
session.findById("wnd[2]/usr/tabsTAB_STRIP/tabpNOSV/ssubSCREEN_HEADER:SAPLALDB:3030/tblSAPLALDBSINGLE_E/ctxtRSCSEL_255-SLOW_E[1,1]").caretPosition = 8
session.findById("wnd[2]").sendVKey(0)

# Confirmar y volver al proceso principal
session.findById("wnd[2]/tbar[0]/btn[0]").press()
session.findById("wnd[2]/tbar[0]/btn[8]").press()

# Fijar filtro en "Soporte"
session.findById("wnd[1]/usr/ssub%_SUBSCREEN_FREESEL:SAPLSSEL:1105/ctxt%%DYN002-LOW").setFocus()
session.findById("wnd[1]/usr/ssub%_SUBSCREEN_FREESEL:SAPLSSEL:1105/ctxt%%DYN002-LOW").caretPosition = 0
session.findById("wnd[1]/usr/ssub%_SUBSCREEN_FREESEL:SAPLSSEL:1105/btn%_%%DYN002_%_APP_%-VALU_PUSH").press()

# Fijar filtro en "Usuario"
session.findById("wnd[2]/usr/tabsTAB_STRIP/tabpNOSV").select()
session.findById("wnd[2]/usr/tabsTAB_STRIP/tabpNOSV/ssubSCREEN_HEADER:SAPLALDB:3030/tblSAPLALDBSINGLE_E/ctxtRSCSEL_255-SLOW_E[1,0]").text = "soporte_sy"
session.findById("wnd[2]/usr/tabsTAB_STRIP/tabpNOSV/ssubSCREEN_HEADER:SAPLALDB:3030/tblSAPLALDBSINGLE_E/ctxtRSCSEL_255-SLOW_E[1,0]").caretPosition = 10
session.findById("wnd[2]").sendVKey(0)

# Fijar filtro en "Usuario SAP"
session.findById("wnd[2]/usr/tabsTAB_STRIP/tabpNOSV/ssubSCREEN_HEADER:SAPLALDB:3030/tblSAPLALDBSINGLE_E/ctxtRSCSEL_255-SLOW_E[1,1]").text = "sap_an"
session.findById("wnd[2]/usr/tabsTAB_STRIP/tabpNOSV/ssubSCREEN_HEADER:SAPLALDB:3030/tblSAPLALDBSINGLE_E/ctxtRSCSEL_255-SLOW_E[1,1]").setFocus()
session.findById("wnd[2]/usr/tabsTAB_STRIP/tabpNOSV/ssubSCREEN_HEADER:SAPLALDB:3030/tblSAPLALDBSINGLE_E/ctxtRSCSEL_255-SLOW_E[1,1]").caretPosition = 6
session.findById("wnd[2]").sendVKey(0)

# Confirmar y volver al proceso principal
session.findById("wnd[2]/tbar[0]/btn[0]").press()
session.findById("wnd[2]/tbar[0]/btn[8]").press()

# Fijar filtro en "Aprobación"
session.findById("wnd[1]/usr/ssub%_SUBSCREEN_FREESEL:SAPLSSEL:1105/ctxt%%DYN003-LOW").setFocus()
session.findById("wnd[1]/usr/ssub%_SUBSCREEN_FREESEL:SAPLSSEL:1105/ctxt%%DYN003-LOW").caretPosition = 0
session.findById("wnd[1]/usr/ssub%_SUBSCREEN_FREESEL:SAPLSSEL:1105/btn%_%%DYN003_%_APP_%-VALU_PUSH").press()

# Fijar filtro en "Rango"
session.findById("wnd[2]/usr/tabsTAB_STRIP/tabpNOSV").select()
session.findById("wnd[2]/usr/tabsTAB_STRIP/tabpNOSV/ssubSCREEN_HEADER:SAPLALDB:3030/tblSAPLALDBSINGLE_E/ctxtRSCSEL_255-SLOW_E[1,0]").text = "a"
session.findById("wnd[2]/usr/tabsTAB_STRIP/tabpNOSV/ssubSCREEN_HEADER:SAPLALDB:3030/tblSAPLALDBSINGLE_E/ctxtRSCSEL_255-SLOW_E[1,0]").caretPosition = 1
session.findById("wnd[2]").sendVKey(0)

# Fijar filtro en "Rango de tipo"
session.findById("wnd[2]/usr/tabsTAB_STRIP/tabpNOSV/ssubSCREEN_HEADER:SAPLALDB:3030/tblSAPLALDBSINGLE_E/ctxtRSCSEL_255-SLOW_E[1,1]").text = "r"
session.findById("wnd[2]/usr/tabsTAB_STRIP/tabpNOSV/ssubSCREEN_HEADER:SAPLALDB:3030/tblSAPLALDBSINGLE_E/ctxtRSCSEL_255-SLOW_E[1,1]").setFocus()
session.findById("wnd[2]/usr/tabsTAB_STRIP/tabpNOSV/ssubSCREEN_HEADER:SAPLALDB:3030/tblSAPLALDBSINGLE_E/ctxtRSCSEL_255-SLOW_E[1,1]").caretPosition = 1
session.findById("wnd[2]").sendVKey(0)

# Confirmar y volver al proceso principal
session.findById("wnd[2]/tbar[0]/btn[0]").press()
session.findById("wnd[2]/tbar[0]/btn[8]").press()

#confirmar todos los filtros
session.findById("wnd[1]/tbar[0]/btn[0]").press()



#pyautogui.hotkey('f9')
session.findById("wnd[0]").resizeWorkingPane(233, 57, False)
session.findById("wnd[0]/mbar/menu[0]/menu[3]/menu[2]").select()
session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[3,0]").select()
session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[3,0]").setFocus()
session.findById("wnd[1]/tbar[0]/btn[0]").press()
session.findById("wnd[1]/usr/ctxtDY_PATH").text = r"C:\Users\manuel.rodriguez\Desktop\Scraping\Generación nóminas SAP"
session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = "export.htm"
session.findById("wnd[1]/usr/ctxtDY_FILENAME").caretPosition = 6
session.findById("wnd[1]/tbar[0]/btn[11]").press()
import convertir_excel

convertir_excel.obtener_csv()