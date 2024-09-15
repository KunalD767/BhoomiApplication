from flask import Flask, request, jsonify
import openai
import API
app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = API.API_KEY

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No input provided'})

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant named Bhoomi specialized in agriculture in india."},
            {"role": "user", "content": user_input}
        ]
    )

    answer = response.choices[0].message['content']
    return jsonify({'response': answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
