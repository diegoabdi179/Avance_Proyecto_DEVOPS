import boto3
import time

# Inicializar recurso DynamoDB en la región correcta
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tabla = dynamodb.Table('Usuarios')

print("=== INICIANDO OPERACIONES CRUD EN DYNAMODB ===")

print("\n1. Insertando registro...")
tabla.put_item(
    Item={
        'id_usuario': '1',
        'nombre': 'Diego',
        'rol': 'Desarrollador Backend'
    }
)
print("-> Registro insertado correctamente.")
time.sleep(2) 

print("\n2. Modificando registro...")
respuesta = tabla.update_item(
    Key={'id_usuario': '1'},
    UpdateExpression="set rol = :r",
    ExpressionAttributeValues={':r': 'Arquitecto Cloud'},
    ReturnValues="UPDATED_NEW"
)
print(f"-> Registro actualizado. Nuevos datos: {respuesta['Attributes']}")
time.sleep(2)

print("\n3. Eliminando registro...")
tabla.delete_item(Key={'id_usuario': '1'})
print("-> Registro eliminado exitosamente.")

print("\n=== OPERACIONES FINALIZADAS ===")