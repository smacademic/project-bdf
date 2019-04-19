# TextifyVision.py - Team BDF - CS 298-01 S19 WCSU

# This python script provides functions for using Textiy's implementation of
# Micrisoft Azure's Computer Vision API

# The current implementation is based off of this quick-start guide:
# https://docs.microsoft.com/en-us/azure/cognitive-services/Computer-vision/QuickStarts/python-analyze

import requests
import json
import authentication

ANALYZE_URL = authentication.cvBaseURL + "/vision/v2.0/analyze"

# 0: a basketball about to enter a baskeball hoop
# 1: a plate of pasta topped with cheese and basil with bread in the background
urlsToAnalyze = ["https://i.imgur.com/045nXnj.jpg", "https://i.imgur.com/U598smz.jpg"]

for imageURL in urlsToAnalyze:
    callHeader = {"Ocp-Apim-Subscription-Key": authentication.cvKey1}
    callParams = {'visualFeatures': "Categories,Description,Color"}
    callData = {"url": imageURL}

    response = requests.post(ANALYZE_URL, headers=callHeader, params=callParams, json=callData)
    response.raise_for_status()

    result = response.json()
    #print(json.dumps(result))

    imageCaption = result["description"]["captions"][0]["text"]
    captionConfidence = result["description"]["captions"][0]["confidence"]
    print("I am " + str(captionConfidence * 100) + "% sure that this is:")
    print(imageCaption + "\n")
