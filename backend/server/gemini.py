import google.generativeai as genai
import os
from flask import Flask, request, jsonify
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv()

SECRET_KEY = os.getenv("GOOGLE_API_KEY")
app = Flask(__name__)

genai.configure(api_key=SECRET_KEY)

@app.route('/generate', methods=['GET','POST'])
def generate_text():
    if request.method == 'GET':
        curDisease = request.args.get('disease')
        print("cD: ",curDisease)
    else:  # POST request
        data = request.get_json()
        curDisease = data.get('disease')
    # data = request.get_json()
    # curDisease = data['disease']
    final_prompt = (
    f'For the crop disease: "{curDisease}", return only a JSON response with the following details: '
    '{"best_pesticide":, "amount_per_acre":, "recovery_time":}. '
    'Please ensure the pesticide, dosage, are realistic and relevant. '
    'Do not include any other text, only return the JSON.'
    )

    model = genai.GenerativeModel('gemini-1.5-flash') 
    if not final_prompt:
         return jsonify({'error': 'Prompt is required'}), 400

    response = model.generate_content(final_prompt,
                                      safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
    })

    res =  response.candidates[0].content.parts[0].text
    print(res)
    return jsonify({"response": res})


if __name__ == "__main__":
    app.run()