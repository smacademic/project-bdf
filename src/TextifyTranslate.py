# TextifyTranslate.py - Team BDF - CS 298-01 S19 WCSU

# Script for implementing Microsoft Azure's Translator API

# The current implementation is based off of this quick-start guide:
# https://docs.microsoft.com/en-us/azure/cognitive-services/translator/quickstart-python-translate

import requests
import json
import authentication

LANGUAGE_CODE = ['af','ar','bn','bs','bg','yue','ca','zh-Hans','zh-Hant','hr', \
                'cs','da','nl','en','et','fj','fil','fi','fr','de','el','ht', \
                'he','hi','mww','hu','is','id','it','ja','sw','tlh','tlh-Qaak', \
                'ko','lv','lt','mg','ms','mt','nb','fa','pl','pt','otq','ro', \
                'ru','sm','sr-Cyrl','sr-Latn','sk','sl','es','sv','ty','ta','te', \
                'th','to','tr','uk','ur','vi','cy','yua']

def translate(textToTranslate, desiredLanguage):

    #textToTranslate = 'hello'
    #desiredLanguage = 'pt'

    base_url = 'https://api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'
    params = '&to=' + desiredLanguage
    constructed_url = base_url + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': authentication.ttKey1,
        'Content-type': 'application/json',
    }

    body = [{
        'text' : textToTranslate
    }]

    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()

    translatedText = response[0]['translations'][0]['text']
    return translatedText