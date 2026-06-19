import os
from datetime import datetime, timedelta

# Configuración de nombres de archivos (Bases de datos simuladas)
FILE_EMPLEADOS = "empleados.csv"
FILE_SOLICITUDES = "solicitudes.csv"

def inicializar_base_de_datos():
    """Crea los archivos CSV iniciales si no existen en el directorio."""
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
    """Lee el CSV de empleados y devuelve un diccionario indexado por legajo."""
    empleados = {}
    with open(FILE_EMPLEADOS, "r", encoding="utf-8") as f:
        lineas = f.readlines()[1:]  # Omitir encabezado
        for linea in lineas:
            if linea.strip():
                legajo, pin, nombre, dias = linea.strip().split(",")
                empleados[legajo] = {
                    "pin": pin,
                    "nombre": nombre,
                    "dias": int(dias)
                }
    return empleados

def actualizar_saldo_empleado(legajo_usuario, nuevos_dias):
    """Sobreescribe el saldo de días de un empleado tras una aprobación."""
    empleados = leer_empleados()
    empleados[legajo_usuario]["dias"] = nuevos_dias

    with open(FILE_EMPLEADOS, "w", encoding="utf-8") as f:
        f.write("legajo,pin,nombre_apellido,dias_disponibles\n")
        for leg, info in empleados.items():
            f.write(f"{leg},{info['pin']},{info['nombre']},{info['dias']}\n")

def registrar_solicitud(legajo, fecha_ini, dias_req, estado, obs):
    """Guarda el resultado del flujo de la solicitud en el historial dinámico."""
    with open(FILE_SOLICITUDES, "r", encoding="utf-8") as f:
        cant_lineas = len(f.readlines())
    id_sol = f"SOL-{cant_lineas:03d}"

    with open(FILE_SOLICITUDES, "a", encoding="utf-8") as f:
        f.write(f"{id_sol},{legajo},{fecha_ini},{dias_req},{estado},{obs}\n")

def ejecutar_chatbot():
    print("==================================================")
    print("      ASISTENTE VIRTUAL DE RECURSOS HUMANOS       ")
    print("==================================================")

    estado_actual = "ESPERANDO_AUTENTICACION"
    usuario_logueado = None
    legajo_activo = ""

    while True:
        # 1. FLUJO DE AUTENTICACIÓN
        if estado_actual == "ESPERANDO_AUTENTICACION":
            legajo_activo = input("\n[Bot]: Por favor, ingrese su número de Legajo: ").strip()
            pin_ingresado = input("[Bot]: Ingrese su PIN de seguridad de 4 dígitos: ").strip()
            estado_actual = "VALIDANDO_CREDENCIALES"

        if estado_actual == "VALIDANDO_CREDENCIALES":
            db_empleados = leer_empleados()
            if legajo_activo in db_empleados and db_empleados[legajo_activo]["pin"] == pin_ingresado:
                usuario_logueado = db_empleados[legajo_activo]
                print(f"\n[Bot Login]: ¡Autenticación Exitosa!")
                estado_actual = "MENU_PRINCIPAL"
            else:
                print("[Bot Error]: Legajo o PIN incorrectos. Intente nuevamente.")
                estado_actual = "ESPERANDO_AUTENTICACION"

        # 2. MENÚ PRINCIPAL Y REGISTRO DE FECHAS
        elif estado_actual == "MENU_PRINCIPAL":
            print(f"\n[Bot]: Bienvenido/a, {usuario_logueado['nombre']}.")
            print(f"[Bot]: Usted cuenta con {usuario_logueado['dias']} días de vacaciones disponibles.")

            print("\n--- INGRESO DE LICENCIA ---")
            fecha_str = input("[Bot]: Ingrese la fecha de inicio deseada (Formato: AAAA-MM-DD): ").strip()
            try:
                fecha_inicio = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            except ValueError:
                print("[Bot Error]: Formato de fecha inválido. Regresando al menú.")
                continue

            dias_str = input("[Bot]: Ingrese la cantidad de días que solicita: ").strip()
            if not dias_str.isdigit():
                print("[Bot Error]: La cantidad de días debe ser un número entero. Regresando.")
                continue
            dias_solicitados = int(dias_str)

            estado_actual = "PROCESANDO_SOLICITUD"

        # 3. EVALUACIÓN DE REGLAS DE NEGOCIO DINÁMICAS
        elif estado_actual == "PROCESANDO_SOLICITUD":
            fecha_actual = datetime.now().date()
            anticipacion_dias = (fecha_inicio - fecha_actual).days
            dias_disponibles = usuario_logueado["dias"]

            print("\n[Bot]: Evaluando políticas corporativas...")

            if dias_solicitados > dias_disponibles:
                motivo = f"Saldo insuficiente. Solicitó {dias_solicitados} días pero posee {dias_disponibles}."
                print(f"[RECHAZADO]: {motivo}")
                registrar_solicitud(legajo_activo, fecha_inicio, dias_solicitados, "RECHAZADO", motivo)
                estado_actual = "FINALIZADO_RECHAZADO"

            elif anticipacion_dias < 15:
                motivo = f"Anticipación insuficiente. Solicitó con {anticipacion_dias} días de antelación (mínimo 15)."
                print(f"[RECHAZADO]: {motivo}")
                registrar_solicitud(legajo_activo, fecha_inicio, dias_solicitados, "RECHAZADO", motivo)
                estado_actual = "FINALIZADO_RECHAZADO"

            else:
                nuevo_saldo = dias_disponibles - dias_solicitados
                actualizar_saldo_empleado(legajo_activo, nuevo_saldo)
                registrar_solicitud(legajo_activo, fecha_inicio, dias_solicitados, "APROBADO", "Procesado Correctamente")

                print(f"\n[¡APROBADO!]: Su solicitud de licencia para el día {fecha_inicio} ha sido autorizada.")
                print(f"[Bot]: Se han debitado {dias_solicitados} días. Su saldo remanente es: {nuevo_saldo} días.")
                estado_actual = "FINALIZADO_APROBADO"

        # 4. CIERRE DEL PROCESO FINITO
        elif estado_actual in ["FINALIZADO_APROBADO", "FINALIZADO_RECHAZADO"]:
            print("\n[Bot]: Muchas gracias por utilizar el Asistente de RRHH. El proceso ha concluido.")
            print("==========================================================================")
            break

if __name__ == "__main__":
    inicializar_base_de_datos()
    ejecutar_chatbot()
