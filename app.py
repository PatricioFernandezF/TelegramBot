import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import telegram
from deploy import ComfyDeployAPI


load_dotenv()

# Usa la variable de entorno para obtener la API key
TOKENTELEGRAM = os.getenv('telegram')
TOKEN = os.getenv('comfyapi')
WORKFLOW=os.getenv('workflow')

# Define una función de manejo para el comando /start
async def start(update: Update, context: telegram.ext.CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Soy un bot de Telegram. ¡Envíame mensajes!")

# Define una función de manejo para mensajes de texto
async def echo(update: Update, context: telegram.ext.CallbackContext) -> None:
    texto=update.message.text

        # Uso de la clase
    api_key = TOKEN
    comfy_api = ComfyDeployAPI(api_key)

    # Ejemplo de cómo desplegar un workflow
    workflow_id = WORKFLOW
    run_response = comfy_api.run_workflow(workflow_id,{"input_text":texto})
    print(run_response)

    # Ejemplo de cómo obtener la salida de la ejecución de un workflow
    run_id = run_response["run_id"] # Reemplaza con el run_id real obtenido después de ejecutar el workflow
    if run_id:
        output_response = comfy_api.get_workflow_run_output(run_id)
        print(output_response)

        image_info = output_response.get('outputs', [{}])[0].get('data', {}).get('images', [{}])[0]
        image_url = image_info.get('url')

        if image_url:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url)
            return  # Finaliza la función después de enviar la imagen
            
    # Si no hay imagen, envía un mensaje de texto indicándolo
    await context.bot.send_message(chat_id=update.effective_chat.id, text="No se pudo generar una imagen.")
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=texto)

# Crea una aplicación usando el token
application = Application.builder().token(TOKENTELEGRAM).build()

# Registra los manejadores de comandos y mensajes
application.add_handler(CommandHandler('start', start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Inicia el bot
application.run_polling()
