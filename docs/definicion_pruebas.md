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

| Cuentas restrictivas | La cuenta `web` debe tener restricciones (nologin, sin shell, etc.) | (poner los requisitos que genera el paquete de `apache2`)| 

Comprobar que se ha realizado esto: https://www.uco.es/users/i02samoj/plazatu/pas/tema03-usuarios/tema03-usuarios.html#ejercicio-usuario-y-grupo-para-apache

# Dudas para el Servicio de Informática
* Forzar a tener una imagen sin interfaz gráfica
* Ampliar las imágenes 
* Se pueden conectar por SSH, ¿bajo qué dirección o nombre?