import sys
sys.path.append('..\\src')
import TextifyTranslate
import pytest

@pytest.mark.parametrize("textToTranslate,desiredLanguage,ExpectedOutput",
    [
        ('Hello','es','Hola'),
        ('Hello','ja','こんにちは'),
        ('Hello','de','Hallo'),
        ('Hello','ar','مرحبا'),
        ('Hello','pt','Olá'),
        ('Hello','he','שלום'),
        ('Hello','hi','नमस्कार'),
        ('Hello','it','ciao')
    ])

def test_translate(textToTranslate, desiredLanguage, ExpectedOutput):
    assert TextifyTranslate.translate(textToTranslate,desiredLanguage) == ExpectedOutput