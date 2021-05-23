import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from steam_util import get_steam_data, set_new_id

client = discord.Client()

# List of keywords used for detecting "sad" messages
sad_words = [
    'kurde', 'słabo', 'badziewie', 'lipa', 'fatalnie', 
    'shit', 'sad', 'rip', 'dupa', 'ała', 'zginąłem', 'stupid', 
    'debil', 'retard', 'i died', 'they killed', 'crying'
]

# Basic encouraging messages that the bot will send
starter_encouragements = [
    "He's probably cheating.", 
    "You're just having a worse day :)",
    "Don't worry bro, it was just unlucky.", 
    "We'll get'em next time.",
    "Just take a break bro and you will come back stronger."
]


if 'responding' not in db.keys():
    db['responding'] = True


def get_quote():
    """
    Returns a random inspirational quote using zenquotes API
    """
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = '*' + json_data[0]['q'].strip() + '* ~ ' + json_data[0]['a']
    return quote


def update_encouragements(encouraging_message):
    """
    Adds new encouraging message to the starter list
    """
    if 'encouragements' in db.keys():
        encouragements = db['encouragements']
        encouragements.append(encouraging_message)
        db['encouragements'] = encouragements
    else:
        db['encouragements'] = [encouraging_message]


def delete_encouragement(index):
    """
    Deletes an encouraging message at given index
    """
    encouragements = db['encouragements']
    if len(encouragements) >= index > 0:
        deleted = encouragements[index-1]
        del encouragements[index-1]
        db['encouragements'] = encouragements
        return deleted
        

def list_encouragements():
    """
    Returns a list of all currently saved encouraging messages
    """
    encouragements = []
    response = 'I currently have the following **extra** messages: \n'
    if 'encouragements' in db.keys():
        encouragements = db['encouragements'].value

    for i, enc in enumerate(encouragements):
        response += f'{i+1}. *{enc}*\n'

    response += '\nI also have these **starter** messages:\n'
    for i, enc in enumerate(starter_encouragements):
        response += f'{i+1}. *{enc}*\n'

    return response


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    """
    Handles any incoming message
    """
    if message.author == client.user:
        return

    msg = message.content

    await check_for_sad_words(message, msg)
    await run_potential_command(message, msg)


async def toggle_responding(message, msg):
    """
    Switch bot responding to sad words on/off
    """
    try:
        value = msg.split('$responding ', 1)[1]
    except IndexError:
        value = '0'

    if value == '1' or value.lower() == 'true':
        db['responding'] = True
        await message.channel.send('I will now start responding!')
    else:
        db['responding'] = False
        await message.channel.send('I will stop responding now.')


async def check_for_sad_words(message, msg):
    """
    Send an encouragement if the message is sad
    """
    if db['responding']:
        options = starter_encouragements[:]
        if 'encouragements' in db.keys():
            options += db['encouragements']

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))


async def run_potential_command(message, msg):
    """
    Detect if a command was sent and run it
    """
    if msg.startswith('$stats'):
        response = await get_steam_data(client, message, os.environ['STEAM_API_KEY'])
        await message.channel.send(response)

    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if msg.startswith('$new'):
        encouraging_message = msg.split('$new ', 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send('Your new message was added!')

    if msg.startswith('$del'):
        await handle_deletion(message, msg)

    if msg.startswith('$responding'):
        await toggle_responding(message, msg)

    if msg.startswith('$list'):
        response = list_encouragements()
        await message.channel.send(response)

    if msg.startswith('$setid'):
        id = msg.split('$setid ', 1)[1]
        response = set_new_id(id, message.author)
        await message.channel.send(response)


async def handle_deletion(message, msg):
    if 'encouragements' in db.keys():
            index = int(msg.split('$del', 1)[1])
            deleted = delete_encouragement(index)

    if deleted:
        await message.channel.send(f'*{deleted}* was deleted.')


keep_alive()
client.run(os.environ['TOKEN'])