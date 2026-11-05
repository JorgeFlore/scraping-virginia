import boto3


def limpiar_bancoestado():
    
    s3 = boto3.client('s3')

    bucket_name = 'anbi-web-scraping'
    carpeta = 'botonpago/bancoestado/'

    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=carpeta)
    
    if 'Contents' in response:
        objetos_a_eliminar = [{'Key': obj['Key']} for obj in response['Contents']]


        delete_response = s3.delete_objects(
            Bucket=bucket_name,
            Delete={
                'Objects': objetos_a_eliminar
            }
        )

        print(f"Archivos eliminados en la carpeta {carpeta} del bucket {bucket_name}.")
    else:
        print(f"No se hizo nada")

    s3.put_object(Bucket = bucket_name, Key = carpeta)



def limpiar_bancoChile():
    
    s3 = boto3.client('s3')

    bucket_name = 'anbi-web-scraping'
    carpeta = 'botonpago/bchile/'

    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=carpeta)
    
    if 'Contents' in response:
        objetos_a_eliminar = [{'Key': obj['Key']} for obj in response['Contents']]


        delete_response = s3.delete_objects(
            Bucket=bucket_name,
            Delete={
                'Objects': objetos_a_eliminar
            }
        )

        print(f"Archivos eliminados en la carpeta {carpeta} del bucket {bucket_name}.")
    else:
        print(f"No se hizo nada")

    s3.put_object(Bucket = bucket_name, Key = carpeta)
