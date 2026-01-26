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
| Instalar servicio `systemd` | Instalar un servidor PHP de ejemplo de [este tutorial](https://medium.com/@benmorel/creating-a-linux-service-with-systemd-611b5c8b91d6). | `resultado=$(echo hola BARRAVERTICAL nc -u 127.0.0.1 10000 2>&1)` debe devolver `ubyn en $resultado` | No hay que hacer nada | 



## Tema 5: Gestión de recursos del sistema

| Prueba | Requisito | Cómo probarlo | Cómo generarlo | 
| --- | --- | --- | --- | 
| Limitar el número de procesos para usuarios | Directiva `ulimit` | Por línea de comandos comprobar que `ulimit` no devuelve `unlimited` (1000 sería un buen valor aquí)| `unlimited` es el valor por defecto | 

Enlaces: 
- <https://www.cyberciti.biz/faq/understanding-bash-fork-bomb/>
- <https://www.geeksforgeeks.org/linux-unix/limits-conf-file-to-limit-users-process-in-linux-with-examples/>




# Dudas para el Servicio de Informática
* Forzar a tener una imagen sin interfaz gráfica
* Ampliar las imágenes 
* Se pueden conectar por SSH, ¿bajo qué dirección o nombre?