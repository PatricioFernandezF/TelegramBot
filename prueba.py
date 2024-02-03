import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters


# Reemplaza 'TU_TOKEN' con el token que obtuviste de BotFather
TOKEN = '6302818856:AAF_fmOtmVQ46g9crtwB_LRjvG_LIh-AnRc'

# Define una función de manejo para el comando /start
async def start(update: Update, context: telegram.ext.CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Soy un bot de Telegram. ¡Envíame mensajes!")

# Define una función de manejo para mensajes de texto
async def echo(update: Update, context: telegram.ext.CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# Crea una aplicación usando el token
application = Application.builder().token(TOKEN).build()

# Registra los manejadores de comandos y mensajes
application.add_handler(CommandHandler('start', start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Inicia el bot
application.run_polling()
