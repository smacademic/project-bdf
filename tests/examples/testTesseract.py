# Team BDF
# Programmer: Calebe de Aquino
# Tesseract OCR Engine Test

import pytesseract

#Python Imaging Library
from PIL import Image
from PIL import ImageFilter


print(" Please input image file path :")
imagePath = input()
print('\n The file path is :' + imagePath + '\n')

image = Image.open(imagePath)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
text = pytesseract.image_to_string(image)

print(" Found text is :\n\n " + text + '\n\n')
