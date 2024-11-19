import os
import africastalking
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from transformers  import AutoModelForSeq2SeqLM, AutoTokenizer


# Load environment variables
load_dotenv()

# Initialize Africa's Talking
username = os.getenv("AFRICASTALKING_USERNAME", "Bandit0")
api_key = os.getenv("AFRICASTALKING_API_KEY")

africastalking.initialize(username, api_key)
sms = africastalking.SMS

# Initialize Flask app
app = Flask(__name__)

model_name = "ahmed807762/flan-t5-base-veterinaryQA_data-v2"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Function to send SMS
def send_sms(to, message):
    try:
        response = sms.send(message, [to])
        print(f"SMS sent: {response}")
        return response
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return str(e)

# Function to process SMS and generate response
# Function to process SMS and generate response
# Function to process SMS and generate response
def process_sms(sms_text):
    input_ids = tokenizer(sms_text, return_tensors="pt").input_ids
    output_ids = model.generate(input_ids, max_new_tokens=50)  # Allow longer responses
    generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    if not generated_text.strip():
        generated_text = "I'm sorry, I couldn't process your request. Please try again."
    
    print(f"Generated response: {generated_text}")  # Debugging
    return generated_text


# Endpoint to handle incoming SMS
@app.route('/incoming_sms', methods=['POST', 'GET'])
def incoming_sms():
    # Debug incoming request
    print(f"Incoming request: {request.form.to_dict()}")

    from_number = request.form.get('from')
    message_body = request.form.get('text')

    if not from_number or not message_body:
        return jsonify({"error": "Invalid request"}), 400

    print(f"Received SMS from {from_number}: {message_body}")

    # Process the SMS and generate a response
    response = process_sms(message_body)

    # Send the response as an SMS
    send_sms(from_number, response)

    return jsonify({"message": "SMS processed successfully"}), 200


if __name__ == '__main__':
    app.run(port=5000) 