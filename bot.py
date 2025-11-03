import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Función para el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde cuando el usuario envía /start"""
    await update.message.reply_text(
        '🤖 ¡Hola! Soy tu Notificador de Carga.\n\n'
        '📱 Envíame cualquier mensaje y te responderé.\n'
        '⚡ Configura tu atajo de iOS para avisarte al 85% de batería.\n\n'
        'Comandos disponibles:\n'
        '/start - Iniciar el bot\n'
        '/ayuda - Ver ayuda\n'
        '/estado - Ver estado del bot'
    )

# Función para el comando /ayuda
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Proporciona ayuda"""
    await update.message.reply_text(
        '📋 AYUDA\n\n'
        '1️⃣ Configura el atajo en tu iPhone:\n'
        '   - Abre "Atajos"\n'
        '   - Crea automatización de batería al 85%\n'
        '   - Envía mensaje a este bot\n\n'
        '2️⃣ El bot recibirá tus notificaciones automáticas\n\n'
        '3️⃣ Puedes enviarme cualquier mensaje para probar'
    )

# Función para el comando /estado
async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el estado del bot"""
    await update.message.reply_text(
        '✅ Bot funcionando correctamente\n'
        f'👤 Tu ID: {update.effective_user.id}\n'
        f'💬 Chat ID: {update.effective_chat.id}\n'
        '🟢 Listo para recibir notificaciones'
    )

# Función para manejar mensajes de texto
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja todos los mensajes de texto que no son comandos"""
    user_message = update.message.text
    user_name = update.effective_user.first_name
    
    logger.info(f"Mensaje recibido de {user_name}: {user_message}")
    
    # Detectar si es una notificación de batería
    if "85%" in user_message or "batería" in user_message.lower() or "carga" in user_message.lower():
        await update.message.reply_text(
            f'⚡ ¡ALERTA RECIBIDA!\n\n'
            f'🔋 Mensaje: {user_message}\n\n'
            f'✅ Notificación procesada correctamente.\n'
            f'🔌 Recuerda desconectar tu cargador.'
        )
    else:
        # Para cualquier otro mensaje
        await update.message.reply_text(
            f'✅ Mensaje recibido: "{user_message}"\n\n'
            f'👋 Hola {user_name}, tu bot está funcionando correctamente.'
        )

# Función principal
def main():
    """Inicia el bot"""
    # Obtener el token desde variable de entorno
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not TOKEN:
        logger.error("ERROR: No se encontró el token. Configura la variable TELEGRAM_BOT_TOKEN")
        return
    
    # Crear la aplicación
    application = Application.builder().token(TOKEN).build()
    
    # Agregar handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ayuda", ayuda))
    application.add_handler(CommandHandler("estado", estado))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Iniciar el bot
    logger.info("🚀 Bot iniciado correctamente")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
