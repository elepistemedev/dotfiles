# Obtener la ruta absoluta de la carpeta raíz del proyecto
$ScriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
$ProjectDir = Split-Path -Parent -Path $ScriptPath

# Configurar PYTHONPATH como la raíz del proyecto
$env:PYTHONPATH = $ProjectDir

# Ejecutar el script main.py desde phase2
python "$ProjectDir\phase2\main.py"
