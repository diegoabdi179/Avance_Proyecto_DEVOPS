import boto3
import datetime

# Inicializamos los clientes de AWS
ec2_client = boto3.client('ec2', region_name='us-east-1')
cw_client = boto3.client('cloudwatch', region_name='us-east-1')
s3_client = boto3.client('s3', region_name='us-east-1')
asg_client = boto3.client('autoscaling', region_name='us-east-1')

# 1. Listado de instancias EC2

def listar_instancias():
    print("\n--- LISTANDO DE INSTANCIAS EC2 ---")
    response = ec2_client.describe_instances()
    instancias_activas = []
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            instance_type = instance['InstanceType']
            
            # Sacar el nombre si tiene la etiqueta "Name"
            name = "Sin Nombre"
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        name = tag['Value']
                        
            print(f"Instancia: {name} | ID: {instance_id} | Tipo: {instance_type} | Estado: {state}")
            
            if state == 'running':
                instancias_activas.append(instance_id)
                
    return instancias_activas


# 2. Reporte de uso CloudWatch

def reporte_uso_ec2(instancias):
    print("\n--- REPORTE DE USO DE CPU (ÚLTIMA HORA) ---")
    if not instancias:
        print("No hay instancias corriendo para sacar métricas.")
        return

    # Definimos el rango de tiempo 
    end_time = datetime.datetime.now(datetime.timezone.utc)
    start_time = end_time - datetime.timedelta(hours=1)

    for instance_id in instancias:
        response = cw_client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600, # Promedio de toda la hora (3600 segundos)
            Statistics=['Average']
        )
        
        datapoints = response['Datapoints']
        if datapoints:
            promedio_cpu = datapoints[0]['Average']
            print(f"Instancia {instance_id} -> Consumo de CPU: {promedio_cpu:.2f}%")
        else:
            print(f"Instancia {instance_id} -> Sin datos recientes de CPU.")


# 3. Listar Buckets de S3 y sus objetos

def listar_s3():
    print("\n--- LISTANDO BUCKETS Y OBJETOS S3 ---")
    response_buckets = s3_client.list_buckets()
    
    for bucket in response_buckets['Buckets']:
        bucket_name = bucket['Name']
        print(f"\nBucket: {bucket_name}")
        
        # Obtenemos los objetos dentro de cada bucket
        response_objects = s3_client.list_objects_v2(Bucket=bucket_name)
        
        if 'Contents' in response_objects:
            for obj in response_objects['Contents']:
                print(f"  - {obj['Key']} ({obj['Size']} bytes)")
        else:
            print("  (Bucket vacío)")


# 4. Gestionar Auto Scaling (Límites Learner Lab)

def ajustar_auto_scaling(nombre_asg, capacidad_deseada, max_size):
    print(f"\n--- GESTIONANDO AUTO SCALING: {nombre_asg} ---")
    
    # Límite de 9 instancias totales
    LIMITE_LAB = 9 
    if max_size > LIMITE_LAB:
        print(f"No se permiten más de {LIMITE_LAB} instancias en total.")
        print("Ajustando MaxSize al límite seguro...")
        max_size = LIMITE_LAB

    try:
        asg_client.update_auto_scaling_group(
            AutoScalingGroupName=nombre_asg,
            MinSize=1,
            MaxSize=max_size,
            DesiredCapacity=capacidad_deseada
        )
        print(f"Auto Scaling Group '{nombre_asg}' actualizado con éxito.")
        print(f"Capacidad Deseada: {capacidad_deseada} | Máximo: {max_size}")
    except Exception as e:
        print(f"Error al actualizar ASG: {e}")

if __name__ == '__main__':
    # 1. Sacamos las instancias y guardamos las que están corriendo
    instancias_corriendo = listar_instancias()
    
    # 2. Generamos el reporte de esas instancias
    reporte_uso_ec2(instancias_corriendo)
    
    # 3. Revisamos qué hay en S3
    listar_s3()
    
    # 4. Configurar Auto Scaling (Descomenta y pon el nombre real de tu ASG para usarlo)
    nombre_de_tu_asg = "MiGrupoAutoScaling"
    ajustar_auto_scaling(nombre_de_tu_asg, capacidad_deseada=2, max_size=4)