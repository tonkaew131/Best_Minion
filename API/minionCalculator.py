import minion2JSON
import hypixelAPI
import requests
import time


def getMinionsData():
    try:
        r = requests.get(
            'https://raw.githubusercontent.com/tonkaew131/Best_Minion/master/resources/minion_data.json')
        return(r.json())
    except:
        return(minion2JSON.openJSONFile('./resources/minion_data_2.json'))


def getItemCompactorData():
    try:
        r = requests.get(
            'https://raw.githubusercontent.com/tonkaew131/Best_Minion/master/resources/item_data_comp.json')
        return(r.json())
    except:
        return(minion2JSON.openJSONFile('./resources/item_data_comp.json'))


def getItemSuperCompactor3000Data():
    try:
        r = requests.get(
            'https://raw.githubusercontent.com/tonkaew131/Best_Minion/master/resources/item_data_sc3000.json')
        return(r.json())
    except:
        return(minion2JSON.openJSONFile('./resources/item_data_sc3000.json'))


def getMinionsResources():
    return(minion2JSON.openJSONFile('./resources/minion_resource.json'))


minionData = getMinionsData()
itemCompactorData = getItemCompactorData()
itemSuperCompactor3000Data = getItemSuperCompactor3000Data()
minionsResource = getMinionsResources()


def getEnchantedItem(ratio, item, upgrade1, upgrade2, sum):
    """Return most enchanted form of item\n
    Return ratio, newItemName
    """
    newItem = ''
    if(upgrade1 == 'Compactor' or upgrade2 == 'Compactor'):
        if(item in itemCompactorData['items']):
            newItem = itemCompactorData['items'][item]['to']
            ratio *= int(itemCompactorData['items'][item]['count'])
            sum += int(itemCompactorData['items'][item]['count'])
    if(upgrade1 == 'Super Compactor 3000' or upgrade2 == 'Super Compactor 3000'):
        if(item in itemSuperCompactor3000Data['items']):
            newItem = itemSuperCompactor3000Data['items'][item]['to']
            ratio *= int(itemSuperCompactor3000Data['items'][item]['count'])
            sum += int(itemSuperCompactor3000Data['items'][item]['count'])

    if(newItem == ''):
        return 1 / ratio, item, sum
    return getEnchantedItem(ratio, newItem, upgrade1, upgrade2, sum)


def calculateTop10(options):
    """Calculate top10 minion return in JSON\n
    Options = {
        'minion_tier', '?bazaar_products', '?price_type'
    }\n
    - minion_tier is 1-12 or 'ALL'
    - bazaar_products is optional\n
    - price_type are 'NPC', 'BZ', 'ALL' (optional, default 'ALL')
    """

    priceType = 'ALL'
    if('price_type' in options):
        priceType = options['price_type']
    if(priceType.lower() == 'bazaar'):
        priceType = 'BZ'
    elif(priceType.lower() == 'all'):
        priceType = 'ALL'

    bazaarProducts = {}
    if('bazaar_products' not in options):
        bazaarProducts = hypixelAPI.getBazaarProducts()
    else:
        bazaarProducts = options['bazaar_products']
    if(bazaarProducts['success'] == False):
        return({
            'success': False,
            'cause': bazaarProducts['cause']
        })

    earningData = []
    if(options['minion_tier'].isnumeric()):
        minionTier = int(options['minion_tier'])
        if(not (1 <= minionTier <= 12)):
            return({'success': False, 'cause': 'Minion tier must be between 1 and 12 or ALL'})

        for m in minionData['minions']:
            minionTier = str(minionTier)
            if(minionTier not in m['tier']):
                continue

            options = {
                'minion_name': m['name'],
                'minion_tier': minionTier,
                'minion_slot': 1,
                'minion_upgrade1': 'Super Compactor 3000',
                'minion_upgrade2': 'Diamond Spreading',
                'minion_fuel': 'None',
                'minion_storage': 'None',
                'is_afk': False,
                'minion_bonus1': 'None',
                'minion_bonus2': 'None',
                'minion_bonus3': 'None',
                'bazaar_products': bazaarProducts,
                'price_type': priceType
            }

            currentData = calculateMinion(options)
            if(currentData['success'] == False):
                return(currentData)

            currentData = currentData['data']
            earningData.append({
                'name': currentData['name'],
                'tier': minionTier,
                'earning_per_hour': currentData['earnings']['per_hour']
            })
    else:
        if(options['minion_tier'].lower() != 'all'):
            return({'success': False, 'cause': 'Minion tier must be between 1 and 12 or ALL'})

        for m in minionData['minions']:
            for t in m['tier']:
                options = {
                    'minion_name': m['name'],
                    'minion_tier': t,
                    'minion_slot': 1,
                    'minion_upgrade1': 'Super Compactor 3000',
                    'minion_upgrade2': 'Diamond Spreading',
                    'minion_fuel': 'None',
                    'minion_storage': 'None',
                    'is_afk': False,
                    'minion_bonus1': 'None',
                    'minion_bonus2': 'None',
                    'minion_bonus3': 'None',
                    'bazaar_products': bazaarProducts,
                    'price_type': priceType,
                    'inferno_fuel': 'None'
                }

                currentData = calculateMinion(options)
                if(currentData['success'] == False):
                    return(currentData)

                currentData = currentData['data']
                earningData.append({
                    'name': currentData['name'],
                    'tier': t,
                    'earning_per_hour': currentData['earnings']['per_hour']
                })

    earningData = sorted(earningData, key=lambda k: k.get('earning_per_hour', 0), reverse=True)

    formatedEarningData, counter = [], 0
    sameMinions, sameMinionEarning, sameMinionName = [], 0, ''
    for m in earningData:
        if(counter == (20 - len(sameMinions))):
            break

        if(len(sameMinions) == 0):
            sameMinions.append(m)
            sameMinionEarning = m['earning_per_hour']
            sameMinionName = m['name']
            continue

        if(sameMinionName == m['name'] and sameMinionEarning == m['earning_per_hour']):
            sameMinions.append(m)
            continue

        if(sameMinionName != m['name'] or (sameMinionName == m['name'] and sameMinionEarning != m['earning_per_hour'])):
            counter += 1
            tier = []
            for i in sameMinions:
                tier.append(int(i['tier']))

            tier = [str(n) for n in sorted(tier)]
            formatedEarningData.append({
                'formatted_name': sameMinionName + ' ' + ' & '.join(tier),
                'name': sameMinionName,
                'tier': tier,
                'earning_per_hour': sameMinionEarning
            })

            sameMinions = [m]
            sameMinionEarning = m['earning_per_hour']
            sameMinionName = m['name']
            continue

    if(len(sameMinions) != 0):
        tier = []
        for i in sameMinions:
            tier.append(int(i['tier']))

        tier = [str(n) for n in sorted(tier)]
        formatedEarningData.append({
            'formatted_name': sameMinionName + ' ' + ' & '.join(tier),
            'name': sameMinionName,
            'tier': tier,
            'earning_per_hour': sameMinionEarning
        })

    timestamp = 0
    if('lastUpdated' in bazaarProducts):
        timestamp = bazaarProducts['lastUpdated']
    else:
        timestamp = int(time.time() * 1000)

    return({
        'success': True,
        'data': formatedEarningData,
        'timestamp': timestamp
    })


def calculateMinion(options):
    """Calculate minion earning return in JSON\n
    Options = {
        'minion_name', 'minion_tier', 'minion_slot', 'minion_upgrade1', 
        'minion_upgrade2', 'minion_fuel', 'minion_storage', 'is_afk', 
        'minion_bonus1', 'minion_bonus2', 'minion_bonus3', '?bazaar_products',
        '?price_type', '?inferno_fuel'
    }\n
    - bazaar_products is optional\n
    - price_type are 'NPC', 'BZ', 'ALL' (optional, default 'ALL')
    """
    _minionData = {}

    if(isinstance(options['minion_tier'], int)):
        options['minion_tier'] = str(options['minion_tier'])

    minionName = (options['minion_name'].lower()).replace(' minion', '')
    minionName = minionName.strip().title() + ' Minion'

    _minionData = getMinionData(minionName)
    if(len(_minionData) == 0):
        return({
            'success': False,
            'cause': minionName + ' doesn\'t exist yet, maybe later.'
        })

    if(options['minion_tier'] not in _minionData['tier']):
        return({
            'success': False,
            'cause': 'Tier ' + options['minion_tier'] + ' for the ' + minionName + ' doesn\'t exist yet, maybe later.'
        })

    totalBuff = 0

    upgrade1 = options['minion_upgrade1']
    upgrade2 = options['minion_upgrade2']
    # Upgrade Buff
    upgradeSpeedBuff = getUpgradeSpeedBuff(upgrade1, upgrade2, options['minion_fuel'])
    totalBuff += upgradeSpeedBuff

    # Inferno Fuel
    infernoFuel = 'None'
    if('inferno_fuel' in options):
        infernoFuel = options['inferno_fuel']

    # Fuel
    fuelSpeed, fuelDuration, itemMultiplier = getFuelSpeedAndDuration(options['minion_fuel'])
    if(minionName != 'Inferno Minion'):
        # if not Inferno Minion, calculate everytime!
        totalBuff += fuelSpeed
    elif((minionName == 'Inferno Minion') and (not isInfernoFuel(infernoFuel))):
        # if Inferno Minion, but doesn't have Inferno Fuel. Also calculate!
        totalBuff += fuelSpeed

    # Crystal
    crystalSpeed, crystalType = getCrystalSpeed(options['minion_bonus1'])
    if(crystalType == _minionData['type']):
        totalBuff += crystalSpeed

    # Beacon
    beaconBuffSpeed = getBeaconBuffSpeed(options['minion_bonus2'])
    totalBuff += beaconBuffSpeed

    # Pet
    petBuffSpeed, petType, petMinions = getPetBuffSpeed(options['minion_bonus3'])
    if(petType == _minionData['type']):
        totalBuff += petBuffSpeed
    elif(_minionData['name'] in petMinions):
        totalBuff += petBuffSpeed

    # Soulflow Engine
    _isLesserSoulflowEngine = isLesserSoulflowEngine(upgrade1, upgrade2)
    _isSoulFlowEngine = isSoulFlowEngine(upgrade1, upgrade2)
    if(_isSoulFlowEngine and minionName == 'Voidling Minion'):
        totalBuff += 0.03 * int(options['minion_tier'])

    isApexMinion = False
    if(minionName == 'Inferno Minion'):
        # - Rising Celsius
        # Each Inferno minion increases the speed of all Inferno minions by 6%.
        totalBuff += 0.06 * int(options['minion_slot'])
        
        if(int(options['minion_tier']) >= 10):
            isApexMinion = True

    minionTimeBetweenAction = _minionData['tier'][options['minion_tier']]['times_between_action']
    minionSpeed = minionTimeBetweenAction * (1 - (totalBuff / (1 + totalBuff)))

    priceType = 'ALL'
    lowestBINItems = {}
    isAHavailable = False
    if('price_type' in options):
        priceType = options['price_type']
    if(priceType.lower() == 'bazaar'):
        lowestBINItems = hypixelAPI.getLowestBINItems()
        if(lowestBINItems['success'] == True):
            isAHavailable = True

        priceType = 'BZ'
    elif(priceType.lower() == 'all'):
        lowestBINItems = hypixelAPI.getLowestBINItems()
        if(lowestBINItems['success'] == True):
            isAHavailable = True

        priceType = 'ALL'

    bazaarProducts = {}
    if('bazaar_products' not in options):
        bazaarProducts = hypixelAPI.getBazaarProducts()
        if(bazaarProducts['success'] == False):
            return({
                'success': False,
                'cause': bazaarProducts['cause'],
            })
    else:
        bazaarProducts = options['bazaar_products']

    totalExpPerHour = {
        'FORAGING': 0, 
        'FISHING': 0, 
        'ALCHEMY': 0,
        'FARMING': 0, 
        'MINING': 0, 
        'ENCHANTING': 0, 
        'COMBAT': 0
    }

    items = []
    totalItemCount = 0
    totalEarning = 0
    actions = getMinionActions(_minionData['name'], options['is_afk'])

    compactRatio = []
    for item in _minionData['items']:
        itemCount = item['amount_per_actions']  # number of items per n actions
        itemName = item['name']

        ratio, itemName, ratioSum = getEnchantedItem(1, itemName, upgrade1, upgrade2, 0)
        itemNPCPrice = item['npc_price'] * (1 / ratio)

        itemType = ''
        itemPrice = 0
        if(priceType == 'NPC'):
            itemType = 'NPC'
            itemPrice = itemNPCPrice
        elif(priceType == 'BZ'):
            if(itemName in bazaarProducts['products']):
                itemType = 'Bazaar'
                itemPrice = bazaarProducts['products'][itemName]['quick_status']['sellPrice']
            elif(isAHavailable and itemName in lowestBINItems['data']):
                itemType = 'AH'
                itemPrice = lowestBINItems['data'][itemName]
            else:
                itemType = 'NPC'
                itemPrice = itemNPCPrice
        elif(priceType == 'ALL'):
            if(itemName in bazaarProducts['products']):
                itemBazaar = bazaarProducts['products'][itemName]
                if(itemNPCPrice >= itemBazaar['quick_status']['sellPrice']):
                    itemType = 'NPC'
                    itemPrice = itemNPCPrice
                else:
                    itemType = 'Bazaar'
                    itemPrice = itemBazaar['quick_status']['sellPrice']
            elif(isAHavailable and itemName in lowestBINItems['data']):
                itemType = 'AH'
                itemPrice = lowestBINItems['data'][itemName]
            else:
                itemType = 'NPC'
                itemPrice = itemNPCPrice

        if(_isLesserSoulflowEngine or _isSoulFlowEngine):
            itemMultiplier /= 2

        itemsPerSecond = itemMultiplier * options['minion_slot'] * (
            (itemCount) / (minionSpeed * getMinionActions(minionName, options['is_afk'])))
        itemsPerHour = itemsPerSecond * 3600
        earningPerHour = ratio * itemsPerHour * itemPrice

        totalItemCount += itemsPerHour
        totalEarning += earningPerHour

        compactRatio.append({
            'item_name': itemName,
            'slot_needed': ratioSum,
            'items_per_hour': itemsPerHour * ratio
        })

        expType = item['exp_per_item']['type']
        expPerHour = itemsPerHour * item['exp_per_item']['amount']
        if(expType != ''):
            totalExpPerHour[expType] += expPerHour

        itemsPerHour *= ratio
        itemName = itemName.replace('_', ' ').title()
        items.append({
            'item_name': itemName,
            'items_per_hour': itemsPerHour,
            'price_per_item': itemPrice,
            'earning_per_hour': earningPerHour,
            'sell_to': itemType,
            'exp': {
                'type': expType,
                'per_hour': expPerHour,
                'per_day': expPerHour * 24,
                'per_week': expPerHour * 24 * 7
            }
        })

    diamondsPerHour = totalItemCount / 10
    diamondsPrice = 0
    diamondsType = ''
    diamondsEarningPerHour = 0
    _isDiamondSpreading = isDiamondSpreading(
        options['minion_upgrade1'], options['minion_upgrade2'])
    if(_isDiamondSpreading):
        itemName = 'DIAMOND'
        ratio, itemName, ratioSum = getEnchantedItem(
            1, itemName, options['minion_upgrade1'], options['minion_upgrade2'], 0)

        if(itemName not in bazaarProducts['products'] or priceType == 'NPC'):
            diamondsPrice = 8 * (1 / ratio)
            diamondsEarningPerHour = ratio * diamondsPerHour * diamondsPrice
            diamondsType = 'NPC'
        elif(priceType == 'BZ'):
            diamondsPrice = bazaarProducts['products'][itemName]['quick_status']['sellPrice']
            diamondsEarningPerHour = ratio * diamondsPerHour * diamondsPrice
            diamondsType = 'Bazaar'
        elif(priceType == 'ALL'):
            if(bazaarProducts['products'][itemName]['quick_status']['sellPrice'] > 8 * (1 / ratio)):
                diamondsPrice = bazaarProducts['products'][itemName]['quick_status']['sellPrice']
                diamondsEarningPerHour = ratio * diamondsPerHour * diamondsPrice
                diamondsType = 'Bazaar'
            else:
                diamondsPrice = 8 * (1 / ratio)
                diamondsEarningPerHour = ratio * diamondsPerHour * diamondsPrice
                diamondsType = 'NPC'

        diamondExpPerHour = diamondsPerHour * 0.4
        totalExpPerHour['MINING'] += diamondExpPerHour

        totalEarning += diamondsEarningPerHour
        isDiamondDropped = False
        for i in items:
            if(i['item_name'] == itemName.replace('_', ' ').title()):
                for j in compactRatio:
                    if j['item_name'] == itemName:
                        j['items_per_hour'] += ratio * diamondsPerHour

                isDiamondDropped = True
                i['items_per_hour'] += ratio * diamondsPerHour
                i['price_per_item'] += diamondsEarningPerHour

                i['exp']['per_hour'] += diamondExpPerHour
                i['exp']['per_day'] += diamondExpPerHour * 24
                i['exp']['per_week'] += diamondExpPerHour * 24 * 7
                break
        if(not isDiamondDropped):
            compactRatio.append({
                'item_name': itemName,
                'slot_needed': ratioSum,
                'items_per_hour': ratio * diamondsPerHour
            })
            items.append({
                'item_name': itemName.replace('_', ' ').title(),
                'items_per_hour': ratio * diamondsPerHour,
                'price_per_item': diamondsPrice,
                'earning_per_hour': diamondsEarningPerHour,
                'sell_to': diamondsType,
                'exp': {
                    'type': 'MINING',
                    'per_hour': diamondExpPerHour,
                    'per_day': diamondExpPerHour * 24,
                    'per_week': diamondExpPerHour * 24 * 7
                }
            })

    potatoesPerHour = totalItemCount / 10
    potatoesPrice = 0
    potatoesType = ''
    potatoesEarningPerHour = 0
    _isPotatoSpreading = isPotatoSpreading(
        options['minion_upgrade1'], options['minion_upgrade2'])
    if(_isPotatoSpreading):
        itemName = 'POTATO_ITEM'
        ratio, itemName, ratioSum = getEnchantedItem(
            1, itemName, options['minion_upgrade1'], options['minion_upgrade2'], 0)

        if(priceType == 'NPC'):
            potatoesPrice = 1 * (1 / ratio)
            potatoesEarningPerHour = ratio * potatoesPerHour * potatoesPrice
            potatoesType = 'NPC'
        elif(priceType == 'BZ'):
            potatoesPrice = bazaarProducts['products'][itemName]['quick_status']['sellPrice']
            potatoesEarningPerHour = ratio * potatoesPerHour * potatoesPrice
            potatoesType = 'Bazaar'
        elif(priceType == 'ALL'):
            if(bazaarProducts['products'][itemName]['quick_status']['sellPrice'] > 1 * (1 / ratio)):
                potatoesPrice = bazaarProducts['products'][itemName]['quick_status']['sellPrice']
                potatoesEarningPerHour = ratio * potatoesPerHour * potatoesPrice
                potatoesType = 'Bazaar'
            else:
                potatoesPrice = 8 * (1 / ratio)
                potatoesEarningPerHour = ratio * potatoesPerHour * potatoesPrice
                potatoesType = 'NPC'

        potatoesExpPerHour = potatoesPerHour * 0.1
        totalExpPerHour['FARMING'] += potatoesExpPerHour

        totalEarning += potatoesEarningPerHour
        isPotatoesDropped = False
        for i in items:
            if(i['item_name'] == itemName.replace('_', ' ').title()):
                for j in compactRatio:
                    if j['item_name'] == itemName:
                        j['items_per_hour'] += ratio * potatoesPerHour

                isPotatoesDropped = True
                i['items_per_hour'] += ratio * potatoesPerHour
                i['price_per_item'] += potatoesEarningPerHour

                i['exp']['per_hour'] += potatoesExpPerHour
                i['exp']['per_day'] += potatoesExpPerHour * 24
                i['exp']['per_week'] += potatoesExpPerHour * 24 * 7
                break
        if(not isPotatoesDropped):
            compactRatio.append({
                'item_name': itemName,
                'slot_needed': ratioSum,
                'items_per_hour': ratio * potatoesPerHour
            })
            items.append({
                'item_name': itemName.replace('_', ' ').title(),
                'items_per_hour': ratio * potatoesPerHour,
                'price_per_item': potatoesPrice,
                'earning_per_hour': potatoesEarningPerHour,
                'sell_to': potatoesType,
                'exp': {
                    'type': 'FARMING',
                    'per_hour': potatoesExpPerHour,
                    'per_day': potatoesExpPerHour * 24,
                    'per_week': potatoesExpPerHour * 24 * 7
                }
            })

    # KrampusHelmet
    redGiftsPerHour = totalItemCount / 25000
    redGiftsPrice = 0
    redGiftsType = ''
    redGiftsEarningPerHour = 0
    _isKrampusHelmet = isKrampusHelmet(
        options['minion_upgrade1'], options['minion_upgrade2'])
    if(_isKrampusHelmet):
        if(priceType == 'NPC'):
            redGiftsPrice = 0
            redGiftsEarningPerHour = redGiftsPerHour * redGiftsPrice
            redGiftsType = 'NPC'
        elif(priceType == 'BZ' or priceType == 'ALL'):
            redGiftsPrice = bazaarProducts['products']['RED_GIFT']['quick_status']['sellPrice']
            redGiftsEarningPerHour = redGiftsPerHour * redGiftsPrice
            redGiftsType = 'Bazaar'

        totalEarning += redGiftsEarningPerHour
        items.append({
            'item_name': 'Red Gift',
            'items_per_hour': redGiftsPerHour,
            'price_per_item': redGiftsPrice,
            'earning_per_hour': redGiftsEarningPerHour,
            'sell_to': redGiftsType,
            'exp': {
                'type': '',
                'per_hour': 0.0,
                'per_day': 0.0,
                'per_week': 0.0
            }
        })

    # Inferno Minion Fuel
    if(minionName == 'Inferno Minion' and isInfernoFuel(infernoFuel)):
        # Deduce old items count to 1/5
        for item in items:
            item['items_per_hour'] /= 5
            item['earning_per_hour'] /= 5

            item['exp']['per_hour'] /= 5
            item['exp']['per_day'] /= 5
            item['exp']['per_week'] /= 5

        # Add special Items to 4/5 * totalItemCount
        specialItemMultiplier = 1
        if('Rare' in infernoFuel):
            specialItemMultiplier = 10
        elif('Epic' in infernoFuel):
            specialItemMultiplier = 15
        elif('Legend' in infernoFuel):
            specialItemMultiplier = 20

        # Get Special Item type & amount
        itemType = ''
        itemAmount = 0
        itemNpcPrice = 0
        expType = ''
        expAmount = 0
        if('Magma Cream' in infernoFuel):
            itemType = 'MAGMA_CREAM'
            itemAmount = 2 * specialItemMultiplier
            itemNpcPrice = 8

            expType = 'COMBAT'
            expAmount = 0.2
        if('Glowstone Dust' in infernoFuel):
            itemType = 'GLOWSTONE_DUST'
            itemAmount = 2.5 * specialItemMultiplier
            itemNpcPrice = 2
            
            expType = 'MINING'
            expAmount = 0.2
        if('Nether Wart' in infernoFuel):
            itemType = 'NETHER_STALK'
            itemAmount = 5 * specialItemMultiplier
            itemNpcPrice = 3
            
            expType = 'ALCHEMY'
            expAmount = 0.2
        if('Blaze Rod' in infernoFuel):
            itemType = 'BLAZE_ROD'
            itemAmount = 1 * specialItemMultiplier
            itemNpcPrice = 9
            
            expType = 'COMBAT'
            expAmount = 0.3
        if('Crude Gabagool' in infernoFuel):
            itemType = 'CRUDE_GABAGOOL'
            itemAmount = 1 * specialItemMultiplier
            itemNpcPrice = 1
            
            expType = ''
            expAmount = 0

        # Compact item down
        ratio, itemType, ratioSum = getEnchantedItem(1, itemType, upgrade1, upgrade2, 0)
        itemNpcPrice = itemNpcPrice * (1 / ratio)

        # Get its price
        itemPricePer = 0
        itemSellTo = ''
        if(priceType == 'NPC'):
            itemPricePer = itemNpcPrice
            itemSellTo = 'NPC'
        elif(priceType == 'BZ'):
            if(itemType in bazaarProducts['products']):
                itemSellTo = 'Bazaar'
                itemPricePer = bazaarProducts['products'][itemType]['quick_status']['sellPrice']
            else:
                itemSellTo = 'NPC'
                itemPricePer = itemNpcPrice
        elif(priceType == 'ALL'):
            if(itemType in bazaarProducts['products']):
                itemBazaar = bazaarProducts['products'][itemType]
                if(itemNpcPrice >= itemBazaar['quick_status']['sellPrice']):
                    itemSellTo = 'NPC'
                    itemPricePer = itemNpcPrice
                else:
                    itemSellTo = 'Bazaar'
                    itemPricePer = itemBazaar['quick_status']['sellPrice']
            else:
                itemSellTo = 'NPC'
                itemPricePer = itemNpcPrice

        # itemsPerSecond = 4 / 5 * options['minion_slot'] * itemAmount * totalItemCount
        itemsPerSecond = 4 / 5 * options['minion_slot'] * ((itemAmount) / (minionSpeed * getMinionActions(minionName, options['is_afk'])))
        
        itemsPerHour = itemsPerSecond * 3600
        earningPerHour = ratio * itemsPerHour * itemPricePer

        # totalItemCount += itemsPerHour
        totalEarning += earningPerHour

        compactRatio.append({
            'item_name': itemType,
            'slot_needed': ratioSum,
            'items_per_hour': itemsPerHour * ratio
        })

        expPerHour = itemsPerHour * expAmount
        if(expType != ''):
            totalExpPerHour[expType] += expPerHour

        itemsPerHour *= ratio
        itemType = itemType.replace('_', ' ').title()

        items.append({
            'item_name': itemType,
            'items_per_hour': itemsPerHour,
            'price_per_item': itemPrice,
            'earning_per_hour': earningPerHour,
            'sell_to': itemSellTo,
            'exp': {
                'type': expType,
                'per_hour': expPerHour,
                'per_day': expPerHour * 24,
                'per_week': expPerHour * 24 * 7
            }
        })

        # Hypergolic Inferno Minion Fuel
        if('Legend' in infernoFuel):
            infernoVertexPerHour = 1 / 18000 * itemsPerHour
            if(priceType == 'BZ' or priceType == 'ALL'):
                if('INFERNO_VERTEX' in bazaarProducts['products']):
                    itemSellTo = 'Bazaar'
                    itemPricePer = bazaarProducts['products']['INFERNO_VERTEX']['quick_status']['sellPrice']
            else:
                itemSellTo = 'NPC'
                itemPricePer = 0

            items.append({
                'item_name': 'Inferno Vertex',
                'items_per_hour': infernoVertexPerHour,
                'price_per_item': itemPricePer,
                'earning_per_hour': infernoVertexPerHour * itemPricePer,
                'sell_to': itemSellTo,
                'exp': {
                    'type': '',
                    'per_hour': 0,
                    'per_day': 0,
                    'per_week': 0
                }
            })

            infernoApexPerHour = 1 / 1728000 * itemsPerHour
            if(priceType == 'BZ' or priceType == 'ALL'):
                if('INFERNO_APEX' in bazaarProducts['products']):
                    itemSellTo = 'Bazaar'
                    itemPricePer = bazaarProducts['products']['INFERNO_APEX']['quick_status']['sellPrice']
            else:
                itemSellTo = 'NPC'
                itemPricePer = 0

            items.append({
                'item_name': 'Inferno Apex',
                'items_per_hour': infernoApexPerHour,
                'price_per_item': itemPricePer,
                'earning_per_hour': infernoApexPerHour * itemPricePer,
                'sell_to': itemSellTo,
                'exp': {
                    'type': '',
                    'per_hour': 0,
                    'per_day': 0,
                    'per_week': 0
                }
            })

            reaperPepperPerHour = 1 / 504000 * itemsPerHour
            if(priceType == 'BZ' or priceType == 'ALL'):
                if('REAPER_PEPPER' in bazaarProducts['products']):
                    itemSellTo = 'Bazaar'
                    itemPricePer = bazaarProducts['products']['REAPER_PEPPER']['quick_status']['sellPrice']
            else:
                itemSellTo = 'NPC'
                itemPricePer = 0

            items.append({
                'item_name': 'Reaper Pepper',
                'items_per_hour': reaperPepperPerHour,
                'price_per_item': itemPricePer,
                'earning_per_hour': reaperPepperPerHour * itemPricePer,
                'sell_to': itemSellTo,
                'exp': {
                    'type': '',
                    'per_hour': 0,
                    'per_day': 0,
                    'per_week': 0
                }
            })

            gabagoolTheFishPerHour = 1 / 432000 * itemsPerHour
            if(priceType == 'BZ' or priceType == 'ALL'):
                if('GABAGOOL_THE_FISH' in bazaarProducts['products']):
                    itemSellTo = 'Bazaar'
                    itemPricePer = bazaarProducts['products']['GABAGOOL_THE_FISH']['quick_status']['sellPrice']
                elif(isAHavailable and 'GABAGOOL_THE_FISH' in lowestBINItems['data']):
                    itemType = 'AH'
                    itemPrice = lowestBINItems['data']['GABAGOOL_THE_FISH']
            else:
                itemSellTo = 'NPC'
                itemPricePer = 0

            items.append({
                'item_name': 'Gabagool The Fish',
                'items_per_hour': gabagoolTheFishPerHour,
                'price_per_item': itemPricePer,
                'earning_per_hour': gabagoolTheFishPerHour * itemPricePer,
                'sell_to': itemSellTo,
                'exp': {
                    'type': expType,
                    'per_hour': expPerHour,
                    'per_day': expPerHour * 24,
                    'per_week': expPerHour * 24 * 7
                }
            })

    sortedCompactRatio = sorted(compactRatio, key=lambda k: k['slot_needed'] / k['items_per_hour'])
    minionSlots = (_minionData['tier'][options['minion_tier']]['storage_slot'] / 64) + getStorageSlots(options['minion_storage'])
    timeUntilFull = ((minionSlots * 64) - sum(item['slot_needed'] for item in sortedCompactRatio)) / (sum(item['items_per_hour'] for item in sortedCompactRatio))

    # Soulflow Engine
    lesserPerHour = 20 * options['minion_slot']  # 1 every 180 seconds
    lesserPrice = 0
    lesserEarningPerHour = 0
    lesserType = ''
    if(_isLesserSoulflowEngine or _isSoulFlowEngine):
        if(priceType == 'NPC'):
            lesserPrice = 0
            lesserEarningPerHour = lesserPerHour * lesserPrice
            lesserType = 'NPC'
        elif(priceType == 'BZ' or priceType == 'ALL'):
            lesserPrice = bazaarProducts['products']['RAW_SOULFLOW']['quick_status']['sellPrice']
            lesserEarningPerHour = lesserPerHour * lesserPrice
            lesserType = 'Bazaar'

        totalEarning += lesserEarningPerHour
        items.append({
            'item_name': 'Raw Soulflow',
            'items_per_hour': lesserPerHour,
            'price_per_item': lesserPrice,
            'earning_per_hour': lesserEarningPerHour,
            'sell_to': lesserType,
            'exp': {
                'type': '',
                'per_hour': 0.0,
                'per_day': 0.0,
                'per_week': 0.0
            }
        })

    fuelDescription = 'None'
    if((not (fuelSpeed == 0 and fuelDuration == -1 and itemMultiplier == 1)) or (infernoFuel != 'None' and minionName == 'Inferno Minion')):
        if(infernoFuel != 'None' and minionName == 'Inferno Minion'):
            fuelId = 'INFERNO_'
            if('Rare' in infernoFuel):
                fuelId += 'FUEL_'
            elif('Epic' in infernoFuel):
                fuelId += 'HEAVY_'
            elif('Legend' in infernoFuel):
                fuelId += 'HYPERGOLIC_'
            if('Magma Cream' in infernoFuel):
                fuelId += 'MAGMA_CREAM'
            elif('Glowstone Dust') in infernoFuel:
                fuelId += 'GLOWSTONE_DUST'
            elif('Nether Wart' in infernoFuel):
                fuelId += 'NETHER_STALK'
            elif('Crude Gabagool' in infernoFuel):
                fuelId += 'CRUDE_GABAGOOL'

            fuelPrice = options['minion_slot'] * getFuelPrice(infernoFuel, bazaarProducts, lowestBINItems)
            fuelDuration = 24
        else:
            fuelPrice = options['minion_slot'] * getFuelPrice(options['minion_fuel'], bazaarProducts, lowestBINItems)

        if(fuelDuration == -1):  # infinite source
            FuelStartToProfit = fuelPrice / totalEarning
            fuelDescription = 'Profit in **' + str(round(FuelStartToProfit, 1)) + '** hours (One minion)'
        else:  # non infinite source
            fuelPricePerHour = fuelPrice / fuelDuration
            if(fuelPricePerHour > totalEarning):
                fuelDescription = 'Loss **-${:,.2f}** / hours (One minion)'.format(
                    fuelPricePerHour - totalEarning)
            else:
                fuelDescription = 'Profit **${:,.2f}** / hours (One minion)'.format(
                    totalEarning - fuelPricePerHour)

    timestamp = 0
    if('lastUpdated' in bazaarProducts and (priceType == 'ALL' or priceType == 'BZ')):
        timestamp = bazaarProducts['lastUpdated']
    else:
        timestamp = int(time.time() * 1000)

    pictures = {}
    if(minionName in minionsResource['minions']):
        pictures = minionsResource['minions'][minionName]
    else:
        pictures = minionsResource['minions']['Wheat Minion']

    expKey = {}
    for key in totalExpPerHour:
        if(totalExpPerHour[key] == 0):
            continue
        exp = {
            'per_hour': totalExpPerHour[key],
            'per_day': totalExpPerHour[key] * 24,
            'per_week': totalExpPerHour[key] * 24 * 7
        }
        expKey[key] = exp

    minionPrice = calculateMinionPrice(_minionData, options['minion_slot'], options['minion_tier'], bazaarProducts)
    if(minionPrice['success'] == False):
        return(minionPrice)

    fuelName = options['minion_fuel']
    if(minionName == 'Inferno Minion' and infernoFuel != 'None'):
        fuelName = infernoFuel
    return({
        'success': True,
        'data': {
            'pictures': pictures,
            'name': minionName,
            'time_between_action': {
                'before': minionTimeBetweenAction,
                'after': minionSpeed
            },
            'earnings': {
                'per_hour': totalEarning,
                'per_day': totalEarning * 24,
                'per_week': totalEarning * 24 * 7
            },
            'fuel': {
                'name': fuelName,
                'description': fuelDescription
            },
            'storage': {
                'hour_until_full': timeUntilFull,
                'slots': minionSlots,
                'type': options['minion_storage']
            },
            'price': minionPrice['data'],
            'items': items,
            'exp': expKey,
            'timestamp': timestamp
        }
    })


def calculateMinionPrice(currentMinionData, amount, tier, bazaarProducts):
    """
    minionData from resources/minion_data_2\n
    amount is number of minions
    """
    if(bazaarProducts['success'] == False):
        return(bazaarProducts)

    if(tier not in currentMinionData['tier']):
        return({
            'success': False,
            'cause': 'Can\'t find ' + currentMinionData['name']
        })

    itemsLastTier = []
    totalLastTier = 0
    itemsTotalTier = {}
    totalTotalTier = 0
    for i in range(1, int(tier) + 1):
        for item in currentMinionData['tier'][str(i)]['upgrade_items']:
            itemPrice = 0
            itemsRequire = []
            if('_MINION_' in item['name']):
                minionName = ' '.join(item['name'].split('_')[
                                      :-2]).title() + ' Minion'
                minionTier = item['name'].split('_')[-1]
                _minionData = {}

                _minionData = getMinionData(minionName)
                if(len(_minionData) == 0):
                    return({'success': False, 'cause': 'Can\'t find ' + minionName + ' ' + minionTier})

                if(minionTier not in _minionData['tier']):
                    return({'success': False, 'cause': 'Can\'t find ' + minionName + ' ' + minionTier})

                minionPrice = calculateMinionPrice(_minionData, item['amount'] * amount, minionTier, bazaarProducts)
                if(minionPrice['success'] == False):
                    return(minionPrice)

                itemPrice = minionPrice['data']['all_tier']['total']
                itemsRequire = minionPrice['data']['all_tier']['items']
            elif(item['name'] == 'COINS'):
                itemPrice = item['amount'] * amount
            elif(item['name'] in bazaarProducts['products']):
                itemPrice = item['amount'] * amount * bazaarProducts['products'][item['name']]['quick_status']['buyPrice']

            if(i == int(tier)):
                itemsLastTier.append({
                    'name': item['name'].replace('_', ' ').title(),
                    'amount': item['amount'] * amount,
                    'price': itemPrice,
                    'items': itemsRequire
                })
                totalLastTier += itemPrice

            totalTotalTier += itemPrice
            if(item['name'] not in itemsTotalTier):
                itemsTotalTier[item['name']] = {
                    'name': item['name'],
                    'amount': item['amount'] * amount,
                    'price': itemPrice,
                    'items': itemsRequire
                }
                continue

            itemsTotalTier[item['name']]['name'] = item['name']
            itemsTotalTier[item['name']]['amount'] += item['amount'] * amount
            itemsTotalTier[item['name']]['price'] += itemPrice
            if(len(itemsRequire) != 0):
                for i in itemsTotalTier[item['name']]['items']:
                    for j in itemsRequire:
                        if(i['name'] == j['name']):
                            i['amount'] += j['amount']
                            i['price'] += j['price']
                        continue
                continue
            itemsTotalTier[item['name']]['items'] = itemsRequire

    pictures = {}
    if(currentMinionData['name'] in minionsResource['minions']):
        pictures = minionsResource['minions'][currentMinionData['name']]
    else:
        pictures = minionsResource['minions']['Wheat Minion']

    return({
        'success': True,
        'data': {
            'pictures': pictures,
            'all_tier': {
                'total': totalTotalTier,
                'items': minion2JSON.jsonToArray(itemsTotalTier)
            },
            'last_tier': {
                'total': totalLastTier,
                'items': itemsLastTier
            }
        }
    })


def getMinionResource(minionName):
    if(minionName in minionsResource['minions']):
        return minionsResource['minions'][minionName]
    return


def getMinionData(minionName):
    _minionData = {}
    for m in minionData['minions']:
        if(m['name'] == minionName):
            _minionData = m
            break
    return _minionData


def getFuelPrice(fuelName, bazaarProducts, binProducts):
    if('data' in binProducts):
        if(fuelName in binProducts['data']):
            return(binProducts['data'][fuelName])

    fuelName = fuelName.upper().replace(' ', '_')
    if(fuelName in bazaarProducts['products']):
        return(bazaarProducts['products'][fuelName]['quick_status']['buyPrice'])

    if(fuelName == 'BLOCK_OF_COAL'):
        return(bazaarProducts['products']['COAL']['quick_status']['buyPrice'] * 9)
    return 0


def getUpgradeSpeedBuff(upgrade1, upgrade2, fuelName):
    """
    Return(speedBuff)
    """
    speedBuff = 0
    if(upgrade1 == 'Flycatcher' and fuelName != 'None'):
        speedBuff += 0.2
    if(upgrade2 == 'Flycatcher' and fuelName != 'None'):
        speedBuff += 0.2

    # if one of them is 'Minion Expander'
    if(upgrade1 == 'Minion Expander' or upgrade2 == 'Minion Expander'):
        # if both of them are 'Minion Expander'
        if(upgrade1 == 'Minion Expander' and upgrade2 == 'Minion Expander'):
            speedBuff += 0.1025
        else:
            speedBuff += 0.05

    return(speedBuff)


def getFuelSpeedAndDuration(fuelName):
    """Get fuel Speed and Duration(in hours) and item multiplier\n
    *if duration is infinite then it's -1\n
    Return(fuelSpeed, fuelDuration, itemMultiplier)
    """
    if(fuelName == 'None'):
        return(0, -1, 1)
    elif(fuelName == 'Coal'):
        return(0.05, 0.5, 1)
    elif(fuelName == 'Block of Coal'):
        return(0.05, 5, 1)
    elif(fuelName == 'Enchanted Bread'):
        return(0.05, 12, 1)
    elif(fuelName == 'Enchanted Coal'):
        return(0.1, 24, 1)
    elif(fuelName == 'Enchanted Charcoal'):
        return(0.2, 36, 1)
    elif(fuelName == 'Solar Panel'):
        # Only work during the day.
        return(0.25, -1, 1)
    elif(fuelName == 'Enchanted Lava Bucket'):
        return(0.25, -1, 1)
    elif(fuelName == 'Magma Bucket'):
        return(0.3, -1, 1)
    elif(fuelName == 'Plasma Bucket'):
        return(0.35, -1, 1)
    elif(fuelName == 'Hamster Wheel'):
        return(0.5, 24, 1)
    elif(fuelName == 'Foul Flesh'):
        return(0.9, 5, 1)
    elif(fuelName == 'Catalyst'):
        return(0, 3, 3)
    elif(fuelName == 'Hyper Catalyst'):
        return(0, 6, 4)
    else:
        return(0, -1, 1)


def getCrystalSpeed(crystalName):
    """
    minionType = ['FARMING', 'MINING', 'FORAGING']\n
    Return(crystalSpeed, minionType)
    """
    if(crystalName == 'None'):
        return(0, '')
    elif(crystalName == 'Farm Crystal'):
        return(0.1, 'FARMING')
    elif(crystalName == 'Mithril Crystal'):
        return(0.1, 'MINING')
    elif(crystalName == 'Woodcutting Crystal'):
        return(0.1, 'FORAGING')
    else:
        return(0, '')


def getBeaconBuffSpeed(beaconName):
    """
    Return(beaconBuffSpeed)
    """
    if(beaconName == 'None'):
        return(0)
    elif(beaconName == 'Beacon I'):
        return(0.02)
    elif(beaconName == 'Beacon II'):
        return(0.04)
    elif(beaconName == 'Beacon III'):
        return(0.06)
    elif(beaconName == 'Beacon IV'):
        return(0.08)
    elif(beaconName == 'Beacon V'):
        return(0.1)
    else:
        return(0)


def getPetBuffSpeed(petName):
    """
    minionType = ['FARMING', 'FORAGING', 'COMBAT']\n
    Return(petBuffSpeed, minionType, minionName[])
    """
    if(petName == 'None'):
        return(0, '', [])
    elif(petName == 'Legendary Rabbit Pet Lv. 100'):
        return(0.3, 'FARMING', [])
    elif(petName == 'Legendary Ocelot Pet Lv. 100'):
        return(0.3, 'FORAGING', [])
    elif(petName == 'Legendary Magma Cube Pet Lv. 100'):
        return(0.3, '', ['Slime Minion', 'Magma Cube Minion'])
    elif(petName == 'Legendary Spider Pet Lv. 100'):
        return(0.3, '', ['Spider Minion', 'Tarantula Minion'])
    elif(petName == 'Legendary Chicken Pet Lv. 100'):
        return(0.3, '', ['Chicken Minion'])
    else:
        return(0, '', [])


def getStorageSlots(storage):
    storageData = {
        'None': 0,
        'Small Storage': 3,
        'Medium Storage': 9,
        'Large Storage': 15,
        'X-Large Storage': 21,
        'XX-Large Storage': 27
    }

    if(storage in storageData):
        return storageData[storage]
    return 0


def isDiamondSpreading(upgrade1, upgrade2):
    if(upgrade1 == 'Diamond Spreading' or upgrade2 == 'Diamond Spreading'):
        return(True)
    return(False)


def isPotatoSpreading(upgrade1, upgrade2):
    if(upgrade1 == 'Potato Spreading' or upgrade2 == 'Potato Spreading'):
        return(True)
    return(False)


def isLesserSoulflowEngine(upgrade1, upgrade2):
    if(upgrade1 == 'Lesser Soulflow Engine' or upgrade2 == 'Lesser Soulflow Engine'):
        return True
    return False


def isSoulFlowEngine(upgrade1, upgrade2):
    if(upgrade1 == 'Soulflow Engine' or upgrade2 == 'Soulflow Engine'):
        return True
    return False


def isKrampusHelmet(upgrade1, upgrade2):
    if(upgrade1 == 'Krampus Helmet' or upgrade2 == 'Krampus Helmet'):
        return(True)
    return(False)


def isInfernoFuel(fuel):
    if('Inferno Minion Fuel' in fuel):
        return(True)

    return(False)


def getMinionActions(minionName, isAFK):
    if(isAFK):
        return(1)
    return(2)
