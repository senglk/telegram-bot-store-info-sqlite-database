# telegram-bot-store-info-sqlite-database

## Introduction

This sample script starts a [Telegram bot](https://core.telegram.org/bots) which saves user input into a [SQLite3](https://www.sqlite.org/) database as the user interacts with the bot.

The script was adapted from the example [conversationbot2](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot2.py) from [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).

## Prerequisites

### Python 3

This script was written for Python 3 (preferably 3.3 and above).

The script requires the following libraries (and dependencies therein).

### python-telegram-bot

A library for the [Telegram Bot API](https://core.telegram.org/bots/api).

You can install or upgrade the python-telegram-bot library with:
````
$ pip install python-telegram-bot --upgrade
````

For more information please refer to [PyPI](https://pypi.python.org/pypi/python-telegram-bot) or [Github](https://github.com/python-telegram-bot/python-telegram-bot). 

### SQLite3

SQLite3 should be included in the standard library.

For more information please refer to the [SQLite3 Documentation](https://docs.python.org/3.5/library/sqlite3.html).

## Usage

### Updating with your bot's token.

Please update the [token](https://core.telegram.org/bots#6-botfather) of your bot before starting the script.

The token goes between the quotation marks of the `Update` call in the `main` function.

Currently the placeholder text where the token should be is `TOKEN:token`.

### Starting the bot

You can start the script in Windows Powershell or command prompt with:
```
> py -3 telephone.py
```

or on Linux terminal with:
```
$ python3 telephone.py
```

### Terminating the bot
You can terminate the bot by pressing `Ctrl+C`.

## Browsing the SQLite3 Database

You may browse the SQLite3 file using [DB Browser for SQLite](http://sqlitebrowser.org/).