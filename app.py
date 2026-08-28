import os
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template,request
from google import genai
from google.genai import types

app = Flask(__name__, template_folder="TEMPLATE", static_folder="TEMPLATE")
load_dotenv()
client = genai.Client()

personality = """
You are DeepSea AI. Answer formally, professionally, and clearly. Give detailed
answers with examples and references when possible. Be respectful and polite.
Include a brief summary when it helps the user understand the answer.
"""
@app.route('/')
def home():
    return render_template('index.html')
api_key = os.getenv("GEMINI_API_KEY")

@app.route('/process', methods=['POST'])
def process_data():
    payload = request.get_json(silent=True) or {}
    user_input = payload.get('user_input', '').strip()
    if not user_input:
        return jsonify({'error': 'No question asked.'}), 400
    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=user_input,
            config=types.GenerateContentConfig(system_instruction=personality),
        )
        return jsonify({'response': response.text})
    except Exception as e:
        app.logger.exception("genmini api call failed")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

