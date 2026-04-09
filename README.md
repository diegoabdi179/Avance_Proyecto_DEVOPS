# Avance_Proyecto_DEVOPS
Este es el repositorio que se utilizara para el avance de Proyecto de DevOps
Contendrá los archivos que se ejecutaran en el CLI de AWS

El siquiente bloque de comandos sera el que se tenga que ejecutar en el EC2 una vez obtenidas las credenciales:

aws cloudformation deploy \
  --template-file infraestructura.yaml \
  --stack-name ProyectoDevOpsStack \
  --region us-east-1 \
  --role-arn arn:aws:iam::TU_NUMERO_DE_CUENTA:role/LabRole

aws cloudformation deploy \   -Indicaremos que queremos utilizar CloudFormation para desplegar infraestructura
  --template-file infraestructura.yaml \ -Le indicamos al CLI donde estan nuestras instruccione sque en este caso es el archivo .yaml
  --stack-name ProyectoDevOpsStack \ -Junta las instancias y buckets en un grupo para que se puedan borrar y no tengamos problemas después
  --region us-east-1 \ -Donde tendremos prendidas nuestras instancias
  --role-arn arn:aws:iam::TU_NUMERO_DE_CUENTA:role/LabRole

La explciación al último comando es la siguiente:
Al usar una cuenta estándar en AWS, Cloudformation hereda los permisos del administrador que ejecuta un comando. Como sabemos, "AWS Learner Lab" tiene límites de seguridad que nos impiden crear roles IAM o ejecutar despliegues de CloudFormation utilizando credenciales de usuario por defecto. Por lo tanto, el agujero legal que utilizaremos es "--role-arn", este indica a CloudFormation que no use las credenciales del usuario actual y que asuma los permisos de un rol específico que los administradores de lab ya preconfiguraron y autorizaron.

-ARN (Amazon Resource Name): Es la nomenclatura estándar de AWS para identificar de manera unívoca cualquier recurso en la nube. Es la "ruta absoluta" hacia el permiso.
-TU_NUMERO_DE_CUENTA: Representa el ID único de 12 dígitos de la cuenta de AWS donde se realiza el despliegue (este valor debe sustituirse por el ID real antes de ejecutar el script).
-role/LabRole: Es el rol oficial y pre-aprobado del Learner Lab. Contiene exactamente los permisos necesarios para aprovisionar las instancias EC2 y los buckets de S3 requeridos para el proyecto.

Omitir el parámetro `--role-arn` o intentar definir políticas de IAM desde cero dentro de la plantilla YAML resultará invariablemente en un error `AccessDenied` debido a las restricciones de la organización de AWS Academy/Educate.
