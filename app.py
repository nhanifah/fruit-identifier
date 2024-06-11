from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import json
import io
from PIL import Image
import requests
import tempfile
import time  # Import missing time module

app = Flask(__name__)

# Print code execute
print('Running program')

# Temporary files to store the downloaded model and class labels
model_file = tempfile.NamedTemporaryFile(delete=False, suffix=".h5")
labels_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")

# Download the model file
model_url = 'https://storage.googleapis.com/bucket-nutrieasy/fruit_and_vegetable_detection.h5'
response = requests.get(model_url)
model_file.write(response.content)
model_file.flush()

# Download the class labels file
labels_url = 'https://storage.googleapis.com/bucket-nutrieasy/metadata_arr.json'
response = requests.get(labels_url)
labels_file.write(response.content)
labels_file.flush()

# Load the trained model
model = load_model(model_file.name)
print('Model loaded')

# Load class labels
with open(labels_file.name, 'r') as f:
    class_labels = json.load(f)

start_time = time.time()  # Initialize start_time

@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'ok'})

@app.route('/health', methods=['GET'])
def health():
    uptime = time.time() - start_time
    # Return the uptime in seconds
    uptime = round(uptime, 2)
    # convert the uptime to hours, minutes and seconds
    uptime = str(int(uptime // 3600)) + ' hours, ' + str(int((uptime % 3600) // 60)) + ' minutes, ' + str(int(uptime % 60)) + ' seconds'
    return jsonify({'status': 'UP', 'uptime': uptime})

@app.route('/classify', methods=['POST'])
def classify_image():
    try:
        if 'file' not in request.files:
            print('Firing program')
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file:
            print('Processing image')
            img = Image.open(io.BytesIO(file.read()))
            img = img.resize((224, 224))
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array / 255.0

            prediction = model.predict(img_array)
            predicted_class = class_labels[np.argmax(prediction)]

            return jsonify({'result': predicted_class})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
