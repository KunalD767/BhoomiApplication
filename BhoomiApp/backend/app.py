from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.models import load_model
from PIL import Image
import numpy as np
import json
import openai
import API
import logging
import csv
import os
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

openai.api_key = API.API_KEY

model_path = 'backend/crop_disease_model.h5'
class_labels_path = 'backend/class_labels.json'

try:
    model = load_model(model_path)
    app.logger.debug("Model loaded successfully.")
except Exception as e:
    app.logger.error(f"Error loading model: {str(e)}")

try:
    with open(class_labels_path) as f:
        class_labels = json.load(f)
    app.logger.debug("Class labels loaded successfully.")
except Exception as e:
    app.logger.error(f"Error loading class labels: {str(e)}")

def prepare_image(image, target_size=(150, 150)):
    """
    Preprocesses the input image to match the model's expected input.
    """
    image = image.resize(target_size)  
    image = np.array(image) 
    image = np.expand_dims(image, axis=0)  
    image = image / 255.0  
    app.logger.debug(f"Processed image shape: {image.shape}")
    return image

def generate_insights(disease):
    """
    Generate concise insights and care tips for the identified disease using OpenAI's chat-based model.
    """
    try:
        prompt = (
            f"The plant has {disease}. "
            "Provide four concise one-line care tips for this disease, formatted with a bullet point and a brief and it should include details like temparature moisture etc. to  "
            "summary of each tip. Example format: '- Tip: description.'"
        )
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant specialized in agriculture."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        insights = response.choices[0].message['content'].strip()
        app.logger.debug(f"Generated insights: {insights}")
        return insights
    except openai.error.OpenAIError as e:
        app.logger.error(f"OpenAI API error: {str(e)}")
        return "OpenAI API error occurred."
    except Exception as e:
        app.logger.error(f"Error generating insights: {str(e)}")
        return "Error generating insights."


@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Server is running'})

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
        disease = class_labels[predicted_class] if predicted_class < len(class_labels) else 'Unknown disease'
        app.logger.debug(f"Predicted disease: {disease}")

        insights = generate_insights(disease)
        app.logger.debug(f"Generated insights: {insights}")

        return jsonify({'disease': disease, 'insights': insights})
    except Exception as e:
        app.logger.error(f"Error during prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('message')
    if not user_input:
        app.logger.error('No input provided')
        return jsonify({'error': 'No input provided'}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": "You are a helpful assistant named Bhoomi specialized in agriculture in India."},
                {"role": "user", "content": user_input}
            ]
        )
        answer = response.choices[0].message['content']
        app.logger.debug(f"Chatbot response: {answer}")
        return jsonify({'response': answer})
    except openai.error.OpenAIError as e:
        app.logger.error(f"OpenAI API error: {str(e)}")
        return jsonify({'error': 'OpenAI API error occurred.'}), 500
    except Exception as e:
        app.logger.error(f"Error generating chatbot response: {str(e)}")
        return jsonify({'error': 'Error generating chatbot response.'}), 500

@app.route('/book', methods=['POST'])
def book():
    app.logger.debug("Received booking request")
    try:
        data = request.json
        name = data.get('name')
        address = data.get('address')
        phone_number = data.get('phone_number')

        if not name or not address or not phone_number:
            app.logger.error('Missing required fields')
            return jsonify({'error': 'Name, address, and phone number are required'}), 400

        csv_file = 'bookings.csv'

        file_exists = os.path.isfile(csv_file)

        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Name', 'Address', 'Phone Number'])
            writer.writerow([name, address, phone_number])

        app.logger.debug(f"Booking saved: {name}, {address}, {phone_number}")
        return jsonify({'message': 'Booking successful'})
    except Exception as e:
        app.logger.error(f"Error processing booking: {str(e)}")
        return jsonify({'error': 'Error processing booking'}), 500

@app.route('/register', methods=['POST'])
def register():
    app.logger.debug("Received registration data")
    try:
        data = request.json
        name = data.get('name')
        phone_number = data.get('phone_number')
        email = data.get('email')
        state = data.get('state')

        if not name or not phone_number or not email or not state:
            app.logger.error('Missing required fields')
            return jsonify({'error': 'Name, phone number, email, and state are required'}), 400

        csv_file = 'registration_data.csv'

        file_exists = os.path.isfile(csv_file)

        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Name', 'Phone Number', 'Email', 'State'])
            writer.writerow([name, phone_number, email, state])

        app.logger.debug(f"Registration saved: {name}, {phone_number}, {email}, {state}")
        return jsonify({'message': 'Registration successful'})
    except Exception as e:
        app.logger.error(f"Error processing registration: {str(e)}")
        return jsonify({'error': 'Error processing registration'}), 500


@app.route('/check_phone', methods=['POST'])
def check_phone():
    app.logger.debug("Received phone number for verification")
    try:
        data = request.json
        phone_number = data.get('phone_number')

        if not phone_number:
            app.logger.error('Phone number not provided')
            return jsonify({'exists': False, 'error': 'Phone number not provided'}), 400

        csv_file = 'registration_data.csv'

        if not os.path.isfile(csv_file):
            return jsonify({'exists': False, 'error': 'No registration data available'}), 404

        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Phone Number'] == phone_number:
                    app.logger.debug(f"Phone number {phone_number} exists in the records.")
                    return jsonify({'exists': True})

        app.logger.debug(f"Phone number {phone_number} does not exist in the records.")
        return jsonify({'exists': False, 'error': 'Phone number does not exist'}), 404

    except Exception as e:
        app.logger.error(f"Error checking phone number: {str(e)}")
        return jsonify({'exists': False, 'error': 'Error processing request'}), 500


@app.route('/get_user_data', methods=['POST'])
def get_user_data():
    app.logger.debug("Fetching user data")
    try:
        data = request.json
        phone_number = data.get('phone_number')

        if not phone_number:
            app.logger.error('Phone number not provided')
            return jsonify({'error': 'Phone number not provided'}), 400

        csv_file = 'registration_data.csv'

        if not os.path.isfile(csv_file):
            return jsonify({'error': 'No registration data available'}), 404

        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Phone Number'] == phone_number:
                    app.logger.debug(f"User data found for {phone_number}")
                    return jsonify({
                        'name': row.get('Name', ''),
                        'phone_number': row.get('Phone Number', ''),
                        'email': row.get('Email', ''),
                        'state': row.get('State', '')
                    })

        app.logger.debug(f"No user data found for {phone_number}")
        return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        app.logger.error(f"Error fetching user data: {str(e)}")
        return jsonify({'error': 'Error processing request'}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)