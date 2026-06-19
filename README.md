
# TPI - Automatización de Gestión de Vacaciones mediante Chatbot

**Cátedra:** Organización Empresarial — Tecnicatura Universitaria en Programación
**Alumnos:** Alanis Rolando, Morales Fabian

## Descripción

Desarrollo de un chatbot integrado con la API de **Telegram** que automatiza el proceso de solicitud de vacaciones de una empresa ficticia (TechCorp S.A.). El sistema maneja el flujo de interacciones mediante una Máquina de Estados Finitos (FSM) asincrónica, autentica al empleado, consulta su saldo de días disponibles y evalúa reglas de negocio antes de aprobar o rechazar la solicitud, registrando el resultado en un historial local.

Adicionalmente, el proyecto incluye una versión alternativa ejecutable por **consola** (`chatbot_vacaciones.py`) para simulaciones y pruebas locales rápidas.

## Requisitos

- Python 3.8 o superior
- Librería externa `python-telegram-bot`

## Instalación

1. Clonar el repositorio:
```bash
git clone [https://github.com/famorales931-arch/TPI-Organizacion-chatbot.git](https://github.com/famorales931-arch/TPI-Organizacion-chatbot.git)
cd TPI-Organizacion-chatbot

Instalar las dependencias requeridas:
Bash
pip install python-telegram-bot

Ejecución
Para iniciar la versión conectada a Telegram:

Bash
python bot_telegram.py

Nota: Al ejecutarse por primera vez, el script crea automáticamente los archivos empleados.csv y solicitudes.csv si no existen en el directorio, inicializándolos con datos de prueba.

Uso

1- Iniciar el chat en Telegram utilizando el comando /start.

2- Ingresar el número de legajo (ej: 1002).

3- Ingresar el PIN de 4 dígitos (ej: 7890).

4- Una vez autenticado, proveer la fecha de inicio deseada en formato AAAA-MM-DD (ej: 2026-12-01).

5- Ingresar la cantidad de días solicitados (ej: 14).

6- El bot informará el resultado de las compuertas lógicas (aprobado/rechazado) y emitirá un comprobante de sesión.

Usuarios de prueba (empleados.csv)

Legajo              PIN        Nombre           Días disponibles
1001                4321       Juan Perez            14
1002                7890       Fabian Morales        21
1003                1111       Rolando Gomez          7

Reglas de negocio

Saldo suficiente: Los días solicitados no pueden superar el saldo disponible del empleado en el registro.

Anticipación mínima: La fecha de inicio debe estar a un mínimo de 15 días corridos de distancia respecto a la fecha actual del sistema.

Estructura del proyecto

TPI-Organizacion-chatbot/
├── bot_telegram.py         # Código principal integrado con la API de Telegram (FSM)
├── chatbot_vacaciones.py   # Versión alternativa ejecutable por consola
├── empleados.csv           # Base de datos simulada de empleados (Persistencia)
├── solicitudes.csv         # Historial y registro de solicitudes procesadas
└── README.md               # Este archivo instructivo


Diagramas BPMN
Los diagramas de proceso de negocio AS-IS (manual) y TO-BE (automatizado) se encuentran completamente documentados y modelados en el informe del Trabajo Práctico Integrador (PDF entregado junto al código).

Herramientas de IA utilizadas
Se utilizó Gemini (Google) como asistente de ingeniería de software para el codiseño de la máquina de estados finitos, la estructura del diccionario de datos y la validación de robustez en los caminos infelices del flujo. Las evidencias y capturas de pantalla de las consultas analíticas están incorporadas formalmente en la Sección 7 del informe escrito.