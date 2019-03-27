import sys
sys.path.append('..\\src')
import botSetup

def test_extractURL():
    assert botSetup.extractURL('https://imgur.com/jfl3d8k.jpg') == ['https://imgur.com/jfl3d8k.jpg']
    assert botSetup.extractURL('https://imgur.com/jfl3d8k.png') == ['https://imgur.com/jfl3d8k.png']
    assert botSetup.extractURL('https://imgur.com/jfl3d8k.tif') == ['https://imgur.com/jfl3d8k.tif']
    assert botSetup.extractURL('https://imgur.com/jfl3d8k.jpg https://imgur.com/jfl3d8k.png') == \
    ['https://imgur.com/jfl3d8k.jpg', 'https://imgur.com/jfl3d8k.png']
    assert botSetup.extractURL('[This is a link](https://facebook.com/image.png) <- check out this link') == \
    ['https://facebook.com/image.png']
    assert botSetup.extractURL('I think that you will find this image useful \
    [https://google.com/fjkd.png](https://google.com/fjkd.png) Let me know what you think') == \
    ['https://google.com/fjkd.png']
    assert botSetup.extractURL('Hello my name is Brian, I am taking Devops this Spring 2019') == None
