#!/bin/bash

# Variables de configuración
DB_NAME="Libreria"
DB_USER="maureentellez"
DB_HOST="localhost"
BACKUP_DIR="/Users/maureentellez/Documents/Universidad/libreria"
DATE=$(date +%Y%m%d)

# Comando de respaldo
pg_dump -U $DB_USER -h $DB_HOST -F c -b -v -f $BACKUP_DIR/libreria_$DATE.backup $DB_NAME

# Verificar si el respaldo fue exitoso
if [ $? -eq 0 ]; then
  echo "Respaldo de PostgreSQL completado exitosamente."
else
  echo "Error al realizar el respaldo de PostgreSQL."
fi

