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
        ('Hello','it','ciao'),
        ('sono sveglio','en', 'I\'m awake'),
        ('ek is wakker','en', 'I wake up'),
        ('буден съм','en', 'I\'m awake'),
        ('estic despert','en', 'I\'m awake'),
        ('budan sam','en', 'I\'m awake'),
        ('gising na ako','en', 'I awake'),
        ('tôi đang lên','en', 'I\'m up'),
        ('jag är vaken','en', 'I am awake'),
    ])

def test_translate(textToTranslate, desiredLanguage, ExpectedOutput):
    assert TextifyTranslate.translate(textToTranslate,desiredLanguage) == ExpectedOutput