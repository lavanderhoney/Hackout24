from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Load environment variables from the .env file
# load_dotenv()

# SECRET_KEY = os.getenv("GOOGLE_API_KEY")
app = Flask(__name__)

genai.configure(api_key="AIzaSyBUlAWqGdBXhhy0CwSH6liMzhX-0E5OnO8")

# def get_rust_treatment_data(response):
#   """Extracts relevant data from GenerateContentResponse."""
#   # Assuming response is an instance of GenerateContentResponse
#   # Replace with appropriate attribute access based on response structure
#   data = {
#       "best_pesticide": response.best_pesticide,
#       "amount_per_acre": response.amount_per_acre,
#       "recovery_time": response.recovery_time
#   }
#   return json.dumps(data)

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()
    curDisease = data['disease']
    final_prompt = (
    f'For the crop disease: "{curDisease}", return only a JSON response with the following details: '
    '{"best_pesticide":, "amount_per_acre":, "recovery_time":}. '
    'Please ensure the pesticide, dosage, are realistic and relevant. '
    'Do not include any other text, only return the JSON.'
    )

    model = genai.GenerativeModel('gemini-1.5-flash')  # Choose your model
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


    # try:
    #     response = model.generate_content(final_prompt)
        # Check if the response contains valid content
    #     if 'candidates' in response and response['candidates']:
    #         # Extract the first candidate's text
    #         candidate = response['candidates'][0]
    #         if 'output' in candidate:
    #             generated_text = candidate['output']
    #         else:
    #             # Handle cases where the content might be blocked or invalid
    #             safety_ratings = candidate.get('safety_ratings', [])
    #             return jsonify({
    #                 'error': 'No valid content was returned. The response may have been blocked.',
    #                 'safety_ratings': safety_ratings
    #             }), 400
    #     else:
    #         return jsonify({'error': 'No candidates were returned in the response.'}), 400
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500

    return get_rust_treatment_data(response)

if __name__ == "__main__":
    app.run(debug=True)