import requests
import time
import json
import gzip

import minion2JSON

# config
hypixel_request_attempt = 5
hypixel_bazaar_cache = 60  # in seconds
moulberry_bin_cache = 30 * 60 # in seconds

# cache
hypixel_bazaar = {'timestamp': 0, 'data': {}}
lowest_bin_items = {'timestamp': 0, 'data': {}}
apiKey_Hypixel = minion2JSON.openTextFile('./API/hypixel_token')


def isAPIlimit():
    r = requests.get('https://api.hypixel.net/key',
                     headers={'API-Key': apiKey_Hypixel})

    if(r.status_code == 200):
        body = r.json()
        if(body['success'] == True):
            return(False)
        if(body['success'] == False):
            return(True)
    return(True)


def getBazaarProducts():
    if((time.time() - hypixel_bazaar['timestamp']) > hypixel_bazaar_cache):
        attempt = 0
        while (isAPIlimit()):
            if(attempt == hypixel_request_attempt):
                return({
                    'success': False,
                    'cause': 'There is a problem talking to Hypixel API, Key throttle'
                })
            attempt += 1
            time.sleep(1)

        r = requests.get('https://api.hypixel.net/skyblock/bazaar',
                         headers={'API-Key': apiKey_Hypixel})

        if(r.status_code == 200):
            hypixel_bazaar['timestamp'] = time.time()
            hypixel_bazaar['data'] = r.json()
            return(r.json())

        return({
            'success': False,
            'cause': 'There is a problem talking to Hypixel API, ' + str(r.status_code)
        })
    return(hypixel_bazaar['data'])


def getSkyblockProfiles(minecraftUUID):
    attempt = 0
    while (isAPIlimit()):
        if(attempt == hypixel_request_attempt):
            return({
                'success': False,
                'cause': 'There is a problem talking to Hypixel API, Key throttle'
            })
        attempt += 1
        time.sleep(1)

    r = requests.get('https://api.hypixel.net/skyblock/profiles',
                     headers={'API-Key': apiKey_Hypixel}, params={'uuid': minecraftUUID})
    if(r.status_code == 200):
        data = r.json()
        return(data)

    return({
        'success': False,
        'cause': 'There is problem talking to Hypixel API, ' + str(r.status_code)
    })


def getShiiyuDungeonAPI(ign, profileName):
    r = requests.get('https://sky.shiiyu.moe/api/v2/dungeons/'+ign+'/'+profileName)

    status = r.status_code
    if status == 200:
        data = r.json()
        return {
            'success': True,
            'data': data
        }

    return {
        'success': False,
        'cause': str(status)
    }


def getShiiyuTalismansAPI(ign, profileName):
    r = requests.get('https://sky.shiiyu.moe/api/v2/talismans/'+ign+'/'+profileName)

    status = r.status_code
    if status == 200:
        data = r.json()
        return {
            'success': True,
            'data': data
        }
        
    return {
        'success': False,
        'cause': 'Not impl'
    }


def getLowestBINItems():
    if((time.time() - lowest_bin_items['timestamp']) > moulberry_bin_cache):
        r = requests.get('https://moulberry.codes/auction_averages_lbin/1day.json.gz', headers={'Accept-Encoding': 'gzip, deflate'})

        status = r.status_code
        if status == 200:
            lowest_bin_items['timestamp'] = time.time()
            lowest_bin_items['data'] = json.loads(gzip.decompress(r.content).decode())

            return {
                'success': True,
                'data': lowest_bin_items['data']   
            }

        return {
            'success': False,
            'cause': 'There is problem talking to Moulberry API, ' + str(status)
        }
    return {
        'success': True,
        'data': lowest_bin_items['data']
    }


def getLatestSkyblockProfile(minecraftUUID):
    profiles = getSkyblockProfiles(minecraftUUID)
    if(profiles['success'] == False):
        return({'success': False, 'cause': profiles['cause']})

    if(profiles['profiles'] is None):
        return({'success': False, 'cause': 'This user doesn\'t have any skyblock profile'})

    if(len(profiles['profiles']) == 1):
        return({'success': True, 'profile': profiles['profiles'][0]})

    latestTimestamp, latestSaveProfile = 0, {}
    for profile in profiles['profiles']:
        if('last_save' not in profile['members'][minecraftUUID]):
            continue
        if(profile['members'][minecraftUUID]['last_save'] > latestTimestamp):
            latestSaveProfile = profile
            latestTimestamp = profile['members'][minecraftUUID]['last_save']

    if(len(latestSaveProfile) == 0):
        return({'success': False, 'cause': 'This player doesn\'t have Skyblock profile'})
    return({'success': True, 'profile': latestSaveProfile})


def getMinecraftUUID(minecraftIGN):
    r = requests.get(
        'https://api.mojang.com/users/profiles/minecraft/' + minecraftIGN)
    status = r.status_code

    if(status == 200):
        data = r.json()
        return({'success': True, 'uuid': data['id'], 'name': data['name']})
    if(status == 204):
        return({'success': False, 'cause': '204 No Content'})

    return({'success': False, 'cause': str(status)})


def convertToDashedUUID(undashedUUID):
    # 8 4 4 4 12
    dashedUUID = undashedUUID[:8] + '-' + undashedUUID[8:]
    dashedUUID = dashedUUID[:13] + '-' + dashedUUID[13:]
    dashedUUID = dashedUUID[:18] + '-' + dashedUUID[18:]
    dashedUUID = dashedUUID[:23] + '-' + dashedUUID[23:]

    return dashedUUID


def getMinecraftIGN(minecraftUUID):
    r = requests.get(
        'https://api.mojang.com/user/profiles/' + minecraftUUID + '/names')
    status = r.status_code

    if(status == 200):
        data = r.json()
        return({'success': True, 'uuid': minecraftUUID, 'name': data[-1]['name']})
    if(status == 204):
        return({'success': False, 'cause': '204 No Content'})

    return({'success': False, 'cause': str(status)})
