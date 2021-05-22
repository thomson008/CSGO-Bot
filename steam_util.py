from steam import webapi

APPID = '730'

def prepare_steam_data(steamid, STEAM_API_KEY):
    api = webapi.WebAPI(STEAM_API_KEY)

    try:
        stats = api.ISteamUserStats.GetUserStatsForGame(steamid=steamid, appid=APPID)
        stats = stats['playerstats']['stats'][:8]
    except:
        return ":rotating_light: Oops, looks like I don't have access to your Steam data. You have to set it to 'Public' first. :rotating_light:"

    emojis = [':gun:', ':skull:', ':timer:', ':firecracker:',
     ':shield:', ':trophy:', ':punch:', ':moneybag:' ]

    final_stats = ''

    for i, stat in enumerate(stats):
        final_stats += f"{emojis[i]} {' '.join(stat['name'].split('_')[1:])}: {stat['value']}\n"

    return final_stats