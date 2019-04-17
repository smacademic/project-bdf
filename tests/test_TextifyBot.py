import sys
sys.path.append('..\\src')
sys.path.append('C:\\Users\\caleb\\Documents\\GitHub\\project-bdf\\src')

import os
import TextifyBot
import pytest

images = []
images.append('C:\\Users\\caleb\\Documents\\GitHub\\project-bdf\\tests\\test_images\\6731168-6436413-image-m-33_1543384208967.jpg')
images.append('C:\\Users\\caleb\\Documents\\GitHub\\project-bdf\\tests\\test_images\\DNQSG48UIAAeahT.jpg')
images.append('C:\\Users\\caleb\\Documents\\GitHub\\project-bdf\\tests\\test_images\\sleeping-squidward-spongebob-squarepants-meme-main.jpg')
images.append('C:\\Users\\caleb\\Documents\\GitHub\\project-bdf\\tests\\test_images\\abraham-lincoln-famous-quotes.jpg')
@pytest.mark.parametrize("transcribeInput,transcribeExpected",
    [
        (images[0],'Me leaving the pot in the sink because\n“it needs to soak”'),
        (images[1],'When the teacher says a project will\ntake weeks to complete and you do it\nthe morning before it\'s due'),
        (images[2],'When you\'re about to go to sleep and\nyou remember you have homework'),
        (images[3],'Nearly all men can\nstand adversity,\nbut if you want to\ntest a man’s\ncharacter, give him\n\npower.\nGin, f, f\nChita Z (nce li\n\n[)sayingimages.com')
    ])
def test_tesseractTranscribe(transcribeInput, transcribeExpected):
    assert TextifyBot.tesseractTranscribe(transcribeInput) == transcribeExpected

@pytest.mark.parametrize("markdownInput,markdownExpected",
    [
        ('Hello #I am Calebe', 'Hello \\#I am Calebe'),
        ('+This is the *second* markdown **syntax test**','\\+This is the \\*second\\* markdown \\*\\*syntax test\\*\\*'),
        ('_Work Hard_ to __Play Hard__','\\_Work Hard\\_ to \\_\\_Play Hard\\_\\_'),
        ('Hello \n Billy','Hello \n\n Billy')
    ])
def test_escapeMarkdown(markdownInput, markdownExpected):
    assert TextifyBot.escapeMarkdown(markdownInput) == markdownExpected