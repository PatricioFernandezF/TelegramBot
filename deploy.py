import requests
import os
from dotenv import load_dotenv
import time
from datetime import datetime
import json
import shutil

load_dotenv()

# Usa la variable de entorno para obtener la API key
TOKEN = os.getenv('comfyapi')
WORKFLOW=os.getenv('workflow')


class ComfyDeployAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://www.comfydeploy.com/api'
        self.headers = {'Authorization': f'Bearer {self.api_key}'}

    def run_workflow(self, deployment_id,inputs):
        url = f'{self.base_url}/run'
        data = {'deployment_id': deployment_id,"inputs": inputs}  # Asumiendo que se requiere un deployment_id en el cuerpo de la solicitud.
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def get_workflow_run_output(self, run_id, timeout=300, interval=10):
        """Obtiene el output de un run, esperando hasta que este finalice.

        Args:
            run_id (str): El ID del run.
            timeout (int): Tiempo máximo de espera en segundos antes de abortar.
            interval (int): Intervalo de tiempo entre sondeos consecutivos en segundos.

        Returns:
            dict: Respuesta JSON del run finalizado.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            response = requests.get(f'{self.base_url}/run?run_id={run_id}', headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') in ['success', 'failed']:  # Ajusta los estados según la API real
                    return data
            time.sleep(interval)
        raise TimeoutError("El tiempo de espera para el run ha excedido.")
    
    
    
    def get_upload_url(self, file_type, file_size):
        url = f'{self.base_url}/upload-url'
        params = {
            'type': file_type,
            'file_size': file_size
        }
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()
    

    def save_image_with_timestamp(self, image_url):
        """Descarga una imagen y la guarda con un timestamp en el nombre.

        Args:
            image_url (str): URL de la imagen a descargar.

        """
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            # Formatea el timestamp para el nombre del archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"image_{timestamp}.png"
            with open(filename, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            print(f"Imagen guardada como: {filename}")
        else:
            print("Error al descargar la imagen.")

    


# Uso de la clase
#api_key = TOKEN
#comfy_api = ComfyDeployAPI(api_key)

# Ejemplo de cómo desplegar un workflow
#workflow_id = WORKFLOW
#run_response = comfy_api.run_workflow(workflow_id,{"input_text":"a big man playing a piano"})
#print(run_response)

# Ejemplo de cómo obtener la salida de la ejecución de un workflow
#run_id = run_response["run_id"] # Reemplaza con el run_id real obtenido después de ejecutar el workflow
#if run_id:
    #output_response = comfy_api.get_workflow_run_output(run_id)
    #print(output_response)

    #image_info = output_response.get('outputs', [{}])[0].get('data', {}).get('images', [{}])[0]
    #image_url = image_info.get('url')

    #if image_url:
        #comfy_api.save_image_with_timestamp(image_url)
    #else:
        #print("No se encontró la URL de la imagen en el output.")
#else:
    #print("No se obtuvo run_id del workflow.")


#CARGA DE FICHEROS
#file_type = 'image/png'  # El tipo MIME del archivo que deseas subir
#file_size = '1024'  # El tamaño del archivo en bytes como string

# Obtén los detalles de la subida
#upload_info = comfy_api.get_upload_url(file_type, file_size)

# Realiza la carga del archivo
#files = {'file': open('archivo.png', 'rb')}
#upload_response = requests.post(upload_info['upload_url'], files=files)
#print(upload_response.text)

# Recuerda cerrar el archivo después de la carga
#files['file'].close()