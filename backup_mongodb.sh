#!/bin/bash

# Variables de configuración
MONGO_URI="mongodb+srv://maureenbarra16:PopiMauLuna1677@cluster0.ifap9.mongodb.net/libreria?retryWrites=true&w=majority"
BACKUP_DIR="/Users/maureentellez/Documents/Universidad/libreria"
DATE=$(date +%Y%m%d)  # Genera la fecha actual en formato YYYYMMDD

# Crear el directorio de respaldo si no existe
if [ ! -d "$BACKUP_DIR/$DATE" ]; then
  mkdir -p "$BACKUP_DIR/$DATE"
fi

# Comando de respaldo usando mongodump
mongodump --uri="$MONGO_URI" --out "$BACKUP_DIR/$DATE"

# Verificar si el respaldo fue exitoso
if [ $? -eq 0 ]; then
  echo "Respaldo de MongoDB completado exitosamente."
else
  echo "Error al realizar el respaldo de MongoDB."
fi

