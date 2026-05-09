import boto3
import time

# Inicializar recurso DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tabla = dynamodb.Table('Usuarios')

print("=== INICIANDO OPERACIONES CRUD EN DYNAMODB ===")

# 1. CREATE (Insertar)
print("\n[1. CREATE] Insertando nuevo registro...")
tabla.put_item(
    Item={
        'id_usuario': '1',
        'nombre': 'Diego Serrano',
        'rol': 'Desarrollador Backend',
        'universidad': 'TecMilenio'
    }
)
print("-> ÉXITO: Registro insertado correctamente.")
time.sleep(2) 

# 2. READ (Leer)
print("\n[2. READ] Consultando el registro en la base de datos...")
respuesta_read = tabla.get_item(Key={'id_usuario': '1'})
if 'Item' in respuesta_read:
    print(f"-> ÉXITO: Datos recuperados: {respuesta_read['Item']}")
else:
    print("-> ERROR: No se encontró el registro.")
time.sleep(2)

# 3. UPDATE (Actualizar)
print("\n[3. UPDATE] Modificando el rol del usuario...")
respuesta_update = tabla.update_item(
    Key={'id_usuario': '1'},
    UpdateExpression="set rol = :r",
    ExpressionAttributeValues={':r': 'Arquitecto Cloud y Serverless'},
    ReturnValues="UPDATED_NEW"
)
print(f"-> ÉXITO: Registro actualizado. Nuevos valores: {respuesta_update['Attributes']}")
time.sleep(2)

# 4. DELETE (Eliminar)
print("\n[4. DELETE] Eliminando el registro de prueba para limpiar la tabla...")
tabla.delete_item(Key={'id_usuario': '1'})
print("-> ÉXITO: Registro eliminado exitosamente.")

print("\n=== TODAS LAS OPERACIONES CRUD FUERON COMPLETADAS ===")