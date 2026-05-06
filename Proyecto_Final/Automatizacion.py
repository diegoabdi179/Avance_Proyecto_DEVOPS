import boto3
import os

# Definir variables
bucket_name = 'nombre-unico-para-tu-bucket-12345'
file_name = 'reporte_automatico.txt'

# Crear un archivo de prueba localmente
with open(file_name, 'w') as f:
    f.write("Este archivo fue generado y subido automáticamente mediante boto3.")

# Inicializar cliente S3 y subir archivo
s3 = boto3.client('s3')
try:
    s3.upload_file(file_name, bucket_name, file_name)
    print(f"Éxito: Archivo '{file_name}' cargado a '{bucket_name}'.")
except Exception as e:
    print(f"Error en la automatización: {e}")