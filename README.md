# Proyecto DevOps - Soluciones Tecnológicas del Futuro

Este es el repositorio que se utilizará para el avance de Proyecto de DevOps. Contiene el código fuente, los scripts de automatización, los archivos que se ejecutarán en la CLI de AWS y las plantillas de Infraestructura como Código (IaC) para la implementación del entorno automatizado de "Soluciones Tecnológicas del Futuro".

## Estructura del Repositorio

* **`setup_env.sh`**: Script de automatización para instalar dependencias (Git, Docker, Python3).
* **`clean_logs.sh`**: Script de mantenimiento preventivo para limpiar logs antiguos.
* **`infraestructura.yaml`**: Plantilla de CloudFormation para levantar recursos en AWS.
* **`auto_tasklist.py`**: Script en Python (Boto3) para gestión, monitoreo y listado de recursos.
* **`app.py` / `requirements.txt`**: Aplicación web financiera desarrollada en Flask.
* **`Dockerfile` / `docker-compose.yml`**: Archivos de configuración para la contenerización multi-stage, redes y volúmenes.
* **`buildspec.yml`**: Instrucciones de construcción para el pipeline CI/CD en AWS CodeBuild.

---

## Instrucciones de Ejecución

### 1. Configuración del Entorno (Linux)
Antes de ejecutar cualquier despliegue, es necesario preparar el servidor instalando las herramientas esenciales. En la terminal de la instancia EC2, una vez obtenidas las credenciales, ejecute:

```bash
chmod +x setup_env.sh
./setup_env.sh