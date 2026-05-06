import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tabla = dynamodb.Table('Usuarios')

# 1. Insertar registro
tabla.put_item(
    Item={
        'id_usuario': '1',
        'nombre': 'Diego',
        'rol': 'Desarrollador'
    }
)

# 2. Modificar registro
tabla.update_item(
    Key={'id_usuario': '1'},
    UpdateExpression="set rol = :r",
    ExpressionAttributeValues={':r': 'Administrador'},
    ReturnValues="UPDATED_NEW"
)

# 3. Eliminar registro
tabla.delete_item(
    Key={'id_usuario': '1'}
)