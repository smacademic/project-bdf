import sys
sys.path.append('..\\src')
sys.path.append('C:\\Users\\caleb\\Documents\\GitHub\\project-bdf\\src')

import os
import TextifyBot

def test_tesseractTranscribe():
    print("Testing function tesseractTranscribe()")

    images = []
    images.append('C:\\Users\\caleb\\Documents\\GitHub\\project-bdf\\tests\\test_images\\6731168-6436413-image-m-33_1543384208967.jpg')
    images.append('C:\\Users\\caleb\\Documents\\GitHub\\project-bdf\\tests\\test_images\\DNQSG48UIAAeahT.jpg')
    images.append('C:\\Users\\caleb\\Documents\\GitHub\\project-bdf\\tests\\test_images\\sleeping-squidward-spongebob-squarepants-meme-main.jpg')
    images.append('C:\\Users\\caleb\\Documents\\GitHub\\project-bdf\\tests\\test_images\\abraham-lincoln-famous-quotes.jpg')

    assert TextifyBot.tesseractTranscribe(images[0]) == 'Me leaving the pot in the sink because\n“it needs to soak”'
    assert TextifyBot.tesseractTranscribe(images[1]) == \
    'When the teacher says a project will\ntake weeks to complete and you do it\nthe morning before it\'s due'
    assert TextifyBot.tesseractTranscribe(images[2]) == \
    'When you\'re about to go to sleep and\nyou remember you have homework'
    assert TextifyBot.tesseractTranscribe(images[3]) == \
    'Nearly all men can\nstand adversity,\nbut if you want to\ntest a man’s\ncharacter, give him\n\npower.\nGin, f, f\nChita Z (nce li\n\n[)sayingimages.com'

def test_arrayToString():

    testArrayOfText1 = ['Hello', ', I am',' coming for you']
    testArrayOfText2 = ['Sample text ','to check and see if',' the function arrayToString() works as expected']
    testArrayOfText3 = ['Checking to',' see if this function',' can turn an array or list of strings into one string']

    assert TextifyBot.arrayToString(testArrayOfText1) == 'Hello, I am Calebe'
    assert TextifyBot.arrayToString(testArrayOfText2) == 'Sample text to check and see if the function arrayToString() works as expected'
    assert TextifyBot.arrayToString(testArrayOfText3) == 'Checking to see if this function can turn an array or '

def test_escapeMarkdown():

    test1 = "Hello #I am Calebe"
    test2 = "+This is the *second* markdown **syntax test**"
    test3 = "_Work Hard_ to __Play Hard__"
    test4 = "Hello \n Billy"

    assert (TextifyBot.escapeMarkdown(test1)) == 'Hello \\#I am Calebe'
    assert (TextifyBot.escapeMarkdown(test2)) == '\\+This is the \\*second\\* markdown \\*\\*syntax test\\*\\*'
    assert (TextifyBot.escapeMarkdown(test3)) == '\\_Work Hard\\_ to \\_\\_Play Hard\\_\\_'
    assert (TextifyBot.escapeMarkdown(test4)) == 'Hello \n\n Billy'