# Definición de pruebas por temas de la asignatura

## Tema 1: introducción a la administración de sistemas y GNU/Linux


El objetivo de estas tareas es que el alumnado haya realizado una postinstalación básica y deje la máquina lista para trabajar y accesible para el sistema. 

| Prueba | Requisito | Cómo probarlo | Cómo generarlo | 
| --- | --- | --- | --- | 
| Sudo | tener instalado `sudo` | `dpkg -i \| grep sudo` | `apt remove sudo` |
| Root defecto | Cambiar la contraseña por defecto de root | Comprobar por terminal o mirar el hash en `/etc/shadow` | Vendrá en la instalación base |
| Usuario de administración | Debe haber un usuiario `adminpas` incluído en el grupo `sudo` | `getent passwd adminpas` y `getent group sudo` Vendrá en la instalación base 
| Servicio SSH | Servicio SSH instalado | Conexión exitosa | Vendrá en la instalación base* |
| Sólo terminal | El servidor no debe tener ninguna interfaz gráfica | ¿mirar servicios X comunes? | Vendrá en la insalación base | 
| Máquina actualizada | No debe haber actualizaciones pendientes | Lo hace Ansible y otros | Vendrá con la instalación base |

Referencias: 

https://www.uco.es/users/i02samoj/plazatu/pas/tema01-introduccion/tema01c-proyecto.html#proyecto-asignatura

https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-22-04

https://www.digitalocean.com/community/tutorials/a-linux-command-line-primer

https://www.digitalocean.com/community/tutorials?q=%5BLinux%20Basics%5D


## Tema 2: organización sistema 

Pensar una carpeta y subcarpetas que queramos con una serie de permisos. Por ejemplo el caso de `www`

| Prueba | Requisito | Cómo probarlo | Cómo generarlo | 
| --- | --- | --- | --- | 
| Permisos claves | Asegurar los permisos de las claves en `.ssh` | Comprobar cadena permisos | `chmod o+rw /root/.ssh && chmod 777 /home/adminpass/ && chmod 777 -R /home/adminpass/.ssh` |
| Pruebas permisos | Establecer unos permisos para `/var/www` que permita modificar a los usuarios del grupo `web` | Comprobar cadena permisos | Por defecto vienen más restringidos. | 



## Tema 3: Gestión de Usuarios

| Prueba | Requisito | Cómo probarlo | Cómo generarlo | 
| --- | --- | --- | --- | 
| Cracklib | Tener instalado Crackib | Con Ansible | Viene en la instalación base. |
| Permisos u/g | Comprobar los permisos de `/etc/passwd`, `/etc/group`, `/etc/shadow` | Máscaras permisos | Estropear los permisos por ejemplo:  `chmod +w /etc/passwd`, `chmod 000 /etc/group`, `chmod a+rx /etc/shadow`
| Comprobar contraseñas fáciles | Todos los usuarios deben tener contraseñas robustas | Con cracklib | El usuario `manzana` tendrá la contraseña `pera` | 
| Caducidad | El usuario `becario` debe expirar en septiembre | Con chage | Se crea el usuario sin fecha de caducidad. |
| Cuentas restrictivas | La cuenta `web` debe tener restricciones (nologin, sin shell, etc.) | (poner los requisitos que genera el paquete de `apache2`: `/usr/sbin/nologin`; permisos y propietario `-rw-r--r-- 1 root root  /etc/apache2/apache2.conf` y `-rw-r--r-- 1 root root 419 mar 18  2024 /lib/systemd/system/apache2.service`)| cambiar `/usr/sbin/nologin` a `/bin/bash` y activar w+o en ficheros de configuración | 

Comprobar que se ha realizado esto: https://www.uco.es/users/i02samoj/plazatu/pas/tema03-usuarios/tema03-usuarios.html#ejercicio-usuario-y-grupo-para-apache


## Tema 4: Arranque y parada


| Prueba | Requisito | Cómo probarlo | Cómo generarlo | 
| --- | --- | --- | --- | 
| Grub timeout | Tiempo de espera grub a cero. Se debe cambiar en `/etc/default/grub` y ejecutar `sudo update-grub` | El valor de la variable `timeout=0` (por defecto `5`) en `/boot/grub/grub.cfg` | Viene en la instalación base. |
| Instalar servicio `systemd` | Instalar un servidor PHP de ejemplo de [este tutorial](https://medium.com/@benmorel/creating-a-linux-service-with-systemd-611b5c8b91d6). | `resultado=$(echo hola \| nc -u 127.0.0.1 10000 2>&1)` debe devolver `ubyn en $resultado` | No hay que hacer nada | 




## Tema 5: Gestión de recursos del sistema

| Prueba | Requisito | Cómo probarlo | Cómo generarlo | 
| --- | --- | --- | --- | 
| Limitar el número de procesos para usuarios | Directiva `ulimit` | Por línea de comandos comprobar que `ulimit` no devuelve `unlimited` (1000 sería un buen valor aquí)| `unlimited` es el valor por defecto | 
| Monitorización memoria | Script que vuelque a un fichero de log la cantidad de memoria física y virtual cada 10 minutos usando crontab o systemd | Comprobar que existe y no está vacío `/opt/monitor_memoria/script_memoria.sh`, `/var/log/memoria.log` y comprobar la línea de crontab del usuario (e.j. `/var/spool/cron/crontabs/root`) | No hay que hacer nada. | 


```bash
# 1. Guardar el script en un directorio adecuado
sudo mkdir -p /opt/monitor_memoria
sudo mv script_memoria.sh /opt/monitor_memoria/

# 2. Dar permisos
sudo chmod +x /opt/monitor_memoria/script_memoria.sh

# 3. Configurar crontab
sudo crontab -e
# Agregar: */10 * * * * /opt/monitor_memoria/script_memoria.sh
# Esto se guarda en  /var/spool/cron/crontabs/USUARIO (en este ejemplo /var/spool/cron/crontabs/root)

# 4. Verificar el log
tail -f /var/log/memoria.log
```


Enlaces: 
- <https://www.cyberciti.biz/faq/understanding-bash-fork-bomb/>
- <https://www.geeksforgeeks.org/linux-unix/limits-conf-file-to-limit-users-process-in-linux-with-examples/>
- <https://www.linuxbash.sh/post/how-to-create-a-bash-script-to-monitor-system-resources>


## Tema 7: Administración de sistemas de ficheros

| Prueba | Requisito | Cómo probarlo | Cómo generarlo | 
| --- | --- | --- | --- | 
| Cuotas instaladas | Instalado el paquete `quota` | Comprobar que está instalado | No hay que hacer nada | 
| Cuotas activadas en el sistema de ficheros | El usuario debe haber activado con `tune2fs -O quota /dev/sda3` | Si no están activadas esto devuelve una línea vacía `sudo tune2fs -l /dev/sda3 \| grep -i quota` | No hay que hacer nada | 
| Probar quotas (TODO) | Script que escriba en disco un fichero enorme | `fallocate --length 2000MB ~/fichero` | No hay que hacer nada | 

NOTA: Adaptar el último caso al dispositivo y partición de la imagen de Debian en OpenNebula. Quizás se pueda hacer una tarea que sea poner una etiqueta "RAIZ" o "HOME" y así queda disponible con la etiqueta y en `/dev/disk/by-label/`


## Tema 8: Restauración y copias de seguridad

| Prueba | Requisito | Cómo probarlo | Cómo generarlo | 
| --- | --- | --- | --- | 
| Backup dump | Debe haber copias de seguridad en | Esto debe devolver un listado de varias líneas `sudo restore -t -f /mnt/backup/dump0`. Si devuelve `No such file or directory` es que no hay ningún fichero | No hay que hacer nada | 
| Programación backup | Las copias deben estar programadas | `crontab -l` debe devolver al menos 2 líneas que no empiecen por #. Las líneas contendrán la orden `dump` | No hay que hacer nada |

Enlaces: 
- Receta de backup incremental con dump + restore + crontab en los apuntes del tema 8.


## Tema 9: Gestión de las comunicaciones

| Prueba | Requisito | Cómo probarlo | Cómo generarlo | 
| --- | --- | --- | --- | 
| Actualizaciones automáticas | Tener instalado y configurado el paquete `unattended-upgrades` | Comprobar que está instalado `unattended-upgrades` y que el fichero `/etc/apt/apt.conf.d/20auto-upgrades` y tiene el contenido `APT::Periodic::Update-Package-Lists "1";APT::Periodic::Unattended-Upgrade "1";APT::Periodic::AutocleanInterval "7";` (ver tutorial abajo) | No hay que hacer nada | 
| Nombre de máquina correcto | Valores correctos en `/etc/hostname` | El comando `hostname` devuelve `login_pas` como nombre de máquina | No hay que hacer nada | 
| Cortafuegos | Instalación y configuración básica de `ufw` | Se rechazan todas las conexiones salvo puerto 22, 80 y 443. | No hay que hacer nada | 
| DNS de respaldo | Añadir DNS de respaldo | `resolvectl status\|grep Fallback` devuelve `Fallback DNS Servers: 1.1.1.1` similar. Si no está configurado devuelve vacío. | No hay que hacer nada | 

TODO: Cuando tengamos OpenNebula funcionando veremos la dificultad de montar un NFS



Enlaces:
- [Actualizaciones automáticas en nuestro equipo con unattended-upgrades](https://geekland.eu/actualizaciones-automaticas-en-nuestro-equipo-con-unattended-upgrades/)
- [How To Set Up a Firewall with UFW on Debian 11](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-debian)
- [https://wiki.archlinux.org/title/Systemd-resolved](systemd-resolved). Aquí no indican que hay que reinicar el servicio para que lea los nuevos DNS con `systemctl restart systemd-resolved.service` 

# Dudas para el Servicio de Informática
* Forzar a tener una imagen sin interfaz gráfica
* Ampliar las imágenes 
* Se pueden conectar por SSH, ¿bajo qué dirección o nombre?