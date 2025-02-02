import base64
import nbt
import io
import requests

import minion2JSON
import hypixelAPI


def getTalismansData():
    try:
        r = requests.get(
            'https://raw.githubusercontent.com/SkyCryptWebsite/SkyCrypt/master/src/constants/talismans.js')
        newData = r.text.strip()
        warning = ''

        f = open('./resources/talismans.js', 'r+')
        oldData = f.read().strip()
        if(oldData == ''):
            f.write(newData)
            f.seek(0)
            oldData = f.read()

        if(oldData != newData):
            warning = 'Outdated talismans data, please contact Tonkaew#2345'

        f.close()
        return {
            'success': True,
            'warning': warning,
            'data': minion2JSON.openJSONFile('./resources/talismans_data.json')
        }
    except Exception as e:
        return {
            'success': True,
            'warning': 'Can\'t check with latest talisman data, please contact Tonkaew#2345',
            'data': minion2JSON.openJSONFile('./resources/talismans_data.json')
        }


def convertCatacombXp2Lvl(cataXp):
    dungeonExperience = [0, 50, 125, 235, 395, 625, 955, 1425, 2095, 3045, 4385, 6275, 8940, 12700, 17960, 25340, 35640, 50040, 70040, 97640, 135640, 188140, 259640, 356640, 488640, 668640, 911640, 1239640, 1684640, 2284640,
                         3084640, 4149640, 5559640, 7459640, 9959640, 13259640, 17559640, 23159640, 30359640, 39559640, 51559640, 66559640, 85559640, 109559640, 139559640, 177559640, 225559640, 285559640, 360559640, 453559640, 465184640]
    for i in range(len(dungeonExperience)):
        if(dungeonExperience[i] > cataXp):
            return(i - 1)
    return(len(dungeonExperience) - 1)


def decodeInventoryData(raw):
    data = nbt.nbt.NBTFile(fileobj=io.BytesIO(base64.b64decode(raw)))
    return(data)


def removeColorCode(text):
    text = str(text)
    colorCode = [u'§4', u'§c', u'§6', u'§e', u'§2', u'§a', u'§b',
                 u'§3', u'§1', u'§9', u'§d', u'§5', u'§f', u'§7', u'§8', u'§0']

    for color in colorCode:
        if color in text:
            text = text.replace(color, '')
    return(text)


def convertInventory2List(inv):
    items = []

    for tag in inv['i'].tags:
        if(tag.tag_info()[15] != '0'):
            amount = removeColorCode(tag['Count'].tag_info()[19:])
            name = removeColorCode(
                tag['tag']['display']['Name'].tag_info()[20:])

            items.append(name)
    return items


def convertPetXp2Lvl(petXp, rarity):
    petLevel = {
        'COMMON': [0, 100, 210, 330, 460, 605, 765, 940, 1130, 1340, 1570, 1820, 2095, 2395, 2725, 3085, 3485, 3925, 4415, 4955, 5555, 6215, 6945, 7745, 8625, 9585, 10635, 11785, 13045, 14425, 15935, 17585, 19385, 21345, 23475, 25785, 28285, 30985, 33905, 37065, 40485, 44185, 48185, 52535, 57285, 62485, 68185, 74485, 81485, 89285, 97985, 107685, 118485, 130485, 143785, 158485, 174685, 192485, 211985, 233285, 256485, 281685, 309085, 338885, 371285, 406485, 444685, 486085, 530885, 579285, 631485, 687685, 748085, 812885, 882285, 956485, 1035685, 1120385, 1211085, 1308285, 1412485, 1524185, 1643885, 1772085, 1909285, 2055985, 2212685, 2380385, 2560085,
                   2752785, 2959485, 3181185, 3418885, 3673585, 3946285, 4237985, 4549685, 4883385, 5241085, 5624785, 6036485],
        'UNCOMMON': [0, 765, 940, 1130, 1340, 1570, 1820, 2095, 2395, 2725, 3085, 3485, 3925, 4415, 4955, 5555, 6215, 6945, 7745, 8625, 9585, 10635, 11785, 13045, 14425, 15935, 17585, 19385, 21345, 23475, 25785, 28285, 30985, 33905, 37065, 40485, 44185, 48185, 52535, 57285, 62485, 68185, 74485, 81485, 89285, 97985, 107685, 118485, 130485, 143785, 158485, 174685, 192485, 211985, 233285, 256485,
                     281685, 309085, 338885, 371285, 406485, 444685, 486085, 530885, 579285, 631485, 687685, 748085, 812885, 882285, 956485, 1035685, 1120385, 1211085, 1308285, 1412485, 1524185, 1643885, 1772085, 1909285, 2055985, 2212685, 2380385, 2560085, 2752785, 2959485, 3181185, 3418885, 3673585, 3946285, 4237985, 4549685, 4883385, 5241085, 5624785, 6036485, 6478185, 6954885, 7471585, 8033285, 8644985],
        'RARE': [0, 1820, 2095, 2395, 2725, 3085, 3485, 3925, 4415, 4955, 5555, 6215, 6945, 7745, 8625, 9585, 10635, 11785, 13045, 14425, 15935, 17585, 19385, 21345, 23475, 25785, 28285, 30985, 33905, 37065, 40485, 44185, 48185, 52535, 57285, 62485, 68185, 74485, 81485, 89285, 97985, 107685, 118485, 130485, 143785, 158485, 174685, 192485, 211985, 233285, 256485, 281685, 309085, 338885, 371285, 406485, 444685, 486085,
                 530885, 579285, 631485, 687685, 748085, 812885, 882285, 956485, 1035685, 1120385, 1211085, 1308285, 1412485, 1524185, 1643885, 1772085, 1909285, 2055985, 2212685, 2380385, 2560085, 2752785, 2959485, 3181185, 3418885, 3673585, 3946285, 4237985, 4549685, 4883385, 5241085, 5624785, 6036485, 6478185, 6954885, 7471585, 8033285, 8644985, 9311685, 10038385, 10830085, 11691785, 12628485],
        'EPIC': [0, 3485, 3925, 4415, 4955, 5555, 6215, 6945, 7745, 8625, 9585, 10635, 11785, 13045, 14425, 15935, 17585, 19385, 21345, 23475, 25785, 28285, 30985, 33905, 37065, 40485, 44185, 48185, 52535, 57285, 62485,
                 68185, 74485, 81485, 89285, 97985, 107685, 118485, 130485, 143785, 158485, 174685, 192485, 211985, 233285, 256485, 281685, 309085, 338885, 371285, 406485, 444685, 486085, 530885, 579285, 631485, 687685, 748085, 812885, 882285, 956485, 1035685, 1120385, 1211085, 1308285, 1412485, 1524185, 1643885, 1772085, 1909285, 2055985, 2212685, 2380385, 2560085, 2752785, 2959485, 3181185, 3418885, 3673585, 3946285, 4237985, 4549685, 4883385, 5241085, 5624785, 6036485, 6478185, 6954885, 7471585, 8033285, 8644985, 9311685, 10038385, 10830085, 11691785, 12628485, 13645185, 14746885, 15938585, 17225285, 18611985],
        'LEGENDARY': [0, 5555, 6215, 6945, 7745, 8625, 9585, 10635, 11785, 13045, 14425, 15935, 17585, 19385, 21345, 23475, 25785, 28285, 30985, 33905, 37065, 40485, 44185, 48185, 52535, 57285, 62485, 68185, 74485, 81485, 89285, 97985, 107685, 118485, 130485, 143785, 158485, 174685, 192485, 211985, 233285, 256485, 281685, 309085, 338885, 371285, 406485, 444685, 486085, 530885, 579285, 631485, 687685, 748085, 812885, 882285,
                      956485, 1035685, 1120385, 1211085, 1308285, 1412485, 1524185, 1643885, 1772085, 1909285, 2055985, 2212685, 2380385, 2560085, 2752785, 2959485, 3181185, 3418885, 3673585, 3946285, 4237985, 4549685, 4883385, 5241085, 5624785, 6036485, 6478185, 6954885, 7471585, 8033285, 8644985, 9311685, 10038385, 10830085, 11691785, 12628485, 13645185, 14746885, 15938585, 17225285, 18611985, 20108685, 21725385, 23472085, 25358785],
        'MYTHIC': [0, 5555, 6215, 6945, 7745, 8625, 9585, 10635, 11785, 13045, 14425, 15935, 17585, 19385, 21345, 23475, 25785, 28285, 30985, 33905, 37065, 40485, 44185, 48185, 52535, 57285, 62485, 68185, 74485, 81485, 89285, 97985, 107685, 118485, 130485, 143785, 158485, 174685, 192485, 211985, 233285, 256485, 281685, 309085, 338885, 371285, 406485, 444685, 486085, 530885, 579285, 631485, 687685, 748085, 812885, 882285,
                   956485, 1035685, 1120385, 1211085, 1308285, 1412485, 1524185, 1643885, 1772085, 1909285, 2055985, 2212685, 2380385, 2560085, 2752785, 2959485, 3181185, 3418885, 3673585, 3946285, 4237985, 4549685, 4883385, 5241085, 5624785, 6036485, 6478185, 6954885, 7471585, 8033285, 8644985, 9311685, 10038385, 10830085, 11691785, 12628485, 13645185, 14746885, 15938585, 17225285, 18611985, 20108685, 21725385, 23472085, 25358785]
    }

    if(rarity in petLevel):
        lvl = petLevel[rarity]
        for i in range(len(lvl)):
            if lvl[i] > int(petXp):
                return(i - 1)
        return(len(lvl) - 1)
    return 0


def getHotbarItems(inv):
    items = []

    counter = 0
    for tag in inv['i'].tags:
        if(tag.tag_info()[15] != '0'):
            extraStat = ''

            id = tag['tag']['ExtraAttributes']['id'].tag_info()[18:].strip()
            if(id == 'MIDAS_STAFF' or id == 'MIDAS_SWORD'):
                pricePaid = int(tag['tag']['ExtraAttributes']
                                ['winning_bid'].tag_info()[24:])
                extraStat = ' ( ${num:,} )'.format(num=pricePaid)

            name = removeColorCode(tag['tag']['display']['Name'])
            name += extraStat
            items.append(name)

        counter += 1
        if(counter == 8):
            break

    return items


talisman_data = getTalismansData()


def getTalismanPrice(itemID):
    if(talisman_data['success'] == False):
        return talisman_data

    talismansData = talisman_data['data']['talismans'].copy()

    if(itemID not in talismansData):
        return {
            'success': False,
            'cause': 'No ' + itemID + ' data.'
        }

    currentTalisman = talismansData[itemID]
    if(currentTalisman == None):
        return {
            'success': False,
            'cause': 'No ' + itemID + ' data.'
        }

    if('acquire_methods' not in currentTalisman):
        return {
            'success': False,
            'cause': 'No ' + itemID + ' data.'
        }

    methods = currentTalisman['acquire_methods']
    lowestBINItems = hypixelAPI.getLowestBINItems()
    if(lowestBINItems['success'] == False):
        return lowestBINItems
    bazaarProducts = hypixelAPI.getBazaarProducts()
    if(bazaarProducts['success'] == False):
        return bazaarProducts

    itemName = itemID
    if('name' in currentTalisman):
        itemName = currentTalisman['name']

    calculatedMethods = []
    for m in methods:
        if(m['type'] == 'ah'):
            if (itemID in lowestBINItems['data']):
                calculatedMethods.append({
                    'type': 'AH',
                    'name': itemName,
                    'total_price': lowestBINItems['data'][itemID]
                })
            continue
        if(m['type'] == 'npc'):
            calculatedMethods.append({
                'type': 'npc',
                'name': itemName,
                'npc': m['npc'],
                'wiki': m['wiki'],
                'total_price': m['price']
            })
            continue
        if(m['type'] == 'craft' or m['type'] == 'forge' or m['type'] == 'npc_trade'):
            items = []
            requiredItems = []
            for i in m['recipe']:
                itemPrice = 0
                if(i['type'] == 'bz'):
                    if(i['name'] in bazaarProducts['products']):
                        itemPrice = bazaarProducts['products'][i['name']
                                                               ]['quick_status']['buyPrice']
                elif(i['type'] == 'ah'):
                    if(i['name'] in lowestBINItems['data']):
                        itemPrice = lowestBINItems['data'][i['name']]
                elif(i['type'] == 'talisman'):
                    requiredItems.append(i['name'])

                items.append({
                    'name': i['name'],
                    'amount': i['amount'],
                    'total_price': itemPrice * i['amount']
                })

            type = 'Crafting'
            if(m['type'] == 'forge'):
                type = 'Forging'

            currMethod = {
                'type': type,
                'name': itemName,
                'items': items,
                'required_items': requiredItems,
                'total_price': sum([i['total_price'] for i in items])
            }

            if(m['type'] == 'npc_trade'):
                currMethod['type'] = 'npc trading'
                currMethod['npc'] = m['npc']
                if('wiki' in m):
                    currMethod['wiki'] = m['wiki']

            calculatedMethods.append(currMethod)
            continue
        if(m['type'] == 'quest'):
            calculatedMethods.append({
                'type': 'Quest',
                'name': itemName,
                'description': m['description'],
                'wiki': m['wiki'],
                'total_price': 0
            })
        else:
            return {
                'success': False,
                'cause': 'Unsupported acquiring method, ' + m['type']
            }

    bestMethods = min(calculatedMethods, key=lambda x: x['total_price'])

    return {
        'success': True,
        'data': bestMethods
    }
