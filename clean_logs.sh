#!/bin/bash

echo "Iniciando limpieza de logs del sistema..."
sudo journalctl --vacuum-time=3d
echo "Limpieza completada: $(date)" >> /home/ubuntu/historial_limpieza.log
