# Textify Installation/Deployment Procedure

# Introduction

This document outlines a procedure for running (deploying) the Textify
bot that is a part of Team BDF’s final project in CS298-01 at Western
Connecticut State University. For more information about the project,
visit <https://github.com/smacademic/project-bdf>.

The document outlines the deployment process for Microsoft Windows and
Ubuntu. The procedure has been tested with Windows 10 Home Version 1809
and Ubuntu 16.04.6 LTS. However, the process should be similar in any
modern version of either operating system.

This document assumes some basic knowledge about Git/GitHub
repositories, installing programs, navigating a computer’s file system,
and in some cases, using a command line interface.

# Windows 

## Install dependencies

### Textify

The Textify bot’s code is hosted on GitHub and can be downloaded like
any other GitHub repository.

You may download a stable version of the bot through the releases page
(<https://github.com/smacademic/project-bdf/releases>) or clone the
repository and use any of the three long-lived branches:

  - `dev` – the most up-to-date version of the bot, not guaranteed to be
    stable or bug-free

  - `pre-production` – a version of the bot that is almost ready to be
    deployed to a production environment, but has not gone through
    extensive testing

  - `production` – the most stable version of the bot that is ready for
    production use

Note that the pre-production and production branches will not be used
until the Textify bot reaches v1.0.

### Python

The Textify bot is developed with Python 3 in mind and has not been
tested in Python 2. As such, we only recommend using Python 3 to run the
Textify bot.

On Windows, Python can be installed through an executable downloaded
from the official Python website: <https://www.python.org/downloads/>.
We recommend downloading Python 3.7.x. During the installation, if you
are asked whether you wish to add Python to the PATH environment
variable, we recommend choosing to do so.

You may also need the package installer `pip` depending on how you choose
to manage your Python environment. This is included in the Python
installer for modern versions of Python (see
<https://pip.pypa.io/en/stable/installing/>).

### Tesseract

Tesseract is a program and command line utility that performs the actual
character recognition that the Textify bot manages. It is installed as a
separate program on the computer that the Textify bot will be run on.

The official repository of the Tesseract project is located at
<https://github.com/tesseract-ocr/tesseract>. However, the project does
not officially distribute a Windows executable, and instead [points to
an installer](https://github.com/tesseract-ocr/tesseract/wiki#windows)
distributed by UB Mannheim. Up-to-date download links for this
distribution can be found
[here](https://github.com/UB-Mannheim/tesseract/wiki). In general, the
specific version of Tesseract used should not matter, however, most
testing so far has been performed on versions 4.0.0 and 4.1.0 (RC1).

When installing, you will be asked what languages and scripts you wish
to install. Currently, we recommend installing all languages, however,
this recommendation is likely to change in the future. To save time,
storage space, and network resources, you may only want to install some
of the most common languages (such as English). Also, when installing,
make a note of the installation directory for the tesseract executable.
By default, it is likely to be located at `C:\\Program
Files\\Tesseract-OCR\\tesseract.exe`.

### Python Modules

Tesseract currently requires the following modules not included by
default:

  - `praw`

  - `pytesseract`

  - `pytest`

These can be installed through `pip` or through an integrated development
environment (IDE) like Visual Studio. Full instructions for installing a
module using `pip` can be found in [`pip`’s
documentation](https://pip.pypa.io/en/stable/user_guide/#installing-packages).
However, in most cases, running the following commands in the Windows
Command Prompt should be enough:

```
pip install praw  
pip install pytesseract  
pip install pytest
```

Instructions for installing Python packages through IDEs will vary.
Instructions for Visual Studio can be found
[here](https://docs.microsoft.com/en-us/visualstudio/python/tutorial-working-with-python-in-visual-studio-step-05-installing-packages?view=vs-2019).

## Prepare for execution

Before running the bot, some configuration is necessary. This
configuration involves obtaining the credentials for the Textify bot and
setting configuration options.

### Credentials

For obvious reasons, the credentials for the Textify bot are not
publicly available. For members of Team BDF and other authorized users
(such as our instructor), the credentials are available in the Files tab
of the General channel of the CS298-S19-BDF team in Microsoft Teams.
However, the bot can be run with any Reddit account with API access
given the correct credentials for that account. These credentials should
be supplied in a file named authentication.py located in the same
directory as the botSetup.py script. This authentication file should
define the following variables:

  - `username`

  - `password`

  - `client\_id`

  - `client\_secret`

  - `user\_agent`

See [Reddit’s
documentation](https://github.com/reddit-archive/reddit/wiki/OAuth2) for
more information on obtaining these credentials for another account.

### Setting options

The following options should be set to their desired values before
running the Textify bot:

  - `WHITELIST` – A list of subreddits that the bot is allowed to post to.
    This can be disabled (so that the bot can post in any subreddit) by
    making the first item of the list the \* character.

  - `BLACKLIST` – A list of subreddits that the bot is not allowed to post
    to. This list is only used when the whitelist is disabled. This
    means that if a subreddit exists in both lists, then the bot will be
    allowed to post in the subreddit.

  - `IMAGE\_DIR` – The local directory in which to temporarily download
    images while they are being transcribed. This directory should exist
    prior to starting the bot. (The bot will **not** create directory if
    it does not exist)

  - `TESSERACT\_PATH` – OS path to the Tesseract executable. Note that
    since file paths in Windows use the `\` character, these separators
    must be escaped. The most common setting for this option is likely
    to be `'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'`. The
    actual location should be identified during installation of
    Tesseract.

  - `CHECKER` – A Boolean flag that specifies whether the bot should
    actually make posts to Reddit. If False, the bot will only echo the
    results of the transcription to the console.

These options are set as variables in the beginning of the TextifyBot.py
file and can be modified with any text editor.

## Run the project

Running the bot is the same as running most Python scripts, which means
it can be done directly through the console or through an IDE. The
script to run is the `TextifyBot.py` script. Once started, the script runs
continuously until it is terminated through a process such as a keyboard
interrupt (`CTRL-C`). Running it through the console is as simple as
navigating to the project’s src directory and running the following
command:

`python TextifyBot.py`
