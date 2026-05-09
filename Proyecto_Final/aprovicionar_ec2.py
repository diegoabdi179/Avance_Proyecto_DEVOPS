import boto3
from datetime import datetime

ec2 = boto3.resource('ec2', region_name='us-east-1')
ec2_client = boto3.client('ec2', region_name='us-east-1')

def contar_instancias_activas():
    respuesta = ec2_client.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'pending', 'stopped']}]
    )
    total = sum(len(r['Instances']) for r in respuesta['Reservations'])
    return total

def aprovisionar_instancia():
    total = contar_instancias_activas()
    print(f"Instancias activas actualmente: {total}/9")

    if total >= 9:
        print("LIMITE ALCANZADO: No se puede crear mas instancias en Learner Lab.")
        return

    timestamp = datetime.now().strftime("%Y%m%d-%H%M")

    instancias = ec2.create_instances(
        ImageId='ami-0c02fb55956c7d316',
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        IamInstanceProfile={'Name': 'LabInstanceProfile'},
        NetworkInterfaces=[{
            'SubnetId': 'subnet-04e78fd44e8e373b1',
            'DeviceIndex': 0,
            'AssociatePublicIpAddress': True,
            'Groups': ['sg-01834b9cc02fdc8eb']
        }],
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [
                {'Key': 'Name', 'Value': f'EC2-aprovisionada-{timestamp}'},
                {'Key': 'Proyecto', 'Value': 'DevOps-Fase1'},
                {'Key': 'Integrante', 'Value': 'Integrante1-Isaac'}
            ]
        }]
    )

    instancia = instancias[0]
    print(f"\nInstancia creada exitosamente")
    print(f"   ID:     {instancia.id}")
    print(f"   Tipo:   {instancia.instance_type}")
    print(f"   Estado: pending → running en ~30 segundos")
    print(f"   Tag:    EC2-aprovisionada-{timestamp}")

    print("\nEsperando que la instancia llegue a estado running...")
    instancia.wait_until_running()
    instancia.reload()
    print(f"   IP Publica: {instancia.public_ip_address}")
    print(f"\nTotal instancias ahora: {contar_instancias_activas()}/9")

aprovisionar_instancia()
