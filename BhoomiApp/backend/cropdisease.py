from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.models import load_model
from PIL import Image
import numpy as np
import json
import openai
import API
import logging

logging.basicConfig(level=logging.DEBUG) 
app = Flask(__name__)
CORS(app)

# Load the trained model
try:
    model = load_model('backend/crop_disease_model.h5')  # Ensure the path is correct
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {str(e)}")

# Load class labels
try:
    with open('backend/class_labels.json') as f:  # Ensure the path is correct
        class_labels = json.load(f)
    print("Class labels loaded successfully.")
except Exception as e:
    print(f"Error loading class labels: {str(e)}")

# Configure OpenAI
openai.api_key = API.API_KEY  # Ensure the API key is set correctly

def prepare_image(image, target_size=(150, 150)):
    """
    Preprocesses the input image to match the model's expected input.
    """
    image = image.resize(target_size)  # Resize the image to the model's input size used during training
    image = np.array(image)  # Convert image to array
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    image = image / 255.0  # Normalize to [0, 1] range
    print(f"Processed image shape: {image.shape}")
    return image
@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Server is running'})

@app.route('/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict():
    app.logger.debug("Starting prediction...")
    try:
        if 'image' not in request.files:
            app.logger.error('No image uploaded')
            return jsonify({'error': 'No image uploaded'}), 400

        file = request.files['image']
        app.logger.debug(f"Received file: {file.filename}")

        image = Image.open(file)
        processed_image = prepare_image(image)
        app.logger.debug("Image preprocessed successfully")

        predictions = model.predict(processed_image)
        app.logger.debug(f"Predictions: {predictions}")

        predicted_class = np.argmax(predictions, axis=1)[0]
        disease = class_labels[predicted_class]
        app.logger.debug(f"Predicted disease: {disease}")

        insights = generate_insights(disease)
        app.logger.debug(f"Generated insights: {insights}")

        return jsonify({'disease': disease, 'insights': insights})
    except Exception as e:
        app.logger.error(f"Error during prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

import openai

def generate_insights(disease):
    """
    Generate detailed insights and care tips for the identified disease using OpenAI's chat-based model.
    """
    try:
        prompt = f"Provide detailed insights and care tips for {disease}."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the correct model name
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        insights = response.choices[0].message['content'].strip()
        print(f"Generated insights: {insights}")
        return insights
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {str(e)}")
        return "OpenAI API error occurred."
    except Exception as e:
        print(f"Error generating insights: {str(e)}")
        return "Error generating insights."

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
