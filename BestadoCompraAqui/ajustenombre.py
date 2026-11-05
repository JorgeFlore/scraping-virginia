import os

def renombrar_archivos():
    carpeta = 'C:\B.Estado - Compra Aqui\descargados'
    inicio = 0   # Posición de inicio
    final = 23   # Posición final

    # 
    # Cambia el directorio actual a la carpeta especificada
    os.chdir(carpeta)
    
    # Itera sobre cada archivo en la carpeta
    for nombre_archivo in os.listdir(carpeta):
        # Verifica si es un archivo
        if os.path.isfile(nombre_archivo):
            # Extrae la parte del nombre del archivo según las posiciones de inicio y final
            nuevo_nombre = nombre_archivo[inicio:final]
            # Renombra el archivo
            os.rename(nombre_archivo, (nuevo_nombre+".TXT"))
            print(f'Renombrado: {nombre_archivo} -> {nuevo_nombre}')

# Ejemplo de uso

