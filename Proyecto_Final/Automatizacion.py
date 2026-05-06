import boto3
import datetime

# Inicializar clientes de AWS
s3_client = boto3.client('s3')
ec2_client = boto3.client('ec2', region_name='us-east-1') 
cw_client = boto3.client('cloudwatch', region_name='us-east-1')

# REEMPLAZA ESTO con tu bucket
bucket_name = 'bucket-datos-equipo-AQUI_LOS_NUMEROS' 
file_name = 'reporte_recursos_aws.txt'

# Iniciar el texto del reporte
reporte = "=== REPORTE AUTOMÁTICO DE RECURSOS AWS ===\n"
reporte += f"Fecha de generación: {datetime.datetime.now()}\n\n"

# 1. Listar Instancias EC2
reporte += "--- 1. INSTANCIAS EC2 ACTIVAS ---\n"
response_ec2 = ec2_client.describe_instances()
instancias_activas = []

for reservation in response_ec2['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        state = instance['State']['Name']
        instancias_activas.append(instance_id)
        reporte += f"- ID: {instance_id} | Tipo: {instance['InstanceType']} | Estado: {state}\n"

if not instancias_activas:
    reporte += "- No se encontraron instancias EC2.\n"

# 2. Métricas de CloudWatch (Uso de CPU de la primera instancia)
reporte += "\n--- 2. MÉTRICAS CLOUDWATCH (CPU) ---\n"
if instancias_activas:
    target_instance = instancias_activas[0]
    # Obtener datos de la última hora
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(hours=1)
    
    response_cw = cw_client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': target_instance}],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Average']
    )
    
    if response_cw['Datapoints']:
        cpu_avg = response_cw['Datapoints'][0]['Average']
        reporte += f"- Instancia {target_instance}: Promedio CPU (última hora) = {cpu_avg:.2f}%\n"
    else:
        reporte += f"- Instancia {target_instance}: EC2 recién creada, aún no hay datos suficientes de CPU.\n"

# 3. Listar Buckets y Objetos en S3
reporte += "\n--- 3. ALMACENAMIENTO S3 ---\n"
response_buckets = s3_client.list_buckets()

for bucket in response_buckets['Buckets']:
    b_name = bucket['Name']
    reporte += f"- Bucket: {b_name}\n"
    
    # Listar objetos solo de tu bucket específico para no hacer el reporte gigante
    if b_name == bucket_name:
        try:
            response_objects = s3_client.list_objects_v2(Bucket=b_name)
            if 'Contents' in response_objects:
                for obj in response_objects['Contents']:
                    reporte += f"  -> Objeto adentro: {obj['Key']} ({obj['Size']} bytes)\n"
            else:
                reporte += "  -> (El bucket está vacío)\n"
        except Exception as e:
            reporte += f"  -> (Sin acceso para leer objetos: {e})\n"

# Guardar el reporte en un archivo local en Cloud9
with open(file_name, 'w') as f:
    f.write(reporte)

# Subir el archivo final a S3
try:
    s3_client.upload_file(file_name, bucket_name, file_name)
    print(f"ÉXITO: Se recolectaron los datos y el reporte '{file_name}' se subió a '{bucket_name}'.")
except Exception as e:
    print(f"Error al subir a S3: {e}")