import sys
sys.path.append('..\\src')

import os
import TextifyBot
import pytest

images = []
images.append('test_images\\6731168-6436413-image-m-33_1543384208967.jpg')
images.append('test_images\\DNQSG48UIAAeahT.jpg')
images.append('test_images\\sleeping-squidward-spongebob-squarepants-meme-main.jpg')
images.append('test_images\\abraham-lincoln-famous-quotes.jpg')
@pytest.mark.parametrize("transcribeInput,transcribeExpected",
    [
        (images[0],'Me leaving the pot in the sink because\n“it needs to soak”'),
        (images[1],'When the teacher says a project will\ntake weeks to complete and you do it\nthe morning before it\'s due'),
        (images[2],'When you\'re about to go to sleep and\nyou remember you have homework'),
        (images[3],'Nearly all men can\nstand adversity,\nbut if you want to\ntest a man’s\ncharacter, give him\n\npower.\nGin, f, f\nChita Z (nce li\n\n[)sayingimages.com')
    ])
def test_tesseractTranscribe(transcribeInput, transcribeExpected):
    assert TextifyBot.tesseractTranscribe(transcribeInput) == transcribeExpected

list1 = ['Hello',' I',' am a student']
list2 = ['I\'m ready, ', 'I\'m ready, ', 'I am ready!']
list3 = ['one ', 'two ', 'three ', 'four ', 'five']
list4 = ['The purpose of this string is to', ' test whether the arrayToString() function is working as expected']
@pytest.mark.parametrize("inputList,expectedString",
    [
        (list1, "Hello I am a student"),
        (list2, "I\'m ready, I\'m ready, I am ready!"),
        (list3, "one two three four five"),
        (list4, "The purpose of this string is to test whether the arrayToString() function is working as expected")
    ])
def test_arrayToString(inputList, expectedString):
    assert TextifyBot.arrayToString(inputList) == expectedString

@pytest.mark.parametrize("markdownInput,markdownExpected",
    [
        ('Hello #I am Calebe', 'Hello \\#I am Calebe'),
        ('+This is the *second* markdown **syntax test**','\\+This is the \\*second\\* markdown \\*\\*syntax test\\*\\*'),
        ('_Work Hard_ to __Play Hard__','\\_Work Hard\\_ to \\_\\_Play Hard\\_\\_'),
        ('Hello \n Billy','Hello \n\n Billy')
    ])
def test_escapeMarkdown(markdownInput, markdownExpected):
    assert TextifyBot.escapeMarkdown(markdownInput) == markdownExpected