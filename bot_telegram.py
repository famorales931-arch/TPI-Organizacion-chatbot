
import os
import logging
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

# Habilitar el registro de log para depuración
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

FILE_EMPLEADOS = "empleados.csv"
FILE_SOLICITUDES = "solicitudes.csv"

# Definición de Estados de la FSM para Telegram
AUTENTICANDO, MENU_OPCIONES, INGRESANDO_FECHA, INGRESANDO_DIAS = range(4)

# ==========================================
#      FUNCIONES DE BASE DE DATOS (CSV)
# ==========================================
def inicializar_archivos():
    if not os.path.exists(FILE_EMPLEADOS):
        with open(FILE_EMPLEADOS, "w", encoding="utf-8") as f:
            f.write("legajo,pin,nombre_apellido,dias_disponibles\n")
            f.write("1001,4321,Juan Perez,14\n")
            f.write("1002,7890,Fabian Morales,21\n")
            f.write("1003,1111,Rolando Gomez,7\n")
            
    if not os.path.exists(FILE_SOLICITUDES):
        with open(FILE_SOLICITUDES, "w", encoding="utf-8") as f:
            f.write("id_solicitud,legajo,fecha_inicio,dias_solicitados,estado,observaciones\n")

def leer_empleados():
    empleados = {}
    with open(FILE_EMPLEADOS, "r", encoding="utf-8") as f:
        lineas = f.readlines()[1:]
        for linea in lineas:
            if linea.strip():
                legajo, pin, nombre, dias = linea.strip().split(",")
                empleados[legajo] = {"pin": pin, "nombre": nombre, "dias": int(dias)}
    return empleados

def actualizar_saldo_empleado(legajo, nuevo_saldo):
    empleados = leer_empleados()
    empleados[legajo]["dias"] = nuevo_saldo
    with open(FILE_EMPLEADOS, "w", encoding="utf-8") as f:
        f.write("legajo,pin,nombre_apellido,dias_disponibles\n")
        for leg, info in empleados.items():
            f.write(f"{leg},{info['pin']},{info['nombre']},{info['dias']}\n")

def registrar_solicitud(legajo, fecha_ini, dias_req, estado, obs):
    with open(FILE_SOLICITUDES, "r", encoding="utf-8") as f:
        cant_lineas = len(f.readlines())
    id_sol = f"SOL-{cant_lineas:03d}"
    with open(FILE_SOLICITUDES, "a", encoding="utf-8") as f:
        f.write(f"{id_sol},{legajo},{fecha_ini},{dias_req},{estado},{obs}\n")

# ==========================================
#        LÓGICA DEL BOT DE TELEGRAM
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inicio del bot. Pide credenciales en formato Legajo-PIN."""
    inicializar_archivos()
    context.user_data.clear() # Limpiar datos previos del usuario
    
    await update.message.reply_text(
        "👋 Hola. Bienvenido al Asistente Virtual de Recursos Humanos para la Gestión de Vacaciones.\n\n"
        "🔒 Para ingresar, por favor envíe su Legajo y PIN separados por un guion.\n"
        "Ejemplo: `1002-7890`",
        parse_mode="Markdown"
    )
    return AUTENTICANDO

async def autenticar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Valida las credenciales ingresadas contra el archivo CSV."""
    texto = update.message.text.strip()
    
    if "-" not in texto:
        await update.message.reply_text("⚠️ Formato inválido. Recuerde usar el formato: Legajo-PIN (Ej: 1002-7890)")
        return AUTENTICANDO
        
    legajo, pin = texto.split("-", 1)
    db = leer_empleados()
    
    if legajo in db and db[legajo]["pin"] == pin:
        context.user_data["legajo"] = legajo
        context.user_data["nombre"] = db[legajo]["nombre"]
        context.user_data["dias_disponibles"] = db[legajo]["dias"]
        
        # Crear un menú con botones interactivos en Telegram
        teclado = [["📊 Consultar Saldo", "📅 Solicitar Vacaciones"], ["❌ Salir"]]
        markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True)
        
        await update.message.reply_text(
            f"✅ ¡Autenticación Exitosa!\nBienvenido/a, *{db[legajo]['nombre']}*.\n"
            "¿Qué trámite desea realizar hoy?",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        return MENU_OPCIONES
    else:
        await update.message.reply_text("❌ Credenciales incorrectas. Verifique su número de Legajo o PIN e intente de nuevo.")
        return AUTENTICANDO

async def menu_opciones(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Procesa la selección del menú principal."""
    opcion = update.message.text
    legajo = context.user_data.get("legajo")
    
    # Recargar datos del CSV por si hubo modificaciones intermedias
    db = leer_empleados()
    context.user_data["dias_disponibles"] = db[legajo]["dias"]

    if opcion == "📊 Consultar Saldo":
        await update.message.reply_text(
            f"ℹ️ Su saldo actual es de *{context.user_data['dias_disponibles']} días* de vacaciones disponibles.",
            parse_mode="Markdown"
        )
        return MENU_OPCIONES
        
    elif opcion == "📅 Solicitar Vacaciones":
        await update.message.reply_text(
            "📝 Iniciando solicitud de licencia.\n\n"
            "Por favor, ingrese la fecha en la que desea iniciar sus vacaciones con formato *AAAA-MM-DD*.\n"
            "Ejemplo: `2026-08-15`",
            reply_markup=ReplyKeyboardRemove(), # Quita los botones para permitir entrada limpia
            parse_mode="Markdown"
        )
        return INGRESANDO_FECHA
        
    elif opcion == "❌ Salir":
        return await salir(update, context)
    else:
        await update.message.reply_text("Opción no reconocida. Utilice los botones de la pantalla.")
        return MENU_OPCIONES

async def ingresar_fecha(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Valida el formato de la fecha ingresada."""
    fecha_str = update.message.text.strip()
    try:
        # Intenta parsear la fecha para validar el formato de entrada
        fecha_validada = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        context.user_data["fecha_inicio"] = fecha_str
        
        await update.message.reply_text(
            f"📆 Fecha registrada: {fecha_str}.\n\n"
            "Ahora ingrese la *cantidad de días* que desea solicitar (número entero):",
            parse_mode="Markdown"
        )
        return INGRESANDO_DIAS
    except ValueError:
        await update.message.reply_text("⚠️ Formato de fecha incorrecto. Asegúrese de usar *AAAA-MM-DD* (Ej: 2026-07-20):", parse_mode="Markdown")
        return INGRESANDO_FECHA

async def ingresar_dias(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Evalúa las Reglas de Negocio Robustas y finaliza el trámite."""
    dias_str = update.message.text.strip()
    
    if not dias_str.isdigit():
        await update.message.reply_text("⚠️ Por favor, ingrese un número entero válido para los días:")
        return INGRESANDO_DIAS
        
    dias_solicitados = int(dias_str)
    legajo = context.user_data["legajo"]
    dias_disponibles = context.user_data["dias_disponibles"]
    fecha_inicio = datetime.strptime(context.user_data["fecha_inicio"], "%Y-%m-%d").date()
    fecha_actual = datetime.now().date()
    
    anticipacion_dias = (fecha_inicio - fecha_actual).days
    
    # CONTROL DE REGLAS DE NEGOCIO DEL TP
    
    # Regla 1: Control de Saldo
    if dias_solicitados > dias_disponibles:
        motivo = f"Saldo insuficiente. Solicitó {dias_solicitados} días pero posee {dias_disponibles}."
        registrar_solicitud(legajo, fecha_inicio, dias_solicitados, "RECHAZADO", motivo)
        await update.message.reply_text(f"❌ *Solicitud Rechazada*\nMotivo: {motivo}", parse_mode="Markdown")
        
    # Regla 2: Control de Anticipación (Mínimo 15 días)
    elif anticipacion_dias < 15:
        motivo = f"Anticipación insuficiente. Solicitó con {anticipacion_dias} días de antelación (Mínimo requerido: 15)."
        registrar_solicitud(legajo, fecha_inicio, dias_solicitados, "RECHAZADO", motivo)
        await update.message.reply_text(f"❌ *Solicitud Rechazada*\nMotivo: {motivo}", parse_mode="Markdown")
        
    # CAMINO FELIZ: Pasa los controles
    else:
        nuevo_saldo = dias_disponibles - dias_solicitados
        actualizar_saldo_empleado(legajo, nuevo_saldo)
        registrar_solicitud(legajo, fecha_inicio, dias_solicitados, "APROBADO", "Procesado vía Telegram")
        
        await update.message.reply_text(
            f"🎉 *¡SOLICITUD APROBADA!*\n\n"
            f"📋 *Detalle del Comprobante:*\n"
            f"• Empleado: {context.user_data['nombre']}\n"
            f"• Fecha de Inicio: {fecha_inicio}\n"
            f"• Días Otorgados: {dias_solicitados}\n"
            f"• Saldo Actualizado: {nuevo_saldo} días.",
            parse_mode="Markdown"
        )
        
    # Volver al menú principal recreando el teclado de opciones
    teclado = [["📊 Consultar Saldo", "📅 Solicitar Vacaciones"], ["❌ Salir"]]
    markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True)
    await update.message.reply_text("¿Desea realizar alguna otra consulta?", reply_markup=markup)
    return MENU_OPCIONES

async def salir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Finaliza formalmente la conversación en el chat."""
    await update.message.reply_text(
        "👋 Sesión cerrada. Gracias por utilizar el Asistente de RRHH. ¡Hasta luego!",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# ==========================================
#            ORQUESTADOR PRINCIPAL
# ==========================================
def main():
    # ⚠️ REEMPLAZAR ESTA CADENA POR EL TOKEN REAL QUE LES DIO @BotFather
    TOKEN = "TU_TOKEN_DE_TELEGRAM_AQUI"
    
    inicializar_archivos()
    application = Application.builder().token(TOKEN).build()

    # Configuración de la máquina de estados mediante un manejador de conversación
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            AUTENTICANDO: [MessageHandler(filters.TEXT & ~filters.COMMAND, autenticar)],
            MENU_OPCIONES: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu_opciones)],
            INGRESANDO_FECHA: [MessageHandler(filters.TEXT & ~filters.COMMAND, ingresar_fecha)],
            INGRESANDO_DIAS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ingresar_dias)],
        },
        fallbacks=[CommandHandler("salir", salir), MessageHandler(filters.Regex("^❌ Salir$"), salir)],
    )

    application.add_handler(conv_handler)
    
    print("🤖 El Bot de Telegram de RRHH está encendido y escuchando mensajes...")
    application.run_polling()

if __name__ == "__main__":
    main()
