#!/bin/bash

#--------------------------------------------
# Variables para ubicar directorios durante la ejecucion del sistema.
export BASE_DIR=$(cd $(dirname $BASH_SOURCE) && pwd)/..
export SCRIPTS_DIR=$BASE_DIR/scripts
export PYTHONPATH=$SCRIPTS_DIR:$PYTHONPATH:$BASE_DIR
export INFO_DIR=$BASE_DIR/info
#--------------------------------------------

# Activar entorno virtual
if [ -f "$BASE_DIR/ambiente/bin/activate" ]; then
    source $BASE_DIR/ambiente/bin/activate
else
    echo "Entorno virtual no encontrado en $BASE_DIR/ambiente/"
    exit 1
fi

#--------------------------------------------
# Ejecutar tests con pytest
echo "Ejecutando tests..."
pytest -v $SCRIPTS_DIR/test/

# Desactivar entorno virtual
deactivate
