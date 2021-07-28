import os
import json
import requests

# WeatherStack API Access Key
ACCESS_KEY = os.environ['ACCESS_KEY']

def lambda_handler(event, context):
    
    # Get the city from Amazon Lex Input Event.
    city_input = event['currentIntent']['slots']['City']
    
    # Use query to pass the location to the API.
    params = {
      'access_key': ACCESS_KEY,
      'query': city_input
    }
    
    # Make a GET request to the URL of WeatherStack API. This establishes the connection from the chatbot to this API to retrieve the weather details for the city user provided.
    api_result = requests.get('http://api.weatherstack.com/current', params)
    api_response = api_result.json()
    
    # Get the response from Amazon Lex.
    # The dialogAction field directs Amazon Lex to the next course of action, and describes what to expect from the user after Amazon Lex returns a response to the client.
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "PlainText",
              "content": f'Current temperature in {api_response["location"]["name"]} is {api_response["current"]["temperature"]}℃. It is {api_response["current"]["weather_descriptions"][0]}.'  
            },
        }
    }
   
    return response