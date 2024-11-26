import os

import re

import africastalking

import google.generativeai as genai

from flask import Flask, request

from dotenv import load_dotenv

import asyncio



import requests  # For connecting to Gemini API or other AI services



# Load environment variables

load_dotenv()



# Africa's Talking credentials and API keys

username = os.getenv("AFRICASTALKING_USERNAME", "sandbox")

api_key1 = os.getenv("AFRICASTALKING_API_KEY", "atsk_23fac71c5da57ab6959d909f6241bcecc93092bbac7b71f8386730d754cdbcd19986844f")

shortcode = os.getenv("AFRICASTALKING_SHORTCODE", "17419")  # Replace with your actual shortcode

keyword = "Coder"  # Define the keyword you’re using for animal health queries



# Initialize Africa's Talking and Gemini API

africastalking.initialize(username, api_key1)

sms = africastalking.SMS

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))



# Gemini AI model configuration

generation_config = {

    "temperature": 0.1,

    "top_p": 0.95,

    "top_k": 40,

    "max_output_tokens": 30,

    "response_mime_type": "text/plain",

}



model = genai.GenerativeModel(

    model_name="gemini-1.5-flash",

    generation_config=generation_config,

    system_instruction="""
You are an AI assistant trained to support expectant mothers by providing accurate and compassionate information on pregnancy-related topics. Respond in a friendly, professional tone, and focus on delivering helpful and easy-to-understand answers. Always prioritize user safety, encourage consulting healthcare professionals for serious concerns, and avoid providing medical diagnoses. You can answer questions in both English and Swahili and should be concise, informative, and friendly.The information you will provide should not exceed 160 characters frpo a normal sms structure.Always keep responses under 160 characters.

    """,

)



# Flask app setup

app = Flask(__name__)



# Function to send SMS



def send_sms(recipient, message):

    try:

        response = sms.send(message, [recipient])

        print("Message sent:", response)

    except Exception as e:

        print(f"Failed to send message: {str(e)}")



# Route to handle incoming SMS from Africa's Talking



# Gemini AI API settings

#gemini_api_url = "https://generativelanguage.googleapis.com/v1beta/models"

gemini_api_key = "AIzaSyCESwkCSyTgj3NXM6UlYQ2dKuzJ9JCKRYU"  # Replace with your actual API key



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



def get_gemini_response(query):

    import google.generativeai as genai



    genai.configure(api_key="AIzaSyCESwkCSyTgj3NXM6UlYQ2dKuzJ9JCKRYU")

    model = genai.GenerativeModel("gemini-1.5-flash")

    print("Model initialized:", model)



    try:

        response = model.generate_content(query)

        print("Generated Response:", response)

        return response.text if hasattr(response, 'text') else "No text attribute found in response"

    except Exception as e:

        print("Error during content generation:", e)

        return str(e)

    

def split_responce(response, limit=160):

    """

    This function splits a long message into multiple parts of 160 characters each

    to ensure compatibility with SMS length constraints.

    """

    # Split the message into parts of 160 characters each

    return [response[i:i + limit] for i in range(0, len(response), limit)]





# Start the Flask app[]

if __name__ == '___main___':

    app.run(port=5000, debug=True)