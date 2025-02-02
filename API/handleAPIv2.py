import minionCalculator
import playerUtils
import hypixelAPI
from minion2JSON import numberToRoman

from flask import request, jsonify
from flask_caching import Cache
import flask

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

FLASK_CONFIG = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = flask.Flask(__name__)
app.config.from_mapping(FLASK_CONFIG)
cache = Cache(app)


@app.errorhandler(404)
def onPageNotFound(e):
    return jsonify({
        'success': False,
        'cause': 'Page Not Found'
    }), 404


@app.errorhandler(500)
def onErrorInApp(e):
    return jsonify({
        'success': False,
        'cause': 'Internal Server Error, please report this to Tonkaew#2345'
    }), 200


@app.route('/api/v2/minion/calculateminion', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def onCalculateMinion():
    queryParameters = request.args

    minionName = queryParameters.get('minion_name')
    if(minionName == None or minionName == ''):
        return(jsonify({
            'success': False,
            'cause': 'Missing minion_name field'
        }))

    minionTier = queryParameters.get('minion_tier')
    if(minionTier == None or minionName == ''):
        return(jsonify({
            'success': False,
            'cause': 'Missing minion_tier field'
        }))
    if(not minionTier.isnumeric()):
        return(jsonify({
            'success': False,
            'cause': 'Minion tier must be a number'
        }))
    minionTier = str(minionTier)

    minionSlot = queryParameters.get('minion_slot')
    if(minionSlot == None or minionName == ''):
        return(jsonify({
            'success': False,
            'cause': 'Missing minion_slot field'
        }))
    if(not minionSlot.isnumeric()):
        return(jsonify({
            'success': False,
            'cause': 'Minion slot must be a number'
        }))
    minionSlot = int(minionSlot)
    if(minionSlot > 40):
        return jsonify({
            'success': False,
            'cause': 'Minion slot can\'t be more than 40 due to server performance'
        })
    if(minionSlot <= 0):
        return jsonify({
            'success': False,
            'cause': 'Minion slot can\'t be zero.'
        })

    minionUpgrade1 = queryParameters.get('minion_upgrade1')
    if(minionUpgrade1 == None or minionUpgrade1 == ''):
        minionUpgrade1 = 'None'
    minionUpgrade2 = queryParameters.get('minion_upgrade2')
    if(minionUpgrade2 == None or minionUpgrade2 == ''):
        minionUpgrade2 = 'None'

    minionFuel = queryParameters.get('minion_fuel')
    if(minionFuel == None or minionFuel == ''):
        minionFuel = 'None'

    infernoFuel = queryParameters.get('inferno_fuel')
    if(infernoFuel == None or infernoFuel == ''):
        infernoFuel = 'None'

    minionStorage = queryParameters.get('minion_storage')

    isAFK = queryParameters.get('is_afk')
    if(isAFK == None or isAFK == ''):
        isAFK = False

    minionBonus1 = queryParameters.get('minion_bonus1')  # Crystal
    if(minionBonus1 == None or minionBonus1 == ''):
        minionBonus1 = 'None'
    minionBonus2 = queryParameters.get('minion_bonus2')  # Beacon
    if(minionBonus2 == None or minionBonus2 == ''):
        minionBonus2 = 'None'
    minionBonus3 = queryParameters.get('minion_bonus3')  # Pet
    if(minionBonus3 == None or minionBonus3 == ''):
        minionBonus3 = 'None'

    priceType = queryParameters.get('price_type')
    if(priceType == None or priceType == ''):
        priceType = 'ALL'
    if(priceType.lower() == 'all'):
        priceType = 'ALL'
    elif(priceType.lower() == 'npc'):
        priceType = 'NPC'
    elif(priceType.lower() == 'bazaar'):
        priceType = 'BZ'
    else:
        priceType = 'ALL'

    options = {
        'minion_name': minionName,
        'minion_tier': minionTier,
        'minion_slot': minionSlot,
        'minion_upgrade1': minionUpgrade1,
        'minion_upgrade2': minionUpgrade2,
        'minion_storage': minionStorage,
        'minion_fuel': minionFuel,
        'is_afk': isAFK,
        'minion_bonus1': minionBonus1,
        'minion_bonus2': minionBonus2,
        'minion_bonus3': minionBonus3,
        'price_type': priceType,
        'inferno_fuel': infernoFuel,
    }

    calculatedData = minionCalculator.calculateMinion(options)
    if(calculatedData['success'] == False):
        return(jsonify({
            'success': False,
            'cause': calculatedData['cause']
        }))

    calculatedData['data']['formatted_name'] = ''
    if(minionSlot > 1):
        calculatedData['data']['formatted_name'] += str(minionSlot) + 'x '
    calculatedData['data']['formatted_name'] += calculatedData['data']['name'] + \
        ' ' + numberToRoman(int(minionTier))

    if(isAFK == True):
        calculatedData['data']['formatted_name'] += ' (AFK)'

    calculatedData['data']['tier'] = minionTier
    return(jsonify({
        'success': True,
        'data': calculatedData['data']
    }))


@app.route('/api/v2/minion/top10', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def onCalculateTop10():
    queryParameters = request.args

    priceType = queryParameters.get('price_type')
    if(priceType == None or priceType == ''):
        priceType = 'ALL'
    if(priceType.lower() == 'all'):
        priceType = 'ALL'
    elif(priceType.lower() == 'npc'):
        priceType = 'NPC'
    elif(priceType.lower() == 'bazaar'):
        priceType = 'BZ'

    minionTier = queryParameters.get('minion_tier')
    if(minionTier == None or minionTier == ''):
        return(jsonify({
            'success': False,
            'cause': 'Missing minion_tier field'
        }))
    if(minionTier.isnumeric()):
        minionTier = int(minionTier)
        if(not (1 <= minionTier <= 12)):
            return(jsonify({
                'success': False,
                'cause': 'Minion tier must be between 1 and 12 or "ALL"'
            }))
    else:
        if(minionTier.lower() != 'all'):
            return(jsonify({
                'success': False,
                'cause': 'Minion tier must be between 1 and 12 or ALL'
            }))

    options = {
        'minion_tier': str(minionTier),
        'price_type': priceType
    }

    earningData = minionCalculator.calculateTop10(options)
    if(earningData['success'] == False):
        return(jsonify(earningData))

    formattedPriceType = priceType.replace('BZ', 'Bazaar')
    formattedPriceType = formattedPriceType.replace('ALL', 'Bazaar & NPC')
    return(jsonify({
        'success': True,
        'data': {
            'minions': earningData['data'],
            'tier': str(minionTier).title(),
            'timestamp': earningData['timestamp'],
            'sell_to': formattedPriceType
        }
    }))


@app.route('/api/v2/minion/craft', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def onMinionPrice():
    queryParameters = request.args

    minionName = queryParameters.get('minion_name')
    if(minionName == None or minionName == ''):
        return(jsonify({
            'success': False,
            'cause': 'Missing minion_name field'
        }))
    minionName = (minionName.lower()).replace(' minion', '')
    minionName = minionName.strip().title() + ' Minion'

    toTier = queryParameters.get('tier')
    if(toTier == None or toTier == ''):
        return(jsonify({
            'success': False,
            'cause': 'Missing tier field'
        }))
    if(not toTier.isnumeric()):
        return(jsonify({
            'success': False,
            'cause': 'Minion tier must be a number'
        }))
    toTier = int(toTier)

    fromTier = queryParameters.get('from')
    if(fromTier == None or fromTier == ''):
        fromTier = '1'
    if(not fromTier.isnumeric()):
        return(jsonify({
            'success': False,
            'cause': 'Minion tier ( from ) must be a number'
        }))
    fromTier = int(fromTier)

    currentMinion = minionCalculator.getMinionData(minionName)
    if(len(currentMinion) == 0):
        return jsonify({
            'success': False,
            'cause': minionName + ' doesn\'t exist yet, maybe later.'
        })
    if(str(fromTier) not in currentMinion['tier'] or str(toTier) not in currentMinion['tier']):
        return jsonify({
            'success': False,
            'cause': 'Invalid minion tier ( ' + str(fromTier) + '-' + str(toTier) + ' )'
        })

    warning = []
    bazaarProducts = hypixelAPI.getBazaarProducts()
    skipBazaar = False
    if(bazaarProducts['success'] == False):
        skipBazaar = True
        warning.append('No Bazaar data')

    materials = {}
    for i in range(fromTier, toTier + 1):
        i = str(i)
        if(i not in currentMinion['tier']):
            return jsonify({
                'success': False,
                'cause': 'Invalid minion tier ( ' + str(i) + ' )'
            })

        materials[i] = {
            'total_price': 0,
            'items': currentMinion['tier'][i]['upgrade_items']
        }
        if(skipBazaar == True):
            continue

        totalPrice = 0
        for m in materials[i]['items']:
            itemName = m['name']
            if('_MINION_' in itemName):
                minionMaterialName = ' '.join(
                    itemName.split('_')[:-2]).title() + ' Minion'
                minionMaterialTier = itemName.split('_')[-1]

                minionMaterial = minionCalculator.getMinionData(
                    minionMaterialName)
                if(len(minionMaterial) == 0):
                    continue

                minionMaterialPrice = minionCalculator.calculateMinionPrice(
                    minionMaterial, m['amount'], minionMaterialTier, bazaarProducts)
                if(minionMaterialPrice['success'] == False):
                    continue

                m['price'] = minionMaterialPrice['data']['all_tier']['total']
                m['items'] = minionMaterialPrice['data']['all_tier']['items']
                m['name'] = minionMaterialName + ' ' + \
                    numberToRoman(int(minionMaterialTier))
                totalPrice += m['price']
                continue

            if(itemName == 'COINS'):
                totalPrice += m['amount']
                m['name'] = 'Coins'
                continue

            if(itemName in bazaarProducts['products']):
                itemPrice = bazaarProducts['products'][itemName]['quick_status']['buyPrice']
                m['price'] = itemPrice * m['amount']
                totalPrice += m['price']

            m['name'] = itemName.replace('_', ' ').title()
        materials[i]['total_price'] = totalPrice

    if(len(materials) == 0):
        return jsonify({
            'success': False,
            'cause': 'There is problem calculating minion price'
        })

    formattedName = minionName + ' '
    if(fromTier != 1 and fromTier != toTier):
        formattedName += numberToRoman(fromTier) + '-'
    formattedName += numberToRoman(toTier)

    return jsonify({
        'success': True,
        'data': {
            'materials': materials,
            'formatted_name': formattedName
        },
        'warning': ', '.join(warning)
    })


@app.route('/api/v2/player/cheapestupgrade', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def onCheapestUpgrade():
    queryParameters = request.args

    minecraftUUID = {}
    minecraftIGNKey = queryParameters.get('minecraft_ign')
    if(minecraftIGNKey == None or minecraftIGNKey == ''):
        minecraftUUIDKey = queryParameters.get('minecraft_uuid')
        if(minecraftUUIDKey == None or minecraftUUIDKey == ''):
            return(jsonify({
                'success': False,
                'cause': 'Missing minecraft_ign field'
            }))

        minecraftIGN = hypixelAPI.getMinecraftIGN(minecraftUUIDKey)
        if(minecraftIGN['success'] == False):
            return(jsonify({'success': False, 'cause': 'Can\'t find that user'}))

        minecraftUUID = {
            'uuid': minecraftUUIDKey,
            'name': minecraftIGN['name']
        }
    else:
        minecraftUUID = hypixelAPI.getMinecraftUUID(minecraftIGNKey)
        if(minecraftUUID['success'] == False):
            return(jsonify(minecraftUUID))

    profile = hypixelAPI.getLatestSkyblockProfile(minecraftUUID['uuid'])
    if(profile['success'] == False):
        return(jsonify({
            'success': False,
            'cause': profile['cause']
        }))

    sortedCraftedMinions = {}
    profile = profile['profile']
    apiDisabled = 0
    for memberUUID in profile['members']:
        if('crafted_generators' not in profile['members'][memberUUID]):
            apiDisabled += 1
            continue

        for m in profile['members'][memberUUID]['crafted_generators']:
            minionName = ' '.join(m.split('_')[:-1])
            minionTier = int(m.split('_')[-1])

            if(minionName in sortedCraftedMinions):
                if(minionTier > sortedCraftedMinions[minionName]['tier']):
                    sortedCraftedMinions[minionName]['tier'] = minionTier
            else:
                sortedCraftedMinions[minionName] = {
                    'name': minionName,
                    'tier': minionTier
                }

    bazaarProducts = hypixelAPI.getBazaarProducts()

    neverCraftedMinions = []
    for m in minionCalculator.getMinionsData()['minions']:
        neverCraftedMinions.append(m['name'])

    failedMinions, minionsPrice = [], []
    for m in sortedCraftedMinions:
        minionName = m.title() + ' Minion'
        minionName = minionName.replace('Cocoa', 'Cocoa Beans')
        minionName = minionName.replace('Cavespider', 'Cave Spider')
        minionName = minionName.replace('Nether Warts', 'Nether Wart')
        minionName = minionName.replace('Ender Stone', 'End Stone')
        _minionData = minionCalculator.getMinionData(minionName)
        if(len(_minionData) == 0):
            failedMinions.append(minionName)
            continue

        if(minionName in neverCraftedMinions):
            neverCraftedMinions.remove(minionName)

        minionNextTier = str(sortedCraftedMinions[m]['tier'] + 1)
        if(minionNextTier not in _minionData['tier']):
            continue

        minionPrice = minionCalculator.calculateMinionPrice(
            _minionData, 1, minionNextTier, bazaarProducts)
        if(minionPrice['success'] == False):
            return(jsonify(minionPrice))

        minionsPrice.append({
            'name': minionName + ' ' + minionNextTier,
            'total': minionPrice['data']['last_tier']['total'],
            'items': minionPrice['data']['last_tier']['items'],
            'pictures': minionPrice['data']['pictures']
        })

    for m in neverCraftedMinions:
        _minionData = minionCalculator.getMinionData(m)
        if(len(_minionData) == 0):
            failedMinions.append(m)
            continue

        minionPrice = minionCalculator.calculateMinionPrice(
            _minionData, 1, '1', bazaarProducts)
        if(minionPrice['success'] == False):
            return(jsonify(minionPrice))

        minionsPrice.append({
            'name': m + ' 1',
            'total': minionPrice['data']['last_tier']['total'],
            'items': minionPrice['data']['last_tier']['items'],
            'pictures': minionPrice['data']['pictures']
        })

    warning = ''
    if(apiDisabled != 0):
        warning = '( API Enabled ' + str(apiDisabled) + \
            '/' + str(len(profile['members'])) + ' )'
    
    warning2 = ''
    if(len(failedMinions) != 0):
        # return(jsonify({
        #     'success': False,
        #     'cause': 'Missing ' + ', '.join(failedMinions) + ' data'
        # }))
        warning2 += 'Missing ' + ', '.join(failedMinions) + ' data'

    # image = 'https://visage.surgeplay.com/face/' + minecraftUUID['uuid'] + '.png'
    image = 'https://mc-heads.net/avatar/' + minecraftUUID['uuid'] + '.png'

    cheapestUpgrade = sorted(
        minionsPrice, key=lambda k: k.get('total', 0), reverse=False)

    return(jsonify({
        'success': True,
        'data': {
            'name': minecraftUUID['name'],
            'uuid': minecraftUUID['uuid'],
            'profile_name': profile['cute_name'],
            'minions': cheapestUpgrade,
            'skin_head': image,
            'warning': warning,
            'warning2': warning2,
            'timestamp': profile['members'][minecraftUUID['uuid']]['last_save']
        }
    }))


@app.route('/api/v2/player/cheapestmax', methods=['GET'])
@cache.cached(timeout=120, query_string=True)
def onCheapestMax():
    queryParameters = request.args

    minecraftUUID = {}
    minecraftIGNKey = queryParameters.get('minecraft_ign')
    if(minecraftIGNKey == None or minecraftIGNKey == ''):
        minecraftUUIDKey = queryParameters.get('minecraft_uuid')
        if(minecraftUUIDKey == None or minecraftUUIDKey == ''):
            return(jsonify({
                'success': False,
                'cause': 'Missing minecraft_ign field'
            }))

        minecraftIGN = hypixelAPI.getMinecraftIGN(minecraftUUIDKey)
        if(minecraftIGN['success'] == False):
            return(jsonify({'success': False, 'cause': 'Can\'t find that user'}))

        minecraftUUID = {
            'uuid': minecraftUUIDKey,
            'name': minecraftIGN['name']
        }
    else:
        minecraftUUID = hypixelAPI.getMinecraftUUID(minecraftIGNKey)
        if(minecraftUUID['success'] == False):
            return(jsonify(minecraftUUID))

    profile = hypixelAPI.getLatestSkyblockProfile(minecraftUUID['uuid'])
    if(profile['success'] == False):
        return(jsonify({
            'success': False,
            'cause': profile['cause']
        }))

    sortedCraftedMinions = {}
    profile = profile['profile']
    apiDisabled = 0
    for memberUUID in profile['members']:
        if('crafted_generators' not in profile['members'][memberUUID]):
            apiDisabled += 1
            continue

        for m in profile['members'][memberUUID]['crafted_generators']:
            minionName = ' '.join(m.split('_')[:-1])
            minionTier = int(m.split('_')[-1])

            if(minionName in sortedCraftedMinions):
                if(minionTier > sortedCraftedMinions[minionName]['tier']):
                    sortedCraftedMinions[minionName]['tier'] = minionTier
            else:
                sortedCraftedMinions[minionName] = {
                    'name': minionName,
                    'tier': minionTier
                }

    bazaarProducts = hypixelAPI.getBazaarProducts()

    neverCraftedMinions = []
    for m in minionCalculator.getMinionsData()['minions']:
        neverCraftedMinions.append(m['name'])

    failedMinions, minionsList = [], []
    for m in sortedCraftedMinions:
        minionName = m.title() + ' Minion'
        minionName = minionName.replace('Cocoa', 'Cocoa Beans')
        minionName = minionName.replace('Cavespider', 'Cave Spider')
        minionName = minionName.replace('Nether Warts', 'Nether Wart')
        minionName = minionName.replace('Ender Stone', 'End Stone')
        _minionData = minionCalculator.getMinionData(minionName)
        if(len(_minionData) == 0):
            failedMinions.append(minionName)
            continue

        if(minionName in neverCraftedMinions):
            neverCraftedMinions.remove(minionName)

        minionMaxTier = len(_minionData['tier'])
        currentTier = sortedCraftedMinions[m]['tier']
        if(currentTier == minionMaxTier):
            continue

        minionsList.append({
            'data': _minionData,
            'from': currentTier,
            'to': minionMaxTier
        })

    for m in neverCraftedMinions:
        _minionData = minionCalculator.getMinionData(m)
        if(len(_minionData) == 0):
            failedMinions.append(m)
            continue

        minionMaxTier = len(_minionData['tier'])
        currentTier = 1

        minionsList.append({
            'data': _minionData,
            'from': currentTier,
            'to': minionMaxTier
        })

    minionPrice = []
    for m in minionsList:
        items = {}

        # loop between tier
        for i in range(int(m['from']), int(m['to'])+1):
            i = str(i)
            currentMinion = m['data']
            if(i not in currentMinion['tier']):
                failedMinions.append(currentMinion['name'])
                continue

            # loop between items in current tier ( i )
            currTierItems = currentMinion['tier'][i]['upgrade_items']
            for j in currTierItems:
                itemName = j['name']

                if('_MINION_' in itemName):
                    matMinionName = ' '.join(
                        itemName.split('_')[:-2]).title() + ' Minion'
                    matMinionTier = itemName.split('_')[-1]

                    matMinion = minionCalculator.getMinionData(matMinionName)
                    if(len(matMinion) == 0):
                        continue

                    matMinionPrice = minionCalculator.calculateMinionPrice(
                        matMinion, 1, matMinionTier, bazaarProducts)
                    if(matMinionPrice['success'] == False):
                        continue

                    j['price'] = matMinionPrice['data']['all_tier']['total']
                    j['items'] = matMinionPrice['data']['all_tier']['items']
                    j['name'] = matMinionName + ' ' + \
                        numberToRoman(int(matMinionTier))
                elif(itemName == 'COINS'):
                    j['name'] = 'Coins'
                    j['price'] = j['amount']
                elif(itemName in bazaarProducts['products']):
                    itemPrice = bazaarProducts['products'][itemName]['quick_status']['buyPrice']
                    j['price'] = itemPrice * j['amount']
                else:
                    j['price'] = 0

                if(itemName not in items):
                    items[itemName] = j
                else:
                    items[itemName]['amount'] += j['amount']
                    items[itemName]['price'] += j['price']

                items[itemName]['name'] = itemName.replace('_', ' ').title()

        wikiLink = ''
        minionResource = minionCalculator.getMinionResource(m['data']['name'])
        if(minionResource):
            wikiLink = minionResource['wiki_link']

        minionPrice.append({
            'name': m['data']['name'],
            'formatted_name': m['data']['name'] + ' ' + numberToRoman(int(m['from'])) + '-' + numberToRoman(int(m['to'])),
            'wiki_link': wikiLink,
            'from': int(m['from']),
            'to': int(m['to']),
            'items': list(items.values()),
            'total_price': sum([items[i]['price'] for i in items])
        })

    warning = ''
    if(apiDisabled != 0):
        warning = '( API Enabled ' + str(apiDisabled) + \
            '/' + str(len(profile['members'])) + ' )'

    warning2 = ''
    if(len(failedMinions) != 0):
        # return(jsonify({
        #     'success': False,
        #     'cause': 'Missing ' + ', '.join(failedMinions) + ' data'
        # }))
        warning2 += 'Missing ' + ', '.join(failedMinions) + ' data'

    # image = 'https://visage.surgeplay.com/face/' + minecraftUUID['uuid'] + '.png'
    image = 'https://mc-heads.net/avatar/' + minecraftUUID['uuid'] + '.png'

    cheapestUpgrade = sorted(minionPrice, key=lambda k: k.get(
        'total_price', 0), reverse=False)

    return(jsonify({
        'success': True,
        'data': {
            'name': minecraftUUID['name'],
            'uuid': minecraftUUID['uuid'],
            'profile_name': profile['cute_name'],
            'minions': cheapestUpgrade,
            'skin_head': image,
            'warning': warning,
            'warning2': warning2,
            'timestamp': profile['members'][minecraftUUID['uuid']]['last_save']
        }
    }))


talismansData = playerUtils.getTalismansData()


@app.route('/api/v2/player/cheapesttalisman', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def onCheapestTalisman():
    """
    active: talisman_bag, inv_contents\n
    inactive: backpack_contents, ender_chest_contents, personal_vault_contents\n
    both combine check dupe, and not crafted one\n
    """
    queryParameters = request.args

    minecraftUUID = {}
    minecraftIGNKey = queryParameters.get('minecraft_ign')
    if(minecraftIGNKey == None or minecraftIGNKey == ''):
        minecraftUUIDKey = queryParameters.get('minecraft_uuid')
        if(minecraftUUIDKey == None or minecraftUUIDKey == ''):
            return(jsonify({
                'success': False,
                'cause': 'Missing minecraft_ign field'
            }))

        minecraftIGN = hypixelAPI.getMinecraftIGN(minecraftUUIDKey)
        if(minecraftIGN['success'] == False):
            return(jsonify({'success': False, 'cause': 'Can\'t find that user'}))

        minecraftUUID = {
            'uuid': minecraftUUIDKey,
            'name': minecraftIGN['name']
        }
    else:
        minecraftUUID = hypixelAPI.getMinecraftUUID(minecraftIGNKey)
        if(minecraftUUID['success'] == False):
            return(jsonify(minecraftUUID))

    profile = hypixelAPI.getLatestSkyblockProfile(minecraftUUID['uuid'])
    if(profile['success'] == False):
        return(jsonify({
            'success': False,
            'cause': profile['cause']
        }))
    profileName = profile['profile']['cute_name']
    talismans = hypixelAPI.getShiiyuTalismansAPI(
        minecraftUUID['name'], profileName)
    if(talismans['success'] == False):
        return jsonify(talismans)

    allTalismans = talismansData['data']['talismans'].copy()
    upgradedTalismans = talismansData['data']['talisman_upgrades'].copy()
    duplicateTalismans = talismansData['data']['talisman_duplicates'].copy()

    noDataTalismans = []

    if('talismans' not in talismans['data']):
        return jsonify({
            'success': False,
            'cause': 'This profile doesn\'t have any talismans!'
        })

    talismans = talismans['data']['talismans']
    for t in talismans:
        itemID = t['tag']['ExtraAttributes']['id']
        if(itemID in allTalismans):
            currentTalisman = itemID

            while True:
                if('WEDDING_RING_' in currentTalisman or 'CAMPFIRE_TALISMAN_' in currentTalisman):
                    for dup in duplicateTalismans:
                        if(currentTalisman in duplicateTalismans[dup]):
                            currentTalisman = dup

                if(allTalismans[currentTalisman] == None):
                    allTalismans.pop(currentTalisman)
                    # noDataTalismans.append(currentTalisman)
                    break

                # print(currentTalisman)
                if('upgraded_of' in allTalismans[currentTalisman]):
                    lastTalisman = allTalismans[currentTalisman]['upgraded_of']
                    allTalismans.pop(currentTalisman)
                    currentTalisman = lastTalisman
                else:
                    allTalismans.pop(currentTalisman)
                    break
        else:
            noDataTalismans.append(itemID)

    calculatedTalismans = []
    for t in allTalismans:
        currentTalisman = allTalismans[t]
        if(currentTalisman == None):
            noDataTalismans.append(t)
            continue

        if('acquire_methods' not in currentTalisman):
            noDataTalismans.append(t)
            continue

        talismanPrice = playerUtils.getTalismanPrice(t)
        if(talismanPrice['success'] == False):
            continue

        if('required_items' in talismanPrice['data']):
            skip = False
            for i in talismanPrice['data']['required_items']:
                if(i not in [j['tag']['ExtraAttributes']['id'] for j in talismans]):
                    skip = True
                    break
            if skip:
                continue

        calculatedTalismans.append(talismanPrice['data'])

    cheapestTalismans = sorted(
        calculatedTalismans, key=lambda k: k.get('total_price', 0), reverse=False)

    warnings = [talismansData['warning']]
    if(talismansData['warning'] == ''):
        warnings = []

    if(len(noDataTalismans) != 0):
        warnings.append(
            'Missing ' + str(len(noDataTalismans)) + ' talisman data.')

    image = 'https://mc-heads.net/avatar/' + minecraftUUID['uuid'] + '.png'

    return jsonify({
        'success': True,
        'warning': warnings,
        'data': {
            # 'talismans': [t['tag']['ExtraAttributes']['id'] for t in talismans],
            'missing_talismans': cheapestTalismans,
            'name': minecraftUUID['name'],
            'profile_name': profileName,
            'skin_head': image,
            'timestamp': profile['profile']['members'][minecraftUUID['uuid']]['last_save']
        }
    })


@app.route('/api/v2/player/dungeonprofile', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def onDungeonProfile():
    queryParameters = request.args

    minecraftUUID = {}
    minecraftIGNKey = queryParameters.get('minecraft_ign')
    if(minecraftIGNKey == None or minecraftIGNKey == ''):
        minecraftUUIDKey = queryParameters.get('minecraft_uuid')
        if(minecraftUUIDKey == None or minecraftUUIDKey == ''):
            return(jsonify({
                'success': False,
                'cause': 'Missing minecraft_ign field'
            }))

        minecraftIGN = hypixelAPI.getMinecraftIGN(minecraftUUIDKey)
        if(minecraftIGN['success'] == False):
            return(jsonify({'success': False, 'cause': 'Can\'t find that user'}))

        minecraftUUID = {
            'uuid': minecraftUUIDKey,
            'name': minecraftIGN['name']
        }
    else:
        minecraftUUID = hypixelAPI.getMinecraftUUID(minecraftIGNKey)
        if(minecraftUUID['success'] == False):
            return(jsonify(minecraftUUID))

    profile = hypixelAPI.getLatestSkyblockProfile(minecraftUUID['uuid'])
    if(profile['success'] == False):
        return(jsonify({
            'success': False,
            'cause': profile['cause']
        }))

    data = {'name': minecraftUUID['name']}
    profile = profile['profile']
    if('dungeons' not in profile['members'][minecraftUUID['uuid']]):
        return jsonify({
            'success': False,
            'cause': 'This user haven\'t played dungeon before'
        })
    dungeonProfile = profile['members'][minecraftUUID['uuid']]['dungeons']

    cataXp, cataLvl = 0, 0
    if('experience' in dungeonProfile['dungeon_types']['catacombs']):
        cataXp = dungeonProfile['dungeon_types']['catacombs']['experience']
        cataLvl = playerUtils.convertCatacombXp2Lvl(cataXp)
    data['catacombs'] = {
        'xp': cataXp,
        'lvl': cataLvl
    }

    selectedClass = 'None'
    if('selected_dungeon_class' in dungeonProfile):
        selectedClass = dungeonProfile['selected_dungeon_class']
    data['classes'] = {'selected_dungeon_class': selectedClass}

    for c in dungeonProfile['player_classes']:
        if 'experience' not in dungeonProfile['player_classes'][c]:
            data['classes'][c] = 0
            continue
        data['classes'][c] = playerUtils.convertCatacombXp2Lvl(
            dungeonProfile['player_classes'][c]['experience'])

    timestamp = 0
    if('last_save' in profile['members'][minecraftUUID['uuid']]):
        timestamp = profile['members'][minecraftUUID['uuid']]['last_save']

    rawArmours = playerUtils.decodeInventoryData(
        profile['members'][minecraftUUID['uuid']]['inv_armor']['data'])
    armours = playerUtils.convertInventory2List(rawArmours)
    armours.reverse()
    data['gears'] = {'armours': armours}

    pet = {
        'name': 'No active pet',
        'formatted_name': 'No active pet',
        'rarity': '',
        'lvl': 0,
        'pet_item': ''
    }
    for p in profile['members'][minecraftUUID['uuid']]['pets']:
        if(p['active'] == True):
            pet['name'] = p['type'].replace('_', ' ').title()
            pet['rarity'] = p['tier'].title()
            pet['lvl'] = playerUtils.convertPetXp2Lvl(p['exp'], p['tier'])

            pet['formatted_name'] = pet['rarity']
            pet['formatted_name'] += ' ' + pet['name']
            pet['formatted_name'] += ' ( Lv.' + str(pet['lvl']) + ' )'

            petItem = ''
            if(p['heldItem'] is not None):
                petItem = p['heldItem']
                petItem = petItem.replace('PET_ITEM_', '')
                petItem = petItem.replace('_', ' ')
                petItem = petItem.title()

                pet['pet_item'] = petItem
                pet['formatted_name'] += ' ( ' + petItem + ' )'
    data['gears']['pet'] = pet

    floors = {
        'catacombs': {'tier_completions': {}, 'times_played': {}},
        'master_catacombs': {'tier_completions': {}}
    }
    if('tier_completions' in dungeonProfile['dungeon_types']['catacombs']):
        floors['catacombs']['tier_completions'] = dungeonProfile['dungeon_types']['catacombs']['tier_completions']
    if('times_played' in dungeonProfile['dungeon_types']['catacombs']):
        floors['catacombs']['times_played'] = dungeonProfile['dungeon_types']['catacombs']['times_played']
    if('master_catacombs' in dungeonProfile['dungeon_types']):
        if('tier_completions' in dungeonProfile['dungeon_types']['master_catacombs']):
            floors['master_catacombs']['tier_completions'] = dungeonProfile['dungeon_types']['master_catacombs']['tier_completions']
    data['floors'] = floors

    if('inv_contents' in profile['members'][minecraftUUID['uuid']]):
        rawInventory = profile['members'][minecraftUUID['uuid']
                                          ]['inv_contents']['data']
        inventory = playerUtils.decodeInventoryData(rawInventory)
        data['gears']['hotbar'] = playerUtils.getHotbarItems(inventory)
    else:
        data['gears']['hotbar'] = []

    mics = {'secrets_found': 0, 'journals': 'None', 'highest_floor': 'None'}
    shiiyuData = hypixelAPI.getShiiyuDungeonAPI(
        minecraftUUID['name'], profile['cute_name'])
    if shiiyuData['success'] == True:
        if 'highest_floor' in shiiyuData['data']['dungeons']['catacombs']:
            mics['highest_floor'] = shiiyuData['data']['dungeons']['catacombs']['highest_floor'].replace(
                '_', ' ').title()

        if 'dungeons' in shiiyuData['data']:
            mics['secrets_found'] = shiiyuData['data']['dungeons']['secrets_found']

        if 'journals' in shiiyuData['data']['dungeons']:
            mics['journals'] = str(
                shiiyuData['data']['dungeons']['journals']['journals_completed'])
            mics['journals'] += ' ( '
            mics['journals'] += str(shiiyuData['data']
                                    ['dungeons']['journals']['pages_collected'])
            mics['journals'] += '/'
            mics['journals'] += str(shiiyuData['data']
                                    ['dungeons']['journals']['total_pages'])
            mics['journals'] += ' )'
    data['mics'] = mics
    # data['mics']['head_pic'] = 'https://visage.surgeplay.com/face/' + minecraftUUID['uuid']
    data['mics']['head_pic'] = 'https://mc-heads.net/avatar/' + \
        minecraftUUID['uuid']

    data['timestamp'] = profile['members'][minecraftUUID['uuid']]['last_save']
    return jsonify({
        'success': True,
        'data': data
    })


@app.route('/api/v2/player/essences', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def onDungeonEssence():
    queryParameters = request.args

    minecraftUUID = {}
    minecraftIGNKey = queryParameters.get('minecraft_ign')
    if(minecraftIGNKey == None or minecraftIGNKey == ''):
        minecraftUUIDKey = queryParameters.get('minecraft_uuid')
        if(minecraftUUIDKey == None or minecraftUUIDKey == ''):
            return(jsonify({
                'success': False,
                'cause': 'Missing minecraft_ign field'
            }))

        minecraftIGN = hypixelAPI.getMinecraftIGN(minecraftUUIDKey)
        if(minecraftIGN['success'] == False):
            return(jsonify({'success': False, 'cause': 'Can\'t find that user'}))

        minecraftUUID = {
            'uuid': minecraftUUIDKey,
            'name': minecraftIGN['name']
        }
    else:
        minecraftUUID = hypixelAPI.getMinecraftUUID(minecraftIGNKey)
        if(minecraftUUID['success'] == False):
            return(jsonify(minecraftUUID))

    profile = hypixelAPI.getLatestSkyblockProfile(minecraftUUID['uuid'])
    if(profile['success'] == False):
        return(jsonify({
            'success': False,
            'cause': profile['cause']
        }))

    data = {'name': minecraftUUID['name']}
    profileName = profile['profile']['cute_name']

    profile = profile['profile']['members'][minecraftUUID['uuid']]
    timestamp = profile['last_save']

    essences = ['wither', 'spider', 'undead', 'dragon', 'diamond', 'ice']
    playerEssences = {}
    for e in essences:
        keyName = 'essence_' + e
        if(keyName in profile):
            playerEssences[e] = profile[keyName]

    headURL = 'https://mc-heads.net/avatar/' + minecraftUUID['uuid']

    return jsonify({
        'success': True,
        'essences': playerEssences,
        'profile_name': profileName,
        'name': minecraftUUID['name'],
        'head_pic': headURL,
        'timestamp': timestamp
    })


@app.route('/api/v2/player/getbestcollections', methods=['GET'])
def onGetBestCollections():
    queryParameters = request.args

    minecraftUUID = {}
    minecraftIGNKey = queryParameters.get('minecraft_ign')
    if(minecraftIGNKey == None or minecraftIGNKey == ''):
        minecraftUUIDKey = queryParameters.get('minecraft_uuid')
        if(minecraftUUIDKey == None or minecraftUUIDKey == ''):
            return(jsonify({
                'success': False,
                'cause': 'Missing minecraft_ign field'
            }))

        minecraftIGN = hypixelAPI.getMinecraftIGN(minecraftUUIDKey)
        if(minecraftIGN['success'] == False):
            return(jsonify({'success': False, 'cause': 'Can\'t find that user'}))

        minecraftUUID = {
            'uuid': minecraftUUIDKey,
            'name': minecraftIGN['name']
        }
    else:
        minecraftUUID = hypixelAPI.getMinecraftUUID(minecraftIGNKey)
        if(minecraftUUID['success'] == False):
            return(jsonify(minecraftUUID))

    profile = hypixelAPI.getLatestSkyblockProfile(minecraftUUID['uuid'])
    if(profile['success'] == False):
        return(jsonify({
            'success': False,
            'cause': profile['cause']
        }))

    sortedCraftedMinions = {}
    profile = profile['profile']
    apiDisabled = 0
    for memberUUID in profile['members']:
        if('crafted_generators' not in profile['members'][memberUUID]):
            apiDisabled += 1
            continue

        for m in profile['members'][memberUUID]['crafted_generators']:
            minionName = ' '.join(m.split('_')[:-1])
            minionTier = int(m.split('_')[-1])

            if(minionName in sortedCraftedMinions):
                if(minionTier > sortedCraftedMinions[minionName]['tier']):
                    sortedCraftedMinions[minionName]['tier'] = minionTier
            else:
                sortedCraftedMinions[minionName] = {
                    'name': minionName,
                    'tier': minionTier
                }

    bazaarProducts = hypixelAPI.getBazaarProducts()

    maxCraftedMinions = []
    for m in minionCalculator.getMinionsData()['minions']:
        maxCraftedMinions.append(m['name'])

    failedMinions, minionsPrice = [], []
    for m in sortedCraftedMinions:
        minionName = m.title() + ' Minion'
        minionName = minionName.replace('Cocoa', 'Cocoa Beans')
        minionName = minionName.replace('Cavespider', 'Cave Spider')
        minionName = minionName.replace('Nether Warts', 'Nether Wart')
        minionName = minionName.replace('Ender Stone', 'End Stone')
        _minionData = minionCalculator.getMinionData(minionName)
        if(len(_minionData) == 0):
            failedMinions.append(minionName)
            continue

        if(minionName in maxCraftedMinions):
            maxCraftedMinions.remove(minionName)

        minionMaxTier = str(sortedCraftedMinions[m]['tier'])
        if(minionMaxTier not in _minionData['tier']):
            continue

        options = {
            'minion_name': minionName,
            'minion_tier': minionMaxTier,
            'minion_slot': 1,
            'minion_upgrade1': 'Super Compactor 3000',
            'minion_upgrade2': 'Diamond Spreading',
            'minion_fuel': 'Enchanted Lava Bucket',
            'is_afk': False,
            'minion_bonus1': 'None',
            'minion_bonus2': 'None',
            'minion_bonus3': 'None',
            'bazaar_products': bazaarProducts,
            'price_type': 'ALL'
        }
        minionEarnings = minionCalculator.calculateMinion(options)
        if(minionEarnings['success'] == False):
            return(jsonify(minionEarnings))

        minionsPrice.append({
            'name': minionName + ' ' + minionMaxTier,
            'total': minionEarnings['data']['earnings']['per_hour']
        })

    if(len(failedMinions) != 0):
        return(jsonify({
            'success': False,
            'cause': 'Missing ' + ', '.join(failedMinions) + ' data'
        }))

    warning = ''
    if(apiDisabled != 0):
        warning = '( API Enabled ' + str(apiDisabled) + \
            '/' + str(len(profile['members'])) + ' )'

    # image = 'https://visage.surgeplay.com/face/' + minecraftUUID['uuid']
    image = 'https://mc-heads.net/avatar/' + minecraftUUID['uuid']

    bestCollections = sorted(
        minionsPrice, key=lambda k: k.get('total', 0), reverse=True)

    return(jsonify({
        'success': True,
        'data': {
            'name': minecraftUUID['name'],
            'uuid': minecraftUUID['uuid'],
            'profile_name': profile['cute_name'],
            'minions': bestCollections,
            'skin_head': image,
            'warning': warning,
            'timestamp': profile['members'][minecraftUUID['uuid']]['last_save']
        }
    }))


@app.route('/api/v2/player/getuuid', methods=['GET'])
def onGetMinecraftUUID():
    queryParameters = request.args

    minecraftIGN = queryParameters.get('minecraft_ign')
    if(minecraftIGN == None or minecraftIGN == ''):
        return(jsonify({
            'success': False,
            'cause': 'Missing minecraft_ign field'
        }))

    data = hypixelAPI.getMinecraftUUID(minecraftIGN)
    if(data['success'] == False):
        return(jsonify(data))

    dashUUID = hypixelAPI.convertToDashedUUID(data['uuid'])
    return(jsonify({
        'success': True,
        'data': {
            'dashed_uuid': dashUUID,
            'undashed_uuid': data['uuid'],
            'name': data['name']
        }
    }))


if __name__ == '__main__':
    app.run(port=5001)
