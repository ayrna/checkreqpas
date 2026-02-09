# Manual de Usuario

## Introducción

Este manual de usuario describe el procedimiento necesario para
instalar, ejecutar y utilizar el sistema de auditoría formativa
desarrollado en este Trabajo Fin de Grado. El sistema está orientado al
uso por parte del profesorado en asignaturas de administración de
sistemas GNU/Linux, permitiendo evaluar de forma objetiva el estado de
configuración de las máquinas virtuales del alumnado.

El alumnado no interactúa directamente con el sistema de auditoría, sino
que se limita a configurar su máquina virtual conforme a las prácticas
propuestas en la asignatura. El uso del sistema queda restringido al
profesorado.

## Prerrequisitos

Para el uso correcto del sistema de auditoría es necesario disponer de
los siguientes elementos en la máquina auditora.

### Sistema operativo

La máquina auditora debe ejecutar un sistema GNU/Linux. El sistema ha
sido desarrollado y probado sobre distribuciones basadas en Debian,
aunque no depende de una versión concreta.

### Ansible

Es necesario disponer de Ansible instalado en la máquina auditora, ya
que constituye la herramienta principal para la ejecución de auditorías
mediante *playbooks*:

``` {.bash fontsize="\\small"}
sudo apt install ansible
```

### Acceso remoto mediante SSH

La máquina auditora debe poder establecer conexión SSH con las máquinas
virtuales del alumnado. Para ello, se requiere autenticación basada en
claves públicas, permitiendo la ejecución automática de auditorías sin
interacción manual.

La clave pública del auditor debe encontrarse registrada en el fichero
`authorized_keys` del usuario con privilegios suficientes en cada *host*
auditado.

### Generación y distribución de la clave SSH

Para permitir la ejecución automática de auditorías sin intervención
manual, es necesario configurar autenticación mediante clave pública
entre la máquina auditora y las máquinas auditadas.

En primer lugar, debe generarse un par de claves SSH en la máquina
auditora mediante el siguiente comando:

``` {.bash fontsize="\\small"}
ssh-keygen -t ed25519
```

Durante el proceso, el sistema solicitará una ruta para almacenar la
clave y una frase de paso. En el contexto de este sistema se recomienda
aceptar la ruta por defecto pulsando *Enter* y omitir la frase de paso
pulsando nuevamente *Enter*. Esto permite que las auditorías se ejecuten
de forma no interactiva.

![Proceso de generación de una clave SSH en la máquina
auditora.](pic/ssh-keygen.png){#fig:ssh-keygen
width="0.9\\linewidth"}

Una vez generada la clave, esta debe copiarse a cada máquina auditada
utilizando el siguiente comando:

``` {.bash fontsize="\\small"}
ssh-copy-id usuario@IP
```

Este procedimiento añade automáticamente la clave pública al fichero
`authorized_keys` del usuario remoto, permitiendo el acceso mediante SSH
sin necesidad de contraseña.

En la Figura [1.2](#fig:ssh-copy-id){reference-type="ref"
reference="fig:ssh-copy-id"} se muestra un ejemplo del proceso de
generación de la clave SSH.

![Proceso de copiado de clave al servidor
.](pic/ssh-copy-id.png){#fig:ssh-copy-id width="0.9\\linewidth"}

### Python y Panel

Para la visualización de resultados es necesario disponer de Python 3 y
de la librería Panel instalada en la máquina auditora. Panel se utiliza
para ejecutar el *dashboard* de resultados.

## Instalación del sistema

El sistema se distribuye como un conjunto de *playbooks* de Ansible y
*scripts* auxiliares organizados en un repositorio. No requiere
instalación ni configuración adicional en las máquinas del alumnado.

Una vez descargado el repositorio en la máquina auditora, debe
comprobarse la presencia de los siguientes elementos:

-   Directorio `ansible_tests/` con los *playbooks* organizados por
    temas.

-   Fichero de inventario `ips` con los *hosts* a auditar.

-   *Playbook* auxiliar `export_csv.yml` para la generación de
    resultados.

-   Código del *dashboard* desarrollado en Python.

No es necesario realizar procesos de compilación ni instalación
adicional.

## Guía de uso

### Preparación del entorno

Antes de ejecutar una auditoría, el profesorado debe asegurarse de que:

-   Las máquinas virtuales del alumnado están accesibles por red.

-   El fichero de inventario contiene las direcciones IP correctas.

-   El acceso SSH funciona correctamente sin solicitar contraseña.

Asimismo, el usuario debe definir en el *script* para exportar los
resultados a CSV un directorio en la máquina auditora donde se
almacenarán los ficheros generados por las auditorías. Este directorio
debe existir previamente y será utilizado tanto por el sistema de
generación de resultados como por el *dashboard* de visualización.

La ruta seleccionada forma parte de la configuración del entorno de
evaluación y puede adaptarse a las necesidades organizativas del
profesorado.

### Ejecución de auditorías

Para ejecutar una auditoría se utiliza un único comando desde la máquina
auditora. El profesorado debe seleccionar el tema a evaluar y ejecutar
el *playbook* correspondiente.

Ejemplo de ejecución:

``` {.bash fontsize="\\small"}
ansible-playbook -i ips ansible_tests/1tema.yml
```

Durante la ejecución, el sistema se conecta a cada *host* del inventario
y evalúa las pruebas definidas para el tema seleccionado.

### Generación e interpretación de resultados

Al finalizar la auditoría, el sistema genera un fichero CSV por cada
*host* auditado y por cada tema evaluado. El nombre del fichero sigue la
convención:

``` {.text fontsize="\\small"}
IP_temaX.csv
```

Cada fichero CSV incluye:

-   Un bloque detallado con una fila por cada prueba ejecutada.

-   Un bloque de resumen con el número de pruebas superadas, el total de
    pruebas y el porcentaje de cumplimiento.

Un resultado marcado como *INCORRECTO* indica que la configuración
evaluada no cumple el requisito solicitado en la práctica
correspondiente.

### Ejemplo de fichero CSV generado

Tras la ejecución de una auditoría, el sistema genera un fichero CSV por
cada máquina auditada y tema evaluado. Un ejemplo simplificado es el
siguiente:

``` text
host,tema,prueba_id,descripcion,resultado
192.168.56.104,tema3,1,Permisos correctos en /etc/shadow,OK
192.168.56.104,tema3,2,Paquete libpam-pwquality instalado,OK
192.168.56.104,tema3,3,Usuario becario con fecha de expiración,FAIL

host,tema,passed,total,score_percent
192.168.56.104,tema3,2,3,66
```

El primer bloque contiene el detalle de las pruebas y el segundo bloque
resume el resultado global del tema auditado.

### Ejemplo de fichero de inventario

El fichero de inventario define las máquinas auditadas y los parámetros
necesarios para la conexión mediante SSH. Un ejemplo mínimo de este
fichero es el siguiente:

``` bash
[auditadas]
192.168.56.104 ansible_user=vboxuser \
ansible_ssh_private_key_file=/home/tfg-audit/.ssh/id_ed25519 \
ansible_become=yes ansible_become_method=sudo
```

El usuario debe adaptar:

-   Las direcciones IP de las máquinas auditadas.

-   La ruta de la clave SSH.

-   El usuario remoto.

### Uso del *dashboard* de visualización

Para facilitar la consulta de los resultados generados por el sistema de
auditoría, se dispone de un *dashboard* desarrollado en Python mediante
la librería Panel. El *dashboard* se ejecuta en la máquina auditora y
consume directamente los ficheros CSV generados durante las auditorías.

El *dashboard* utiliza como fuente de datos el directorio configurado
por el usuario para el almacenamiento de los ficheros CSV. Esta ruta
debe coincidir con la definida durante la generación de resultados,
garantizando que el *dashboard* pueda localizar y cargar correctamente
los ficheros correspondientes a cada *host* y tema.

### Instalación de dependencias y ejecución del *dashboard*

Antes de utilizar el *dashboard*, es necesario instalar las dependencias
del sistema. Para ello se proporciona un *script* denominado
`install.sh`, que instala automáticamente los paquetes necesarios para
el funcionamiento del sistema.

``` {.bash fontsize="\\small"}
chmod +x install.sh
./install.sh
```

Para ejecutar el *dashboard*, primero es necesario dar permisos de
ejecución al *script* correspondiente:

``` bash
chmod +x run_dashboard.sh
```

A continuación, se ejecuta el script:

``` bash
./run_dashboard.sh
```

Una vez completada la instalación, el *dashboard* puede iniciarse
manualmente utilizando el siguiente comando:

``` {.bash fontsize="\\small"}
panel serve dashboard.py --show
```

Este comando inicia el servidor de Panel y abre automáticamente el
*dashboard* en el navegador web del sistema.

Una vez iniciado el servidor, el *dashboard* estará accesible desde un
navegador web en la dirección:

``` text
http://<IP_AUDITORA>:5006/dashboard
```

El *dashboard* escanea automáticamente el directorio donde se almacenan
los ficheros CSV y permite seleccionar de forma conjunta el *host*
auditado y el tema evaluado. A partir de esta selección, se muestra una
tabla con el detalle de las pruebas realizadas y un resumen del
porcentaje de cumplimiento.

La información se presenta utilizando un código de colores que varía
desde el verde hasta el rojo, pasando por tonos intermedios, lo que
facilita la interpretación rápida de los resultados por parte del
profesorado.

![Ejemplo del *dashboard* mostrando los resultados de una
auditoría](pic/dashboard.png){#fig:dashboard width="90%"}

## Extensión del sistema de auditoría

Aunque el sistema de auditoría ha sido diseñado para su uso directo por
parte del profesorado, también permite extender su funcionalidad de
forma controlada, incorporando nuevas pruebas o ampliando los temas
existentes. Esta sección describe los pasos básicos necesarios para
realizar dichas extensiones.

### Añadir una nueva prueba a un tema existente

Para añadir una nueva prueba a un tema ya implementado, es necesario
modificar el *playbook* correspondiente al tema dentro del directorio
`ansible_tests/`. Cada tema se implementa como un fichero independiente
denominado `Xtema.yml`.

El procedimiento general para añadir una prueba es el siguiente:

1.  Abrir el fichero `ansible_tests/Xtema.yml` correspondiente al tema
    que se desea ampliar.

2.  Definir una nueva tarea de Ansible que realice la comprobación
    deseada, utilizando módulos como `command`, `shell` u otros módulos
    estándar según el tipo de verificación.

3.  Asociar a la prueba un identificador único dentro del tema
    (`prueba_id`) y una descripción textual clara.

4.  Evaluar el resultado de la prueba de forma objetiva, estableciendo
    si el requisito se considera *CORRECTO* o *INCORRECTO*.

A modo de ejemplo, la siguiente prueba comprueba que un servicio
determinado está instalado en el sistema:

``` {.yaml fontsize="\\small"}
- name: Comprobar que el paquete apache2 está instalado
  command: dpkg -l apache2
  register: apache_installed
  changed_when: false

- set_fact:
    prueba_id: 3
    descripcion: "Paquete apache2 instalado"
    resultado: "{{ 'OK' if apache_installed.rc == 0 else 'INCORRECTO' }}"
```

Una vez añadida la prueba, esta se ejecutará automáticamente la próxima
vez que se lance la auditoría del tema correspondiente, sin necesidad de
realizar cambios adicionales en el sistema.

### Generación de resultados tras añadir una prueba

El sistema de generación de resultados en CSV no requiere modificaciones
al añadir nuevas pruebas. El *playbook* auxiliar `export_csv.yml`
recopila dinámicamente los resultados definidos durante la ejecución y
los incluye en el fichero CSV correspondiente.

Esto garantiza que cualquier prueba adicional se refleje automáticamente
tanto en el bloque de detalle como en el resumen de resultados.

### Añadir un nuevo tema de auditoría

Para añadir un nuevo tema completo, es suficiente con crear un nuevo
*playbook* dentro del directorio `ansible_tests/`, siguiendo la
nomenclatura existente (`Xtema.yml`). En este fichero se definen todas
las pruebas asociadas al nuevo bloque temático.

Una vez creado el nuevo *playbook*, el tema puede auditarse directamente
mediante el comando habitual de ejecución, sin necesidad de modificar el
resto del sistema.

Siempre que los ficheros CSV sigan la estructura definida, el
*dashboard* será capaz de cargar y visualizar correctamente los nuevos
resultados, manteniendo la compatibilidad con las extensiones
realizadas.

## Consideraciones finales

El sistema de auditoría está diseñado como una herramienta de apoyo al
profesorado y no sustituye la evaluación tradicional de la asignatura.
No proporciona *feedback* automático al alumnado ni realiza correcciones
sobre las máquinas auditadas, manteniendo un enfoque formativo y no
intrusivo.

Su uso permite complementar las prácticas y el examen, proporcionando
una visión objetiva del progreso técnico del alumnado.
