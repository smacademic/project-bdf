# TextifyTranslate.py - Team BDF - CS 298-01 S19 WCSU

# Script for implementing Microsoft Azure's Translator API

# The current implementation is based off of this quick-start guide:
# https://docs.microsoft.com/en-us/azure/cognitive-services/translator/quickstart-python-translate

import requests
import uuid
import json
import authentication

subscriptionKey = authentication.ttKey1
textToTranslate = 'Hi, I am a computer science student at Western Connecticut State University!'
desiredLanguage = 'pt'

base_url = 'https://api.cognitive.microsofttranslator.com'
path = '/translate?api-version=3.0'
params = '&to=' + desiredLanguage
constructed_url = base_url + path + params

headers = {
    'Ocp-Apim-Subscription-Key': subscriptionKey,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

body = [{
    'text' : textToTranslate
}]

request = requests.post(constructed_url, headers=headers, json=body)
response = request.json()

translatedText = response[0]['translations'][0]['text']
print(translatedText)