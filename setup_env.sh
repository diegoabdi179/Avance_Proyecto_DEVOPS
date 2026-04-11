#!/bin/bash

echo "Actualizando repositorios..."
sudo apt-get update -y

echo "Instalando Git, Vim, Python3 y Docker..."
sudo apt-get install -y git vim python3 docker.io

echo "Habilitando e iniciando Docker..."
sudo systemctl enable docker
sudo systemctl start docker

echo "Agregando el usuario actual al grupo de Docker..."
sudo usermod -aG docker $USER

echo "¡Instalación completada exitosamente!"
