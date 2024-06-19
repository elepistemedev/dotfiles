#!/bin/bash

# os=`cat /etc/fedora-release | awk '{printf "%s %s", $1, $3}'`
os=$(hostnamectl | grep -i 'operating system' | awk -F ':' '{print $2}' | awk -F ' ' '{print $1}')
# rootUsed=`df -h --output=used / | tail -n1 | tr -d ' \n'`
# rootTotal=`df -h --output=size / | tail -n1 | tr -d ' \n'`
# memUsed=`free -m | grep "Mem" | awk '{printf "%.1fG", $3/1000}'`
# memTotal=`free -m | grep "Mem" | awk '{printf "%.fG", $2/1000}'`
# cpuTemp=`sensors | grep CPU | awk '{print $2}' | sed 's/+//' | tr -d '\n'`
# loadAvg=`cat /proc/loadavg | awk '{printf "%s %s %s", $1, $2, $3}'`

case $os in
*Fedora)
	os_listar="\uf30a Fedora"
	;;
*Ubuntu)
	os_listar="\uebc9 Ubuntu"
	;;
*)
	os_listar="👽 en el Multiverso"
	;;
esac
source /home/el/anaconda3/bin/deactivate
clear

# printf "
# █▀ █▀▀ █▄░█ ▀█▀ █░█     $os
# ▄█ ██▄ █░▀█ ░█░ █▄█    $rootUsed/$rootTotal   $memUsed/$memTotal   $cpuTemp  辰$loadAvg
#             .STUDIO
# "

printf "
  █▀ █▀▀ █▄░█ ▀█▀ █░█  ┎┤ Arquitectura de Software ├┒
  ▄█ ██▄ █░▀█ ░█░ █▄█  ┖┤    en Python | Django    ├┚
              .studio en $os_listar
"
exit
