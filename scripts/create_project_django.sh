#!/bin/bash

echo "Proyecto: $2"
echo "Lugar: $PWD/$2/"

RUN="docker compose run --rm"

ansi()          { echo -e "\e[${1}m${*:2}\e[0m"; }
bold()          { ansi 1 "$@"; }
# italic()        { ansi 3 "$@"; }
underline()     { ansi 4 "$@"; }
# strikethrough() { ansi 9 "$@"; }
red()           { ansi 31 "$@"; }
parpadear()           { ansi 5 "$@"; }

sentu_color()           { ansi 93 "$@"; }

name=$(basename $0)
command=$1
args=${@:2}

run_footer=$(
cat <<EOF
case \$command in

venv)
python -m venv .venv
.source venv/bin/activate
;;

requerimientos)
pip install -r requirements.txt
;;

dotenv)
echo -e "\$dotenv_file" > .env
;;

entorno)
docker compose down && \\
python -m venv .venv && \\
source .venv/bin/activate && \\
pip install -r requirements.txt && \\
echo -e "\$dotenv_file" > .env && \\
echo -e "\$local_sqlite_file" > "$PWD/$2/$2/settings/local.py"
;;

entorno_postgres)
python -m venv .venv && \\
source .venv/bin/activate && \\
pip install -r requirements.txt && \\
echo -e "\$dotenv_file" > .env && \\
echo -e "\$local_postgres_file" > "$PWD/$2/$2/settings/local.py" && \\
docker compose up -d
;;

activa_postgres)
echo -e "\$local_postgres_file" > "$PWD/$2/$2/settings/local.py" && \\
docker compose up -d
;;

activa_sqlite)
docker compose down && \\
echo -e "\$local_sqlite_file" > "$PWD/$2/$2/settings/local.py"
;;

makemigrations)
\$RUN makemigrations \$args
;;

migrate)
\$RUN migrate \$args
;;

createsuperuser)
\$RUN createsuperuser \$args
;;

server)
\$RUN runserver \$args
;;

super)
\$RUN makemigrations && \$RUN migrate && \$RUN createsuperuser --username=admin --email=admin@admin.com && \$RUN runserver
;;

help|"")

# Alignment of help message must be as it is, it will be nice looking when printed
clear


echo -e "\$usage"
;;

*)
message="\$(red Unknown command: \$command). See \$(bold ./\$name help) for available commands."
#echo -e "\$message" >&2
echo -e "\$message"
\$0 help
exit 1
;;

esac
EOF
)

case $command in

project_simple)
django-admin startproject --template /home/el/sentu/templates/django/projects/sentu_template_simple $2 && \
echo -e "$run_footer" >> $PWD/$2/run || echo -e "$(red Error:) al ejecutar django-admin, deberías instalar $(bold pip install Django)"
;;

project_users_simple)
django-admin startproject --template /home/el/sentu/templates/django/projects/sentu_template_users_simple $2 && \
echo -e "$run_footer" >> $PWD/$2/run || echo -e "$(red Error:) al ejecutar django-admin, deberías instalar $(bold pip install Django)"
;;

test)
echo -e "$run_footer"|| echo "algo se jorovó"
;;

pnpm)
$RUN mermaid sh -c "pnpm $args"
;;

dev)
$RUN --service-ports mermaid sh -c "pnpm run dev"
;;

docs:dev)
$RUN --service-ports mermaid sh -c "pnpm run --filter mermaid docs:dev:docker"
;;

cypress)
$RUN cypress $args
;;

help|"")

# Alignment of help message must be as it is, it will be nice looking when printed
clear
usage=$(
cat <<EOF

$(sentu_color  "  █▀ █▀▀ █▄░█ ▀█▀ █░█  ┎┤ Arquitectura de Software ├┒")
$(sentu_color  "  ▄█ ██▄ █░▀█ ░█░ █▄█  ┖┤    en Python | Django    ├┚")
$(sentu_color  "              .studio")


$(bold CENTRO DE DESPLIEGUE DE COMANDOS)

¡Bienvenidos! Gracias por usar las herramientas de $(bold $(sentu_color SENTU.studio)),
Este es un scrpit para correr comandos con el proyecto de forma simple.
__________________________________________________________________________________________

Development Quick Start Guide:

$(bold ./$name pnpm install)           # Install packages
$(underline ./$name dev)                    # Launch dev server with examples, open http://localhost:9000
$(red ./$name docs:dev)               # Launch official website, open http://localhost:3333
__________________________________________________________________________________________
Commands:
$(bold ./$name build)                  # Build image
$(bold ./$name cypress)                # Run integration tests
$(bold ./$name dev)                    # Run dev server with examples, open http://localhost:9000

EOF
)

echo -n -e "$usage"
;;

*)
message="$(red Unknown command: $command). See $(bold ./$name help) for available commands."
#echo -n -e "$message\n" >&2
echo -n -e "$message\n"
$0 help
exit 1
;;

esac

cd $2
sh run