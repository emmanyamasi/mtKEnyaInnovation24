import os
from flask import Flask, request
from dotenv import load_dotenv
import africastalking
from google.generativeai import configure, GenerativeModel
# Load environment variables
load_dotenv()

# Validate environment variables
required_env_vars = ["AFRICASTALKING_USERNAME", "AFRICASTALKING_API_KEY", "GEMINI_API_KEY"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Africa's Talking setup
username = os.getenv("AFRICASTALKING_USERNAME")
api_key = os.getenv("AFRICASTALKING_API_KEY")
shortcode = os.getenv("AFRICASTALKING_SHORTCODE", "17419")
keyword = "Coder"
africastalking.initialize(username, api_key)
sms = africastalking.SMS

# Gemini API setup
gemini_api_key = os.getenv("GEMINI_API_KEY")
configure(api_key=gemini_api_key)

# Define the system instruction for the Gemini model

# Load the Gemini model with configuration
generation_config = {
    "temperature": 0.05,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 150,
}



model = GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
     system_instruction="You are an AI assistant trained to support expectant mothers by providing accurate and compassionate information on pregnancy-related topics. Respond in a friendly, professional tone, and focus on delivering helpful and easy-to-understand answers. Always prioritize user safety, encourage consulting healthcare professionals for serious concerns, and avoid providing medical diagnoses.",
)

# Flask app
app = Flask(__name__)

def send_sms(recipient, message):

    try:

        response = sms.send(message, [recipient])

        print("Message sent:", response)

    except Exception as e:

        print(f"Failed to send message: {str(e)}")


def get_gemini_response(query):

    import google.generativeai as genai



    genai.configure(api_key='AIzaSyCuNmwq7xzrrBdILrKHcuuR2uV3IGzqX4E')

    model = genai.GenerativeModel("gemini-1.5-flash")

    print("Model initialized:", model)



    try:

        response = model.generate_content(query)

        print("Generated Response:", response)

        return response.text if hasattr(response, 'text') else "No text attribute found in response"

    except Exception as e:

        print("Error during content generation:", e)

        return str(e)

    


@app.route("/incoming_sms", methods=["POST","GET"])

def incoming_sms():

    # Get the SMS details

    data = request.form 

    sender = data.get("from")  # User's phone number

    message = data.get("text").strip().lower()  # The SMS content



    # Extract the query

    if message.startswith("coder"):

        query = message.replace("coder", "").strip()

        print(f"{query}")



        if query:

            # Forward the query to Gemini API

            ai_response = get_gemini_response(query)

            print(f"AI Response: {ai_response}")



            # Reply to the user

            send_sms(sender, ai_response)

        else:

            send_sms(sender, "Please include a query after 'Coder'.")

    else:

        send_sms(sender, "Invalid message format. Start with 'Coder'.")



    return "Message received", 200





def split_responce(response, limit=160):

    """

    This function splits a long message into multiple parts of 160 characters each

    to ensure compatibility with SMS length constraints.

    """

    # Split the message into parts of 160 characters each

    return [response[i:i + limit] for i in range(0, len(response), limit)]


if __name__ == "__main__":
    app.run(port=5000, debug=False)
