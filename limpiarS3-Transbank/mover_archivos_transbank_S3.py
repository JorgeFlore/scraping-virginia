import boto3
import botocore

def mover_archivos():
    s3 = boto3.client('s3')

    bucket_name = 'anbi-web-scraping'
    carpeta_origen = 'transbank/'
    carpeta_destino = 'transbank_backup/'  # Nueva carpeta de destino

    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=carpeta_origen)

        if 'Contents' in response and response['Contents']:
            for obj in response['Contents']:
                archivo_origen = obj['Key']
                archivo_destino = archivo_origen.replace(carpeta_origen, carpeta_destino, 1)

                # Copiar archivo a la nueva ubicación
                s3.copy_object(
                    Bucket=bucket_name,
                    CopySource={'Bucket': bucket_name, 'Key': archivo_origen},
                    Key=archivo_destino
                )

                # Eliminar archivo original
                s3.delete_object(Bucket=bucket_name, Key=archivo_origen)

                print(f"Movido: {archivo_origen} -> {archivo_destino}")

        else:
            print(f"No se encontraron archivos en la carpeta {carpeta_origen}. No se movió nada.")

        # Asegurar que la carpeta de destino existe (S3 no maneja carpetas reales, solo prefijos vacíos)
        s3.put_object(Bucket=bucket_name, Key=carpeta_destino)

    except botocore.exceptions.BotoCoreError as e:
        print(f"Error al interactuar con S3: {str(e)}")
    except botocore.exceptions.ClientError as e:
        print(f"Error en la solicitud a S3: {str(e)}")

# Ejecutar la función
mover_archivos()
