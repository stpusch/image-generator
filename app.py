from flask import Flask, render_template, request, url_for
import requests
import base64
from PIL import Image
from io import BytesIO
import os
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Standardwerte definieren
    default_modelId = os.getenv('DEFAULT_MODEL_ID', '874c1033-932c-45c5-9357-e1fff5349557')
    default_temperature = os.getenv('DEFAULT_TEMPERATURE', '0.01')
    default_prompt = os.getenv('DEFAULT_PROMPT', 'Old man looking at the sea')
    default_token = os.getenv('BEARER_TOKEN', '')

    if request.method == 'POST':
        bearer_token = request.form.get('token') or default_token
        modelId = request.form.get('modelId') or default_modelId
        prompt = request.form.get('prompt') or default_prompt
        temperature = request.form.get('temperature') or default_temperature

        headers = {"Authorization": f"Bearer {bearer_token}"}
        url = f"https://inference.de-txl.ionos.com/models/{modelId}/predictions"

        data = {
            "type": "prediction",
            "properties": {
                "input": prompt,
                "options": {
                    "temperature": temperature
                }
            }
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            response_json = response.json()
            base64_data = response_json['properties']['output']

            # Decode the base64 data
            image_data = base64.b64decode(base64_data)
            image = Image.open(BytesIO(image_data))

            # Generate a unique filename
            filename = f"{uuid.uuid4()}.jpg"
            filepath = os.path.join('static', filename)
            image.save(filepath)

            return render_template('result.html', filename=filename)
        else:
            error_message = f"Request failed with status code {response.status_code}: {response.text}"
            # Übergebene Werte beibehalten
            return render_template('index.html',
                                   error=error_message,
                                   default_modelId=modelId,
                                   default_temperature=temperature,
                                   default_prompt=prompt)
    else:
        return render_template('index.html',
                               default_modelId=default_modelId,
                               default_temperature=default_temperature,
                               default_prompt=default_prompt)

if __name__ == '__main__':
    app.run(debug=True)
