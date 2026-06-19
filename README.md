# TPI - Automatización de Gestión de Vacaciones mediante Chatbot

**Cátedra:** Organización Empresarial — Tecnicatura Universitaria en Programación
**Alumnos:** Alanis Rolando, Morales Fabian

## Descripción

Simulación por consola de un chatbot que automatiza el proceso de solicitud de
vacaciones de una empresa ficticia (TechCorp S.A.). El bot autentica al
empleado, consulta su saldo de días disponibles y evalúa reglas de negocio
(saldo suficiente y anticipación mínima de 15 días) antes de aprobar o
rechazar la solicitud, registrando el resultado en un historial.

La implementación actual corre por consola (`input()`); está pensada para
migrarse a Telegram reemplazando esas llamadas por handlers de
`python-telegram-bot`.

## Requisitos

- Python 3.8 o superior
- No requiere librerías externas (usa únicamente la librería estándar:
  `os`, `datetime`)

## Instalación

```bash
git clone https://github.com/famorales931-arch/TPI-Organizacion-chatbot.git
cd TPI-Organizacion-chatbot
```

No es necesario instalar dependencias adicionales.

## Ejecución

```bash
python chatbot_vacaciones.py
```

Al ejecutarse por primera vez, el script crea automáticamente los archivos
`empleados.csv` y `solicitudes.csv` si no existen, con datos de ejemplo.

## Uso

1. Ingresar el número de legajo (ej: `1001`).
2. Ingresar el PIN de 4 dígitos (ej: `4321`).
3. Una vez autenticado, ingresar la fecha de inicio deseada en formato
   `AAAA-MM-DD` (ej: `2026-08-15`).
4. Ingresar la cantidad de días solicitados (ej: `7`).
5. El bot informa el resultado: aprobado o rechazado, con el motivo.

### Usuarios de prueba (empleados.csv)

| Legajo | PIN  | Nombre          | Días disponibles |
|--------|------|-----------------|-------------------|
| 1001   | 4321 | Juan Perez      | 14                |
| 1002   | 7890 | Fabian Morales  | 21                |
| 1003   | 1111 | Rolando Gomez   | 7                 |

## Reglas de negocio

- **Saldo suficiente:** los días solicitados no pueden superar el saldo
  disponible del empleado.
- **Anticipación mínima:** la fecha de inicio debe estar a 15 días corridos
  o más desde la fecha actual.

## Estructura del proyecto

```
TPI-Organizacion-chatbot/
├── chatbot_vacaciones.py   # Lógica del bot y máquina de estados
├── empleados.csv           # Base de datos simulada de empleados
├── solicitudes.csv         # Historial de solicitudes procesadas
└── README.md               # Este archivo
```

## Diagramas BPMN

Los diagramas de proceso AS-IS y TO-BE se encuentran documentados en el
informe del Trabajo Práctico Integrador (PDF entregado junto al código).

## Herramientas de IA utilizadas

Se utilizó Gemini (Google) como asistente para el diseño de la máquina de
estados, el diccionario de datos y la revisión de los caminos infelices del
flujo. Las capturas de las consultas realizadas se encuentran documentadas
en el informe del TPI.
