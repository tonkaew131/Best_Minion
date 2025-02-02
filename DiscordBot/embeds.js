const Discord = require('discord.js');

const Utils = require('./utils');

const BESTMINION_THEME_COLOR = '#f9eb45';
const BESTMINION_WAIT_COLOR = '#154897';

const BESTMINION_CORRECT_COLOR = '#00ff00';
const BESTMINION_ERROR_COLOR = '#ff0000';

const BLANK_EMOJI = '<:BLANK:874926396235989063>';
const DISCORD_INVITE = 'https://discord.com/invite/yw9bNwR';
const MICS_EMOTES = {
    'ENCHANTED_COOKIE': '<:ENCHANTED_COOKIE:874921436899319818>',
    'GOD_POTION_2': '<:GOD_POTION_2:874923045901459466>',
    'MAYOR_DERPY': '<:MAYOR_DERPY:874925675251908608>',
    'WHEAT_GENERATOR_1': '<:WHEAT_GENERATOR_1:825342120663449661>',
    'ESSENCE_WITHER': '<:ESSENCE_WITHER:891700005453307954>',
    'ESSENCE_UNDEAD': '<:ESSENCE_UNDEAD:891700050915368991>',
    'ESSENCE_SPIDER': '<:ESSENCE_SPIDER:891699972184109128>',
    'ESSENCE_ICE': '<:ESSENCE_ICE:891699923278516295>',
    'ESSENCE_GOLD': '<:ESSENCE_GOLD:891699845298028546>',
    'ESSENCE_DRAGON': '<:ESSENCE_DRAGON:891699882845405224>',
    'ESSENCE_DIAMOND': '<:ESSENCE_DIAMOND:891699478715858964>'
};

function parsedMinionOptions(list) {
    let result = [];
    for (var key in list) {
        result.push(`[${key}] ${list[key]}`)
    }

    return result;
}

module.exports = {
    helpEmbed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setColor(BESTMINION_THEME_COLOR);
        embed.setTitle('**BestMinion\'s Commands**');
        embed.setThumbnail(Utils.getDefaultProfilePicture());

        let minionField = '';
        minionField += '►**craft**: Calculate minion price\n';
        minionField += '►**minion**: Advanced minions\' earning calculator\n';
        minionField += '►**top10**: Calculate 10 best minions right now, order by its earning\n';
        embed.addField('- Minion commands', minionField);

        let playerField = '';
        playerField += '►**dprofile**: Dungeon profile viewer\n';
        playerField += '►**essences**: Get player\'s essences\n'
        playerField += '►**link**: Link your minecraft account with BestMinion bot\n';
        playerField += '►**next**: Calculate 5 cheapest unique minions upgrade (Required account link)\n';
        playerField += '►**nextmax**: Calculate 5 cheapest unique minions max upgrade (Required account link)\n';
        playerField += '►**talisman**: Talisman related commands ( missing5, ... )';
        embed.addField('- Player commands', playerField);

        let micsField = '';
        micsField += '►**help** : Shows informations about BestMinion\n';
        micsField += '►**donate**: Support me ❤️, !supporter for perks\n';
        micsField += '►**about**: Show information about BestMinion\n';
        micsField += '►**skills**: Skills calculation\n';
        embed.addField('- Mics commands', micsField);

        return embed;
    },
    helpMinionEmbed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setTitle('**Command: /Minion**');
        embed.setColor(BESTMINION_THEME_COLOR);
        embed.setThumbnail(Utils.getDefaultProfilePicture());

        let minionDescription = '**Description:** Advanced minions\' earning calculator\n';
        minionDescription += '**Usage:** !minion [minion name] [tier] [slot] [upgrade1] [upgrade2]';
        minionDescription += ' [fuel] [storage] [?is afk: Yes/No] [?sell to: All/NPC/Bazaar]';
        minionDescription += ' [?bonus1] [?bonus2] [?bonus3]\n';
        minionDescription += '**Example:** !m voidling 11 30 15 14 9 5 Yes All 0 5 \n';
        embed.setDescription(minionDescription);

        let minionOptions = Utils.getMinionOptions();
        let upgradeField = parsedMinionOptions(minionOptions['upgrades']).join('\n');
        embed.addField(' - Upgrade', upgradeField, true);
        let fuelField = parsedMinionOptions(minionOptions['fuels']).join('\n');
        embed.addField(' - Fuel', fuelField, true);
        let storageField = parsedMinionOptions(minionOptions['storages']).join('\n');
        embed.addField(' - Storage', storageField, true);
        let bonus1Field = parsedMinionOptions(minionOptions['bonus1']).join('\n');
        embed.addField(' - Bonus 1 ( Crystal bonus )', bonus1Field, true);
        let bonus2Field = parsedMinionOptions(minionOptions['bonus2']).join('\n');
        embed.addField(' - Bonus 2 ( Beacon bonus )', bonus2Field, true);
        let bonus3Field = parsedMinionOptions(minionOptions['bonus3']).join('\n');
        embed.addField(' - Bonus 3 ( Pet bonus )', bonus3Field, true);

        return embed;
    },
    helpTop10Embed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setTitle('**Command: /Top10**');
        embed.setColor(BESTMINION_THEME_COLOR);

        let top10Description = '**Description:** Calculate 10 best minions right now, order by its earning\n';
        top10Description += '**Usage:** /top10 [1-12 or all] [?sell to: All/NPC/Bazaar] [?except]\n';
        top10Description += '**Example:** /top10 12 NPC tarantula';

        embed.setDescription(top10Description);
        return embed;
    },
    helpDprofileEmbed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setTitle('**Command: /Dprofile**');
        embed.setColor(BESTMINION_THEME_COLOR);

        let dpDescription = '**Description:** Checking skyblock dungeon profiles\n';
        dpDescription += '**Usage:** !dprofile [ign]\n';
        dpDescription += '**Example:** !dprofile FROGKung'

        embed.setDescription(dpDescription);
        return embed;
    },
    helpLinkEmbed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setTitle('**Command: /Link**');
        embed.setColor(BESTMINION_THEME_COLOR);

        let linkDescription = '**Description:** Link your minecraft account with BestMinion bot ( you don\'t need to link discord to your hypixel account )\n';
        linkDescription += '**Usage:** !link [ign]\n';
        linkDescription += '**Example:** !link FROGKung'

        embed.setDescription(linkDescription);
        return embed;
    },
    helpCraftEmbed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setTitle('**Command: /Craft**');
        embed.setColor(BESTMINION_THEME_COLOR);

        let linkDescription = '**Description:** Calculate minion price\n';
        linkDescription += '**Usage:** !craft [minion] [tier] [?from]\n';
        linkDescription += '**Example:** !craft voidling 6 3'

        embed.setDescription(linkDescription);
        return embed;
    },
    helpEssencesEmbed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setTitle('**Command: /Essences**');
        embed.setColor(BESTMINION_THEME_COLOR);

        let essencesDescription = '**Description:** Get player\'s essences\n';
        essencesDescription += '**Usage:** !essences [ign]\n';
        essencesDescription += '**Example:** !essences FROGKung'

        embed.setDescription(essencesDescription);
        return embed;
    },
    helpSkillsEmbed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setTitle('**Skills commands list**');
        embed.setColor(BESTMINION_THEME_COLOR);

        let helpDescription = '►**boost** : Calculate skills xp with boost\n';
        helpDescription += '►**invboost** : Convert boosted skill xp back to base\n';
        embed.setDescription(helpDescription);
        return embed;
    },
    helpTalismanEmbed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setTitle('**Talisman commands list**');
        embed.setColor(BESTMINION_THEME_COLOR);

        let helpDescription = '►**missing5** : Shows 5 cheapest missing talisman\n';
        embed.setDescription(helpDescription);
        return embed;
    },
    helpTalismanMissingEmbed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setTitle('**Talisman command: /Missing**');
        embed.setColor(BESTMINION_THEME_COLOR);

        let description = '**Description:** Get cheapest missing talisman (detailed)\n';
        description += '**Usage:** !talisman missing [ign]\n';
        description += '**Example:** !talisman m FROGKung'

        embed.setDescription(description);
        return embed;
    },
    helpTalismanMissing5Embed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setTitle('**Talisman command: /Missing5**');
        embed.setColor(BESTMINION_THEME_COLOR);

        let description = '**Description:** Get 5 cheapest missing talisman\n';
        description += '**Usage:** !talisman missing5 [ign]\n';
        description += '**Example:** !talisman m5 FROGKung'

        embed.setDescription(description);
        return embed;
    },
    aboutMeEmbed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setColor('#f8c9d3');
        embed.setThumbnail(Utils.getDefaultProfilePicture());
        embed.setTitle('About BestMinion bot');
        embed.setFooter('Bot made by Tonkaew#2345', 'https://cdn.discordapp.com/avatars/352448254304321537/c8f6a5c6461e2783c25161428522e03d.webp');
        embed.setTimestamp(Date.now());

        let description = `${BLANK_EMOJI}BestMinion is Hypixel Skyblock bot that can calculate`;
        description += ' specific minion or even all minion at once. It also has many QOL';
        description += ' features such as cheapest unqiue minion upgrade, dungeon profile viewer.\n\n';
        description += `Getting support about bot at`;
        description += `\n- ${DISCORD_INVITE}`;
        embed.setDescription(description);

        return embed;
    },
    directMessageWarningEmbed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setColor('#000000');
        embed.setThumbnail(Utils.getDefaultProfilePicture());
        embed.setTitle('BestMinion commands aren\'t allow in DM.');
        embed.setFooter('Bot made by Tonkaew#2345', 'https://cdn.discordapp.com/avatars/352448254304321537/c8f6a5c6461e2783c25161428522e03d.webp');
        embed.setTimestamp(Date.now());

        let description = `${BLANK_EMOJI}Only supporter can use BestMinion in DM right now,`;
        description += ' further more information check BestMinion Official Server';
        description += `\n- ${DISCORD_INVITE}`;
        embed.setDescription(description);

        return embed;
    },
    commandWarningEmbed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setColor('#000000');
        embed.setThumbnail(Utils.getDefaultProfilePicture());
        embed.setTitle('You aren\'t allow to use this feature/command');
        embed.setFooter('Bot made by Tonkaew#2345', 'https://cdn.discordapp.com/avatars/352448254304321537/c8f6a5c6461e2783c25161428522e03d.webp');
        embed.setTimestamp(Date.now());

        let description = 'Only supporter can use this feature';
        description += ' further more information check BestMinion Official Server';
        description += `\n- ${DISCORD_INVITE}`;
        embed.setDescription(description);

        return embed;
    },
    supporterPerksEmbed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setColor('#f96854');
        embed.setTitle('**Supporter\'s perks**');
        embed.setThumbnail('https://play-lh.googleusercontent.com/Na6tpXBhckELpKiT8y0rTE6iJeytOHszx3yBdPbVujrjD0uPrZlNq6CgdagSORdhaQ');
        embed.setFooter('Bot made by Tonkaew#2345', 'https://cdn.discordapp.com/avatars/352448254304321537/c8f6a5c6461e2783c25161428522e03d.webp');
        embed.setTimestamp(Date.now());

        let description = '- Use BestMinion commands in DM.\n';
        description += '- Talisman related commands ( !t missing5, ... ).\n'
        description += '- More to come in the future.'
        embed.setDescription(description);
        return embed;
    },
    errorEmbed: function (data) {
        let embed = new Discord.MessageEmbed();
        embed.setAuthor(`❌ ${data['cause']} ❌`, Utils.getDefaultProfilePicture())
        embed.setColor(BESTMINION_ERROR_COLOR);

        return embed;
    },
    fetchingEmbed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setAuthor('Fetching...', Utils.getDefaultProfilePicture())
        embed.setColor(BESTMINION_WAIT_COLOR);

        return embed;
    },
    calculatingEmbed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setAuthor('Calculating...', Utils.getDefaultProfilePicture())
        embed.setColor(BESTMINION_WAIT_COLOR);

        return embed;
    },
    linkedEmbed: function (data) {
        let embed = new Discord.MessageEmbed();
        embed.setAuthor(`✅ ${data['data']['name']}, linked to your discord!`, Utils.getDefaultProfilePicture());
        embed.setColor(BESTMINION_CORRECT_COLOR);

        return embed;
    },
    nextEmbed: function (data, user) {
        data = data['data'];

        let embed = new Discord.MessageEmbed();
        embed.setAuthor(`Top 5 Cheapest upgrades ( ${data['profile_name']} ) ${data['warning']}`, data['skin_head']);
        embed.setColor(BESTMINION_THEME_COLOR);
        embed.setFooter('Latest updated at', user.avatarURL())
        embed.setTimestamp(new Date(data['timestamp']).toISOString());

        if (data['minions'].length == 0) {
            embed.setAuthor(`🎉🎉 Congratulations! 🎉🎉 ${data['warning']}`, data['skin_head']);
            embed.setThumbnail(data['skin_head']);
            embed.setDescription('You have crafted all minions in the game!!');

            return embed;
        }

        if (data['warning2'] != '') {
            embed.addField('**❌ Warning! ❌**', `- ${data['warning2']}`);
        }

        for (let i = 0; i < data['minions'].length; i++) {
            if (i == 5) break;
            let currentMinion = data['minions'][i];

            let formattedName = `${currentMinion['name']} ( ${Utils.formattedCurrency(currentMinion['total'])} )`;
            let fieldName = `${i + 1}. ${formattedName}`;

            let fieldValue = `- [Wiki link](${currentMinion['pictures']['wiki_link']})\n`;
            for (let j = 0; j < currentMinion['items'].length; j++) {
                fieldValue += `- ${currentMinion['items'][j]['name'] == 'Coins' ? Utils.formattedCurrency(currentMinion['items'][j]['amount'])
                    : `${currentMinion['items'][j]['amount']} x ${currentMinion['items'][j]['name']}`}`;

                if (currentMinion['items'][j]['name'] != 'Coins' && currentMinion['items'][j]['price'] != 0) {
                    fieldValue += ` ( ${Utils.formattedCurrency(currentMinion['items'][j]['price'])} )`;
                }

                fieldValue += '\n';
            }

            embed.addField(fieldName, fieldValue);
        }

        return embed;
    },
    nextMaxEmbed: function (data, user) {
        data = data['data'];

        let embed = new Discord.MessageEmbed();
        embed.setAuthor(`Top 5 Cheapest max upgrades ( ${data['profile_name']} ) ${data['warning']}`, data['skin_head']);
        embed.setColor(BESTMINION_THEME_COLOR);
        embed.setFooter('Latest updated at', user.avatarURL())
        embed.setTimestamp(new Date(data['timestamp']).toISOString());

        if (data['minions'].length == 0) {
            embed.setAuthor(`🎉🎉 Congratulations! 🎉🎉 ${data['warning']}`, data['skin_head']);
            embed.setThumbnail(data['skin_head']);
            embed.setDescription('You have crafted and max all minions in the game!!');

            return embed;
        }

        if (data['warning2'] != '') {
            embed.addField('**❌ Warning! ❌**', `- ${data['warning2']}`);
        }

        for (let i = 0; i < data['minions'].length; i++) {
            if (i == 5) break;
            let currentMinion = data['minions'][i];

            let formattedName = `${currentMinion['formatted_name']} ( ${Utils.formattedCurrency(currentMinion['total_price'])} )`;
            let fieldName = `${i + 1}. ${formattedName}`;

            let fieldValue = `- [Wiki link](${currentMinion['wiki_link']})\n`;
            for (let j = 0; j < currentMinion['items'].length; j++) {
                fieldValue += `- ${currentMinion['items'][j]['name'] == 'Coins' ? Utils.formattedCurrency(currentMinion['items'][j]['amount'])
                    : `${currentMinion['items'][j]['amount']} x ${currentMinion['items'][j]['name']}`}`;

                if (currentMinion['items'][j]['name'] != 'Coins' && currentMinion['items'][j]['price'] != 0) {
                    fieldValue += ` ( ${Utils.formattedCurrency(currentMinion['items'][j]['price'])} )`;
                }

                fieldValue += '\n';
            }

            embed.addField(fieldName, fieldValue);
        }

        return embed;
    },
    skillsBoostHelpEmbed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setTitle('**Skills command: /Boost**');
        embed.setColor(BESTMINION_THEME_COLOR);

        let linkDescription = '**Description:** Calculate skills xp with boost\n';
        linkDescription += '**Usage:** !skill boost [xp] [booster]\n';
        linkDescription += '**Example:** !skill boost 4652.31 20+20+50'

        embed.setDescription(linkDescription);
        let boostField = `${MICS_EMOTES['GOD_POTION_2']}20%: God potion\n`;
        boostField += `${MICS_EMOTES['ENCHANTED_COOKIE']}20%: Booster Cookie\n`;
        boostField += `${MICS_EMOTES['MAYOR_DERPY']}50%: Mayor Derpy\n`;
        embed.addField(' - Booster', boostField, true);
        return embed;
    },
    skillsBoostEmbed: function (xp) {
        let embed = new Discord.MessageEmbed();
        embed.setTitle(`${xp} xp`);
        embed.setColor(BESTMINION_THEME_COLOR);

        return embed;
    },
    skillsInvertBoostHelpEmbed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setTitle('**Skills command: /Invboost**');
        embed.setColor(BESTMINION_THEME_COLOR);

        let helpDescription = '**Description:** Convert boosted skill xp back to base\n';
        helpDescription += '**Usage:** !skill invboost [xp] [booster]\n';
        helpDescription += '**Example:** !skill invboost 4652.31 20+20+50'

        embed.setDescription(helpDescription);
        let boostField = `${MICS_EMOTES['GOD_POTION_2']}20%: God potion\n`;
        boostField += `${MICS_EMOTES['ENCHANTED_COOKIE']}20%: Booster Cookie\n`;
        boostField += `${MICS_EMOTES['MAYOR_DERPY']}50%: Mayor Derpy\n`;
        embed.addField(' - Booster', boostField, true);
        return embed;
    },
    donateEmbed: function () {
        let embed = new Discord.MessageEmbed();
        embed.setAuthor('💰 Donate information', 'https://cdn.discordapp.com/attachments/600316093872996382/752854516419919923/LOGO_CO_accout.png');
        embed.setColor('#0d4d9c');
        embed.setDescription('**If you want to support my work, you can do that via**');

        embed.addField('** - Patreon (monthly)**', 'https://www.patreon.com/frogkung');
        embed.addField('** - Ko-fi (one-time)**', 'https://ko-fi.com/frogkung');
        return embed;
    },
    essencesEmbed: function (data, user) {
        let embed = new Discord.MessageEmbed();
        embed.setAuthor(`${data['name']}'s Essences ( ${data['profile_name']} )`, data['head_pic']);
        embed.setFooter('Last online', user.avatarURL());
        embed.setTimestamp(new Date(data['timestamp']).toISOString());
        embed.setColor('#2c2c2c');

        if (Object.keys(data['essences']).length == 0) {
            embed.setDescription('No essences data found.');
            return embed;
        }

        for (let key in data['essences']) {
            let emoteName = `ESSENCE_${key.toUpperCase()}`;
            let emote = '';
            if (emoteName in MICS_EMOTES)
                emote = `${MICS_EMOTES[emoteName]} `;

            let fieldName = `${emote}${Utils.titled(key)} Essence`;
            embed.addField(fieldName, `- ${Utils.formattedNumber(data['essences'][key])}`);
        }
        return embed;
    },
    dprofileEmbed: function (data, user) {
        const classesImage = {
            'healer': 'https://www.minecraftguides.org/wp-content/uploads/2012/07/splashHeal.gif',
            'mage': 'https://art.pixilart.com/62cffc62286b132.png',
            'berserk': 'https://static.wikia.nocookie.net/minecraft_gamepedia/images/8/8e/Iron_Sword_JE2_BE2.png/revision/latest/scale-to-width-down/160?cb=20200217235910',
            'archer': 'https://cdn.discordapp.com/attachments/600316093872996382/831979613580034049/27-278841_bow-minecraft-bow-png.png',
            'tank': 'https://www.canteach.ca/minecraft-pe/images/leather_tunic.gif'
        };

        armoursField = '';
        let armours = data['data']['gears']['armours'];
        for (let key in armours) {
            armoursField += `- ${armours[key]}\n`;
        }

        itemsField = '';
        let items = data['data']['gears']['hotbar'];
        for (let key in items) {
            itemsField += `- ${items[key]}\n`;
        }

        floorsField = '';
        const floorsInfo = ['Entrance', 'Bonzo', 'Scarf', 'The Professor', 'Thorn', 'Livid', 'Sadan', 'Necron'];
        let floors = data['data']['floors'];
        let catacombsFloors = floors['catacombs'];
        let masterFloors = floors['master_catacombs'];
        for (let key in catacombsFloors['times_played']) {
            floorsField += `- ${!(key in catacombsFloors['tier_completions']) ? 0 : catacombsFloors['tier_completions'][key]}`;
            floorsField += `  ${floorsInfo[key]}`;
            floorsField += ` ( ${catacombsFloors['times_played'][key]} )\n`;
        }

        let masterModeField = ''
        for (let key in masterFloors['tier_completions']) {
            masterModeField += `- ${masterFloors['tier_completions'][key]} Master mode ${floorsInfo[key]}`;
            masterModeField += '\n';
        }

        let selectedClass = data['data']['classes']['selected_dungeon_class'];
        let classField = `- ${Utils.capitalized(selectedClass)}`;
        if (selectedClass != 'None') classField += ` ( Lv.${data['data']['classes'][selectedClass]} )`;

        let micsField = '';
        micsField += `\n- Highest Floor Beaten: ${data['data']['mics']['highest_floor']}`;
        micsField += `\n- Secrets Found: ${Utils.formattedNumber(data['data']['mics']['secrets_found'])}`;
        micsField += `\n- Journals Completed: ${data['data']['mics']['journals']}`;

        let embed = new Discord.MessageEmbed();
        embed.setAuthor(`${data['data']['name']}'s Dungeon profile`, data['data']['mics']['head_pic']);
        embed.setThumbnail(classesImage[selectedClass]);
        embed.setFooter('Last online', user.avatarURL());
        embed.setTimestamp(new Date(data['data']['timestamp']).toISOString());
        embed.setColor('#2c2c2c');

        embed.addField('Dungeons: ', `- The Catacombs ( Lv.${data['data']['catacombs']['lvl']} )` || 'API Disabled');
        embed.addField('Selected Class: ', classField || 'API Disabled');
        if (armoursField != '') embed.addField('Armour: ', armoursField);
        embed.addField('Pet: ', `- ${data['data']['gears']['pet']['formatted_name']}`)
        embed.addField('Items: ', itemsField || 'API Disabled');
        if (floorsField != '') embed.addField('Boss Collection: ', floorsField);
        if (masterModeField != '') embed.addField('Master Mode Collection: ', masterModeField);
        if (micsField != '') embed.addField('Miscellaneous: ', micsField);
        return embed;
    },
    minionEmbed: function (data, user) {
        let priceField = `From tier 1: **${Utils.formattedCurrency(data['data']['price']['all_tier']['total'])}**\n`;
        priceField += data['data']['tier'] == 1 ? '' : `From tier ${data['data']['tier'] - 1}: **${Utils.formattedCurrency(data['data']['price']['last_tier']['total'])}**`;

        let earningField = `1 Hour: **${Utils.formattedCurrency(data['data']['earnings']['per_hour'])}**`;
        earningField += `\n1 Day: **${Utils.formattedCurrency(data['data']['earnings']['per_day'])}**`;
        earningField += `\n1 Week: **${Utils.formattedCurrency(data['data']['earnings']['per_week'])}**`;

        let experiencesField = '';
        let index = 1;
        for (var key in data['data']['exp']) {
            let experienceType = key.toLowerCase();
            experienceType = experienceType.charAt(0).toUpperCase() + experienceType.slice(1);

            experiencesField += `${index}. ${experienceType} Exp\n`;
            experiencesField += `- 1 Hour: **${Utils.formattedNumber(data['data']['exp'][key]['per_hour'])}** xp\n`;
            experiencesField += `- 1 Day: **${Utils.formattedNumber(data['data']['exp'][key]['per_day'])}** xp\n`;
            experiencesField += `- 1 Week: **${Utils.formattedNumber(data['data']['exp'][key]['per_week'])}** xp\n`;
            index += 1;
        }

        let itemsField = '';
        for (var key in data['data']['items']) {
            let experienceType = data['data']['items'][key]['exp']['type'].toLowerCase();
            experienceType = experienceType.charAt(0).toUpperCase() + experienceType.slice(1);

            let itemAmount = data['data']['items'][key]['items_per_hour'];
            let itemUnit = 'hour';
            if (itemAmount < 1) {
                itemAmount *= 24;
                itemUnit = 'day';
                if (itemAmount < 1) {
                    itemAmount *= 7;
                    itemUnit = 'week';
                    if (itemAmount < 1) {
                        itemAmount *= 30;
                        itemUnit = 'month';
                    }
                }
            }

            itemsField += `${Number(key) + 1}. ${data['data']['items'][key]['item_name']} (${data['data']['items'][key]['sell_to']})\n`;
            itemsField += `- **${Utils.formattedNumber(itemAmount)}** items / ${itemUnit}\n`;
            itemsField += experienceType == '' ? '' : `- **${Utils.formattedNumber(data['data']['items'][key]['exp']['per_hour'])}** ${experienceType} xp / hour\n`;
        }

        let embed = new Discord.MessageEmbed();
        embed.setAuthor(data['data']['formatted_name'], data['data']['pictures']['head'], data['data']['pictures']['wiki_link']);
        embed.setColor(data['data']['pictures']['color']);
        embed.setFooter(`Requested by ${user['username']}`, user.avatarURL());
        embed.setThumbnail(data['data']['pictures']['full']);
        embed.setTimestamp(new Date(data['data']['timestamp']).toISOString());

        embed.addField('- Price', priceField);
        embed.addField('- Earning', earningField);
        if (experiencesField != '') embed.addField('- Experiences', experiencesField);
        if (itemsField != '') embed.addField('- Items', itemsField);
        if (data['data']['fuel']['name'] != 'None') embed.addField('- Fuel', `${data['data']['fuel']['name']} - ${data['data']['fuel']['description']}`);
        embed.addField(`- Storage (${data['data']['storage']['slots']} slots)`, `${data['data']['storage']['type']} - ${Utils.secondsToString(data['data']['storage']['hour_until_full'] * 60 * 60)}`);

        return embed;
    },
    top10Embed: function (data, user, exceptMinion) {
        let tierName = data['data']['tier'] == 'All' ? ` - All tiers (${data['data']['sell_to']})` :
            ` - Tier ${data['data']['tier']} (${data['data']['sell_to']})`;

        let except = exceptMinion == undefined ? '' : exceptMinion;
        except = except.toLowerCase();
        except = except.replace(' Minion', '');
        except = `${except.charAt(0).toUpperCase() + except.slice(1)} Minion`;

        tierName += exceptMinion == undefined ? '' : ` (except **${except}**)`;
        let minions = data['data']['minions'].filter(m => m.name != except);
        let minionField = '';
        for (m in minions.slice(0, 10)) {
            minionField += `${Number(m) + 1}. ${minions[m]['formatted_name']} - ${Utils.formattedCurrency(minions[m]['earning_per_hour'])}\n`;
        }

        let embed = new Discord.MessageEmbed();
        embed.setAuthor('Top 10 minions', Utils.getDefaultProfilePicture());
        embed.setColor(BESTMINION_THEME_COLOR);
        embed.addField(tierName, minionField);
        embed.setFooter(`Requested by ${user['username']}`, user.avatarURL());
        embed.setTimestamp(new Date(data['data']['timestamp']).toISOString());

        return embed;
    },
    talismanMissing5Embed(data, user) {
        talismanData = data['data'];

        let embed = new Discord.MessageEmbed();
        embed.setAuthor(`Top 5 Cheapest missing talismans ( ${talismanData['profile_name']} )`, talismanData['skin_head']);
        embed.setColor(BESTMINION_THEME_COLOR);
        embed.setFooter('Latest updated at', user.avatarURL())
        embed.setTimestamp(new Date(talismanData['timestamp']).toISOString());

        if (talismanData['missing_talismans'].length == 0) {
            embed.setAuthor(`🎉🎉 Congratulations! 🎉🎉`, talismanData['skin_head']);
            embed.setThumbnail(talismanData['skin_head']);

            let description = 'You have all talismans in the game!!';
            description += '\n\n*warning - ';
            let warnings = [];
            for (let i = 0; i < data['warning'].length; i++) {
                if (data['warning'][i] == '') continue;
                warnings.push(`\`${data['warning'][i]}\``);
            }
            description += warnings.join(', ');
            embed.setDescription(description);

            return embed;
        }

        for (let i = 0; i < talismanData['missing_talismans'].length; i++) {
            if (i == 5) break;
            let currentTalisman = talismanData['missing_talismans'][i];

            let priceField = Utils.formattedCurrency(currentTalisman['total_price']);
            if (currentTalisman['total_price'] == 0) {
                priceField = 'Free';
            }

            let formattedName = `${Utils.titled(currentTalisman['name'].split('_').join(' '))} ( ${priceField} )`;
            let fieldName = `${i + 1}. ${formattedName}`;

            let fieldValue = `- From **${currentTalisman['type']}**\n`;

            if (currentTalisman['type'] == 'npc') {
                fieldValue = `- From **[${currentTalisman['npc']}](${currentTalisman['wiki']}) NPC**`;
            }

            if (currentTalisman['type'] == 'npc trading') {
                fieldValue = `- From **[${currentTalisman['npc']}](${currentTalisman['wiki']}) NPC Trading**\n`;
            }

            if (currentTalisman['type'] == 'Quest') {
                fieldValue = `- From [**Quest**](${currentTalisman['wiki']}): ${currentTalisman['description']}`;
            }

            if (currentTalisman['type'] == 'Crafting' || currentTalisman['type'] == 'Forging' || currentTalisman['type'] == 'npc trading') {
                for (let k = 0; k < currentTalisman['items'].length; k++) {
                    let currentItem = currentTalisman['items'][k];
                    fieldValue += `${BLANK_EMOJI}- **${currentItem['amount']}** x ${Utils.titled(currentItem['name'].split('_').join(' '))}`;
                    if (currentItem['total_price'] != 0) {
                        fieldValue += ` ( **${Utils.formattedCurrency(currentItem['total_price'])}** )`;
                    }

                    fieldValue += '\n';
                }
            }

            if (i == 4 || i == talismanData['missing_talismans'].length - 1) {
                fieldValue += '\n*warning - ';
                let warnings = [];
                for (let j = 0; j < data['warning'].length; j++) {
                    if (data['warning'][j] == '') continue;
                    warnings.push(`\`${data['warning'][j]}\``);
                }
                fieldValue += warnings.join(', ');
            }

            embed.addField(fieldName, fieldValue);
        }

        return embed;
    },
    craftEmbed: function (data, user) {
        let embed = new Discord.MessageEmbed();
        embed.setAuthor(`${data['data']['formatted_name']} Recipe ${data['warning'] == '' ? '' : ` ( ${data['warning']} )`}`, Utils.getDefaultProfilePicture());
        embed.setColor(BESTMINION_THEME_COLOR);
        embed.setFooter(`Requested by ${user['username']}`, user.avatarURL());
        embed.setTimestamp(Date.now());

        let totalCoins = 0;
        for (var key in data['data']['materials']) {
            let currentMaterials = data['data']['materials'][key];
            let fieldValue = '';
            for (var item in currentMaterials['items']) {
                let currentItem = currentMaterials['items'][item];

                fieldValue += `- ${currentItem['amount']} x ${currentItem['name']}`;
                if (currentItem['price'] != undefined && currentItem['price'] != 0) fieldValue += ` ( ${Utils.formattedCurrency(currentItem['price'])} )`;
                fieldValue += '\n';

                if (currentItem['name'].includes('Minion')) {
                    for (var item2 in currentItem['items']) {
                        let minionItem = currentItem['items'][item2];

                        fieldValue += `${BLANK_EMOJI}- ${minionItem['amount']} x ${Utils.titled(minionItem['name'].split('_').join(' '))}`;
                        if (minionItem['price'] != undefined && minionItem['price'] != 0) fieldValue += ` ( ${Utils.formattedCurrency(minionItem['price'])} )`;
                        fieldValue += '\n';
                    }
                }

                if (currentItem['name'] == 'Coins') fieldValue = ` - ${Utils.formattedCurrency(currentItem['amount'])}`;
            }

            let fieldName = `Tier ${key}`;
            totalCoins += currentMaterials['total_price'];
            if (currentMaterials['total_price'] != 0) fieldName += ` - ${Utils.formattedCurrency(currentMaterials['total_price'])}`;
            if (totalCoins != 0 && totalCoins != currentMaterials['total_price']) fieldName += ` ( ${Utils.formattedCurrency(totalCoins)} )`;
            embed.addField(fieldName, fieldValue);
        }
        return embed;
    }
}