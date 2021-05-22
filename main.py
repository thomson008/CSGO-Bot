import os
import discord
import requests
import json
import random
import re
from replit import db
from keep_alive import keep_alive
from steam_util import prepare_steam_data

client = discord.Client()

sad_words = [
    'kurde', 'słabo', 'fuck', 'badziewie', 'lipa', 'fatalnie', 
    'shit', 'sad', 'rip', 'dupa', 'ała', 'zginąłem', 'stupid', 
    'debil', 'retard', 'i died', 'they killed', 'crying'
]

starter_encouragements = [
    'He\'s probably cheating.', 
    'You\'re just having a worse day :)',
    'Don\'t worry bro, it was just unlucky.', 
    'We\'ll get\'em next time.',
    'Just take a break bro and you will come back stronger.'
]


if 'responding' not in db.keys():
    db['responding'] = True


def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = '*' + json_data[0]['q'].strip() + '* ~ ' + json_data[0]['a']
    return quote


def update_encouragements(encouraging_message):
    if 'encouragements' in db.keys():
        encouragements = db['encouragements']
        encouragements.append(encouraging_message)
        db['encouragements'] = encouragements
    else:
        db['encouragements'] = [encouraging_message]


def delete_encouragement(index):
    encouragements = db['encouragements']
    if len(encouragements) >= index > 0:
        deleted = encouragements[index-1]
        del encouragements[index-1]
        db['encouragements'] = encouragements
        return deleted
        

def list_encouragements():
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


async def get_steam_data(message):
    STEAM_API_KEY = os.environ['STEAM_API_KEY']
    author = str(message.author)
    response = ''  

    if author in db.keys():
        steamid = db[author]
    else:
        await message.channel.send('I don\'t know your Steam ID. Please send it.')
        id_provided = False
        while not id_provided:
            msg = await client.wait_for("message")
            id_provided = validate_id_message(msg, message)
            if not id_provided and msg.author != client.user:
                await message.channel.send('Invalid ID. Please try again.')
        steamid = msg.content
        db[author] = steamid
        response += f'I saved your Steam ID to my database!\n'
   
    stats = prepare_steam_data(steamid, STEAM_API_KEY)
    response += f'Here are your **CS:GO stats**, {message.author.mention}:\n\n{stats}'
    
    return response


def validate_id(id):
    return re.search('[0-9]{17}', id)

def validate_id_message(msg, message):
    matching_author = message.author == msg.author
    return validate_id(msg.content) and matching_author


def set_new_id(id, author):
    if not validate_id(id):
        return 'This ID is invalid. Try the command again with a valid ID.'
    db[str(author)] = id
    return f'Your new Steam ID was set, {author.mention}!'

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('$stats'):
        response = await get_steam_data(message)
        await message.channel.send(response)

    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if db['responding']:
        options = starter_encouragements[:]
        if 'encouragements' in db.keys():
            options += db['encouragements']

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

    if msg.startswith('$new'):
        encouraging_message = msg.split('$new ', 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send('Your new message was added!')

    if msg.startswith('$del'):
        if 'encouragements' in db.keys():
            index = int(msg.split('$del', 1)[1])
            deleted = delete_encouragement(index)

        if deleted:
            await message.channel.send(f'*{deleted}* was deleted.')

    if msg.startswith('$list'):
        response = list_encouragements()
        await message.channel.send(response)

    if msg.startswith('$setid'):
        id = msg.split('$setid ', 1)[1]
        response = set_new_id(id, message.author)
        await message.channel.send(response)

    if msg.startswith('$responding'):
        value = msg.split('$responding ', 1)[1]

        if value == '1' or value.lower == 'true':
            db['responding'] = True
            await message.channel.send('I will now start responding!')
        else:
            db['responding'] = False
            await message.channel.send('I will stop responding now.')

keep_alive()
client.run(os.environ['TOKEN'])