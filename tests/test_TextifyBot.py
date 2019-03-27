import sys
sys.path.append('..\\src')
import os
import TextifyBot
import pytest

def test_tesseractTranscribe():
    images = []
    images.append('test_images\\6731168-6436413-image-m-33_1543384208967.jpg')
    images.append('test_images\\DNQSG48UIAAeahT.jpg')
    images.append('test_images\\eHs1xVU.jpg')
    images.append('test_images\\sleeping-squidward-spongebob-squarepants-meme-main.jpg')

    assert TextifyBot.tesseractTranscribe(images[0]) == 'Me leaving the pot in the sink because\n“it needs to soak”'
    assert TextifyBot.tesseractTranscribe(images[1]) == \
    'When the teacher says a project will\ntake weeks to complete and you do it\nthe morning before it\'s due'
    assert TextifyBot.tesseractTranscribe(images[2]) == 'Meek coming back with a diss\ntrack like'
    assert TextifyBot.tesseractTranscribe(images[3]) == \
    'When you\'re about to go to sleep and\nyou remember you have homework'
