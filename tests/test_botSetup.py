import sys
sys.path.append('..\\src')
import botSetup
import pytest

@pytest.mark.parametrize("extractInput,extractExpected",
    [
        ('https://imgur.com/jfl3d8k.jpg',['https://imgur.com/jfl3d8k.jpg']),
        ('https://imgur.com/jfl3d8k.png',['https://imgur.com/jfl3d8k.png']),
        ('https://imgur.com/jfl3d8k.tif',['https://imgur.com/jfl3d8k.tif']),
        ('https://imgur.com/jfl3d8k.jpg https://imgur.com/jfl3d8k.png',['https://imgur.com/jfl3d8k.jpg', 'https://imgur.com/jfl3d8k.png']),
        ('[This is a link](https://facebook.com/image.png) <- check out this link',['https://facebook.com/image.png']),
        ('I think that you will find this image useful [https://google.com/fjkd.png](https://google.com/fjkd.png) Let me know what you think',\
            ['https://google.com/fjkd.png']),
        ('Hello my name is Brian, I am taking Devops this Spring 2019',None)
    ])
def test_extractURL(extractInput, extractExpected):
    assert botSetup.extractURL(extractInput) == extractExpected
