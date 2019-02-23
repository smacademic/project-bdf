# Reddit Transcription Bot

The Reddit Transcription Bot (final name pending) transcribes text from images posted on Reddit on request. The images may be part of a post on a subreddit, or linked to within a comment. The bot will reply with a comment containing an attempted transcription of the text contained with the image.

This Reddit Bot is a part of a project created by 3 students in CS 298-01 at Western Connecticut State University. It is currently still within the initial planning process.

### Team Members
- Calebe De Aquino
- Brian Bacon
- Andrew Figueroa

### Original Project Idea

**High Level Description:** Social Media Bot

**Minimum Requirements:**

1. Ingest content from a social media platform using an API
2. Analyze content (identify relevant text). Involves parsing what is likely to be a JSON object
3. Generate a post based on the analyzed content. The post should have some markup other than text (hashtags, URLs, Markdown, etc)
4. Post to the social media site - Ideally. It is possible that external issues may prevent this from happening, in which case a simulated post is sufficient.

The project as currently defined meets requirements 1, 2, and 4. Requirement 3 is partially met (a post is generated, but it does not have any markup). This requirement can be fully met with some extentions to the project, such as identifying any URLS and turning them into hyperlinks, or possibly idenitying that the picutre is a screenshot of a Twitter post and linking to the original post on Twitter.

**Likely Social Media Platform:** Reddit

Reddit has a relatively generous public API and is friendly towards non-malicious bots. It also has a variety of content and many already existing bots that can be used for inspiration and guidance (what to do and not to do, e.g. some subreddits do not allow bots).

[Reddit API](https://www.reddit.com/dev/api)
[Reddit API Guidlines](https://github.com/reddit-archive/reddit/wiki/API)

## Dependencies (tentative)

- [Python Reddit API Wrapper (PRAW)](https://github.com/praw-dev/praw)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
