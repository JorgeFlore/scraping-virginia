@echo off
:: Cambia el directorio activo a la carpeta donde está tu script.
:: Es importante usar comillas por si la ruta tiene espacios.
cd "C:\Scraping\FactoringPDF"

:: Ejecuta el script de Python.
:: Reemplaza "mi_script.py" con el nombre de tu archivo.
python factoringPDF.py

:: Pausa la ventana para que no se cierre automáticamente.
exit

