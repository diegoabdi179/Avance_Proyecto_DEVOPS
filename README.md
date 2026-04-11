Proyecto DevOps - Soluciones Tecnológicas del Futuro
Este es el repositorio que se utilizará para el avance de Proyecto de DevOps. Contiene el código fuente, los scripts de automatización, los archivos que se ejecutarán en la CLI de AWS y las plantillas de Infraestructura como Código (IaC) para la implementación del entorno automatizado de Soluciones Tecnológicas del Futuro.

Estructura del Repositorio

setup_env.sh: Script de automatización para instalar dependencias (Git, Docker, Python3).

clean_logs.sh: Script de mantenimiento preventivo para limpiar logs antiguos.

infraestructura.yaml: Plantilla de CloudFormation para levantar recursos en AWS.

auto_tasklist.py: Script en Python (Boto3) para gestión, monitoreo y listado de recursos.

app.py / requirements.txt: Aplicación web financiera desarrollada en Flask.

Dockerfile / docker-compose.yml: Archivos de configuración para la contenerización multi-stage, redes y volúmenes.

buildspec.yml: Instrucciones de construcción para el pipeline CI/CD en AWS CodeBuild.

Instrucciones de Ejecución

Configuración del Entorno (Linux)
Antes de ejecutar cualquier despliegue, es necesario preparar el servidor instalando las herramientas esenciales. En la terminal de la instancia EC2, una vez obtenidas las credenciales, ejecute:

chmod +x setup_env.sh
./setup_env.sh

Despliegue de Infraestructura (CloudFormation)
El siguiente bloque de comandos será el que se tenga que ejecutar en la CLI de AWS para desplegar los servidores y buckets:

aws cloudformation deploy

--template-file infraestructura.yaml

--stack-name ProyectoDevOpsStack

--region us-east-1

--role-arn arn:aws:iam::TU_NUMERO_DE_CUENTA:role/LabRole

Explicación de parámetros:

--template-file: Le indicamos a la CLI dónde están nuestras instrucciones (que en este caso es el archivo .yaml).
--stack-name: Junta las instancias y buckets en un grupo lógico para que se puedan borrar y no tengamos problemas después.
--region us-east-1: Especifica la región donde tendremos prendidas nuestras instancias.
--role-arn: Parámetro crítico para AWS Learner Lab. Al usar una cuenta estándar en AWS, CloudFormation hereda los permisos del administrador que ejecuta un comando. Como sabemos, AWS Learner Lab tiene límites de seguridad que nos impiden crear roles IAM o ejecutar despliegues de CloudFormation utilizando credenciales de usuario por defecto. Por lo tanto, el agujero legal que utilizaremos es --role-arn; este indica a CloudFormation que no use las credenciales del usuario actual y que asuma los permisos de un rol específico que los administradores del lab ya preconfiguraron y autorizaron.
ARN (Amazon Resource Name): Es la nomenclatura estándar de AWS para identificar de manera unívoca cualquier recurso en la nube. Es la ruta absoluta hacia el permiso.
TU_NUMERO_DE_CUENTA: Representa el ID único de 12 dígitos de la cuenta de AWS donde se realiza el despliegue (este valor debe sustituirse por el ID real antes de ejecutar el script).
role/LabRole: Es el rol oficial y pre-aprobado del Learner Lab. Contiene exactamente los permisos necesarios para aprovisionar las instancias EC2 y los buckets de S3 requeridos.

Nota: Omitir el parámetro --role-arn o intentar definir políticas de IAM desde cero dentro de la plantilla YAML resultará invariablemente en un error AccessDenied debido a las restricciones de la organización de AWS Academy/Educate.

Automatización y Monitoreo (Python)
Para comenzar el monitoreo de uso de CPU, listado de instancias y auditoría de buckets S3, ejecute el siguiente comando:

python3 auto_tasklist.py

Contenerización de la Aplicación (Docker)
Para levantar la aplicación web aislada en su contenedor con la red y volúmenes configurados, ejecute:

sudo docker-compose up --build -d

Verifique el despliegue accediendo localmente mediante curl localhost:80.