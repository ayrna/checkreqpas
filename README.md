# Sistema de auditoría formativa para la enseñanza de administración de sistemas GNU/Linux

Este repositorio contiene el desarrollo realizado en el Trabajo Fin de Grado:

**Diseño e implementación de un sistema de auditoría formativa para la enseñanza de administración de sistemas GNU/Linux en entornos universitarios.**

El sistema permite al profesorado evaluar de forma objetiva el estado de configuración de máquinas virtuales del alumnado mediante auditorías automatizadas no intrusivas.

---

# Objetivo del proyecto

El objetivo del sistema es permitir:

- Verificar de forma automática requisitos técnicos de configuración.
- Evaluar el progreso del alumnado en prácticas de administración de sistemas.
- Obtener resultados estructurados y comparables.
- Facilitar la revisión mediante un dashboard visual.

El sistema está orientado a **evaluación formativa**, no a pentesting ni hardening.

---

# Arquitectura del sistema

El sistema se compone de:

- Máquina auditora (profesor)
- Máquinas auditadas (alumnado)
- Playbooks de auditoría
- Generación de resultados en CSV
- Dashboard de visualización

Flujo básico:

1. El profesor ejecuta un playbook de auditoría.
2. Ansible se conecta por SSH a las máquinas auditadas.
3. Se ejecutan pruebas objetivas.
4. Se generan ficheros CSV.
5. El dashboard permite visualizar resultados.

---

# Tecnologías utilizadas

- Ansible  
- GNU/Linux (Debian/Mint)  
- SSH  
- Python 3  
- Panel (dashboard)  
- CSV  
- VirtualBox (entorno de pruebas)  

---

# Estructura del repositorio

ansible_tests/
tema1.yml
tema2.yml
tema3.yml
...
export_csv.yml

dashboard.py
install.sh
run_dashboard.sh
ips
resultados_csv/
README.md


---

# Requisitos

En la máquina auditora:

- GNU/Linux
- Ansible instalado
- Python 3
- Panel
- Acceso SSH a las máquinas auditadas
- Clave SSH configurada

---

# Instalación

Instalar dependencias:

```bash
chmod +x install.sh
./install.sh


## Configuración SSH

### Generar clave

```bash
ssh-keygen -t ed25519
```

### Copiar clave al host

```bash
ssh-copy-id usuario@IP
```

---

## Configuración del inventario

Ejemplo de fichero `ips`:

```bash
[auditadas]
192.168.56.104 ansible_user=vboxuser ansible_become=yes
192.168.56.105 ansible_user=vboxuser ansible_become=yes
```

---

## Ejecución de auditorías

Para auditar un tema:

```bash
ansible-playbook -i ips ansible_tests/tema1.yml
```

El sistema:

- Ejecuta pruebas  
- Evalúa requisitos  
- Genera CSV por host  

Formato de salida:

```
IP_temaX.csv
```

---

## Dashboard

El dashboard puede iniciarse manualmente:

```bash
panel serve dashboard.py --show
```

O utilizando el script proporcionado:

```bash
chmod +x run_dashboard.sh
./run_dashboard.sh
```

El dashboard permite:

- Seleccionar host  
- Seleccionar tema  
- Visualizar resultados  
- Ver porcentaje de cumplimiento  

---

## Cómo añadir una nueva prueba

1. Editar el playbook del tema correspondiente.  
2. Añadir una tarea de Ansible.  
3. Definir:
   - `prueba_id`
   - `descripción`
   - `resultado` (OK / INCORRECTO)

No es necesario modificar el dashboard ni el sistema de exportación.

---

## Cómo añadir un nuevo tema

1. Crear un nuevo playbook en:

```
ansible_tests/
```

2. Ejecutar con:

```bash
ansible-playbook -i ips ansible_tests/Xtema.yml
```

---

## Entorno de pruebas

El sistema ha sido desarrollado y probado en:

- VirtualBox  
- Máquinas virtuales GNU/Linux  
- Inventarios con múltiples hosts  

La integración con OpenNebula queda prevista como mejora futura.


---

## Trabajo futuro

- Integración con OpenNebula.  
- Informes automáticos.  
- Historial de progreso.  
- Comparación entre alumnos.  
- Exportación a formatos adicionales.  

---

## Autor

Juan Andrés Torres Magne  
Grado en Ingeniería Informática  
Universidad de Córdoba  

---

## Licencia

Este proyecto se distribuye con fines académicos y docentes.
