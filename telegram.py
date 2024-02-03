import os
from dotenv import load_dotenv
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from deploy import ComfyDeployAPI

load_dotenv()

# Usa la variable de entorno para obtener la API key
TOKENTELEGRAM = os.getenv('telegram')
# Usa la variable de entorno para obtener la API key
TOKEN = os.getenv('comfyapi')
WORKFLOW=os.getenv('workflow')

# Define una función de manejo para el comando /start
async def start(update: Update, context: telegram.ext.CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Soy un bot de Telegram. ¡Envíame mensajes!")

# Define una función de manejo para mensajes de texto
async def echo(update: Update, context: telegram.ext.CallbackContext) -> None:
    texto=update.message.text
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=texto)

# Crea una aplicación usando el token
application = Application.builder().token(TOKENTELEGRAM).build()

# Registra los manejadores de comandos y mensajes
application.add_handler(CommandHandler('start', start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Inicia el bot
application.run_polling()
