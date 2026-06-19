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
