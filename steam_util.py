from steam import webapi
from replit import db
import re
import datetime

APPID = '730'

def prepare_steam_data(steamid, STEAM_API_KEY):
    """
    Fetch user statistics from API and format them
    """
    api = webapi.WebAPI(STEAM_API_KEY)

    try:
        stats = api.ISteamUserStats.GetUserStatsForGame(steamid=steamid, appid=APPID)
        stats = stats['playerstats']['stats'][:8]
    except:
        return (":rotating_light: Oops, looks like I don't have access to your Steam data. "
        "You have to set it to 'Public' first. :rotating_light:")

    emojis = [':gun:', ':skull:', ':timer:', ':firecracker:',
     ':shield:', ':trophy:', ':punch:', ':moneybag:' ]

    final_stats = ''

    for i, stat in enumerate(stats):
        value = stat['value']
        if stat['name'] == 'total_time_played':
            value = str(datetime.timedelta(seconds=value))

        final_stats += f"{emojis[i]} {' '.join(stat['name'].split('_')[1:])}: {value}\n"

    return final_stats


async def get_steam_data(client, message, STEAM_API_KEY):
    """
    Handle an user request for CS:GO statistics
    Send a message with formatted statistics once they are ready
    """
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
    return validate_id(msg.content) and message.author == msg.author


def set_new_id(id, author):
    """
    Manually set Steam ID for a Discord user that requests it
    """
    if not validate_id(id):
        return 'This ID is invalid. Try the command again with a valid ID.'
    db[str(author)] = id
    return f'Your new Steam ID was set, {author.mention}!'