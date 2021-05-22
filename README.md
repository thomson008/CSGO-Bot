# CSGO-Bot

A Discord bot designed for a Counter Strike: Global Offensive related server. 
It is currently capable of sending encouraging messages when it detects someone's message might have an angry or sad tone.
Furthermore, it can provide users with their most importans CS:GO statistics, such as number of kills or hours played.

As an extra, the bot can send a random inspirational quote.

### Implementation
This bot is written in Python, using Discord's Python API. Steam API is also used, 
wrapped with a special [Python framework for Steam](https://github.com/ValvePython/steam).

### Commands
Having the bot added to your Discord server, you can run the following commands by sending them as text messages:

```$stats``` - will print your CS:GO statistics

```$list``` - will list currently saved encouraging messages

```$new NEW_MESSAGE``` - will add "NEW_MESSAGE" to the list of encouraging messages

```$del INDEX``` - will delete an encouraging message at index INDEX

```$inspire``` - will send you a random inspirational quote, including its author

```$setid STEAM_ID``` - will store your Steam ID (specified as "STEAM_ID") in a database. It will be used to retrieve your statistics when running the `$stats` command

