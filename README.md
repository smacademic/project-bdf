# Textify - An Unofficial Reddit Transcription Bot

Textify transcribes text from images posted on Reddit on request. The images may be part of a post on a subreddit, or linked to within a comment. The bot will reply with a comment containing an attempted transcription of the text contained with the image. [Here](https://github.com/smacademic/project-bdf/blob/dev/docs/TranscriptionRequestGuide.md) is the guide for requesting
transcriptions from Textify.

This Reddit Bot is a part of a project created by 3 students in CS 298-01 at Western Connecticut State University. Development is currently underway and the project is still in its alpha stages. Transcriptions are performed, but the results are not formatted well and often have errors.

Outside collaboration is not currently expected as the project is part of a major graded assignment. However, feedback or suggestions are welcome. The easiest way to make these comments is to send a [Reddit inbox message to the /u/TextifyReddit account](https://www.reddit.com/message/compose/?to=TextifyReddit).

### Team Members
- Calebe de Aquino
- Brian Bacon
- Andrew Figueroa

## Original Project Idea

**High Level Description:** Social Media OCR Bot

**Minimum Requirements:**

1. Ingest content from Reddit using an API
2. Analyze content from a comment or submission
3. Generate a post based on the analyzed content. The post should have some markup other than text (hashtags, URLs, Markdown, etc)
4. Post to Reddit. It is possible that external issues may prevent this from happening, in which case a simulated post is sufficient.

The project as currently implemented meets all the requirements.

**Extensions:**
- Translation: Converting any found language to a specified langauge through the use of Microsoft Azure's Translator Text
- Image description: Depict an image along with the confidence percentage through the use of Microsoft Azure's Computer Vision
- Locating tweet: Search the internet for possible tweet through the use of Google

### Why we chose Reddit

Reddit has a relatively generous public API and is friendly towards non-malicious bots. It also has a variety of content and many already existing bots that can be used for inspiration and guidance (what to do and not to do, e.g. some subreddits do not allow bots).

[Reddit API](https://www.reddit.com/dev/api)
[Reddit API Guidlines](https://github.com/reddit-archive/reddit/wiki/API)

## Dependencies (tentative)

- [Python Reddit API Wrapper (PRAW)](https://github.com/praw-dev/praw)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Pytest](https://docs.pytest.org/en/latest/)

## Installation

The installation/deployment procedure for both Windows and Ubuntu is detailed [here](https://github.com/smacademic/project-bdf/blob/dev/docs/InstallationProcess.md).

## System Architecture

![System Architecture Diagram](https://i.imgur.com/kMBMQHV.png)

  1.User A posts an image to Reddit

  2.User B (who may have visual impairments) posts a comment requesting Textify to process the image

  3.The Textify server receives a notification. The image is then processed, utilizing Microsoft Azure to describe an image or translate text (if requested)

  4.The Textify server posts a reply containing the transcription to user B’s comment

  5.User B receives a notification that Textify has responded with a transcription
