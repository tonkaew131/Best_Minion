const Discord = require('discord.js');
const client = new Discord.Client();

const InteractionUtils = require('./interaction');
const APIUtils = require('./api');
const Utils = require('./utils');

const Embeds = require('./embeds');

require('dotenv').config();
const developingMode = process.env.DEV_MODE == 'true' ? true : false;

const { JsonDB } = require('node-json-db');
const { Config } = require('node-json-db/dist/lib/JsonDBConfig');
const embeds = require('./embeds');
var GuildsDB = new JsonDB(new Config('./Database/Guilds_db.json', true, true, '/'));
var UsersDB = new JsonDB(new Config('./Database/Users_db.json', true, true, '/'));

client.on('ready', () => {
    let readyAt = client.readyAt.toLocaleString('en-US', {
        timeZone: 'Asia/Bangkok',
        hour12: false,
        weekday: 'long',
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric'
    });

    if (developingMode) {
        console.log('Running as Developing mode');
    }

    let logMessages = `Bot has started, with ${client.users.cache.size} users, in ${client.channels.cache.size} channels of ${client.guilds.cache.size} guilds. `;
    logMessages += `Ready at ${readyAt}`;
    console.log(logMessages);

    client.user.setActivity('🤔 !help', { type: 'LISTENING' });
});

client.on('error', () => {
    client.login(process.env.BOT_TOKEN)
});

client.on('raw', async data => {
    let eventType = data['t'];

    if (eventType === 'INTERACTION_CREATE') {
        let interactionID = data['d']['id'];
        let interactionToken = data['d']['token'];

        let guildID = data['d']['guild_id'];
        let channelID = data['d']['channel_id'];

        let user = data['d']['user'];
        if (user == undefined) user = data['d']['member']['user'];
        user = client.users.cache.get(user['id']);

        if (user == undefined) return;
        let isSupporter = Utils.hasRank(client, GuildsDB, user['id'], 'supporter');

        // if bot is running in developing environment
        if (developingMode) {
            // if dm
            if (guildID == undefined) return;

            let botData = GuildsDB.getData('/bot/environments/development');
            let allowedGuilds = botData['allowed_guilds'];

            if (allowedGuilds.length == 0) {
                console.log('[ERROR]: Developing environment must not run in every guild!');
                process.exit(1);
            }

            if (!allowedGuilds.includes(guildID)) return;
            if (Utils.isDatabaseExist(GuildsDB, `/guilds/${guildID}`)) {
                let guildData = GuildsDB.getData(`/guilds/${guildID}`);
                let allowedChannels = guildData['allowed_channels'];

                if (allowedChannels.length != 0 && !allowedChannels.includes(channelID)) return;
            } else {
                GuildsDB.push(`/guilds/${guildID}`, {
                    'allowed_channels': []
                }, true);
            }
        } else {
            if (guildID == undefined && !isSupporter) {
                let needSupporterEmbed = Utils.parsedJsonEmbed(Embeds.directMessageWarningEmbed());
                InteractionUtils.responseInteraction(interactionID, interactionToken, needSupporterEmbed);
                return;
            }

            if (guildID != undefined) {
                let botData = GuildsDB.getData('/bot/environments/production');
                let allowedGuilds = botData['allowed_guilds'];
                let blockedGuilds = botData['blocked_guilds'];

                if (blockedGuilds.includes(guildID)) return;

                // if there are allowed guilds, only allowed guild will work
                // else work every where
                if (allowedGuilds.length != 0 && !allowedGuilds.includes(guildID)) return;

                if (Utils.isDatabaseExist(GuildsDB, `/guilds/${guildID}`)) {
                    let guildData = GuildsDB.getData(`/guilds/${guildID}`);
                    let allowedChannels = guildData['allowed_channels'];

                    if (allowedChannels.length != 0 && !allowedChannels.includes(channelID)) return;
                } else {
                    GuildsDB.push(`/guilds/${guildID}`, {
                        'allowed_channels': []
                    }, true);
                }
            }
        }

        let command = data['d']['data']['name'].toLowerCase();

        // fully implemented
        if (command == 'help') {
            let commandOptions = InteractionUtils.parseInteractionOptions(data['d']['data']['options']);

            if (commandOptions == undefined) {
                let helpEmbed = Utils.parsedJsonEmbed(Embeds.helpEmbed());
                InteractionUtils.responseInteraction(interactionID, interactionToken, helpEmbed);
                return;
            }

            commandOptions = commandOptions['command'];
            if (commandOptions == 'minion') {
                InteractionUtils.responseInteraction(interactionID, interactionToken, {
                    tts: false,
                    content: 'https://cdn.discordapp.com/attachments/752859515119992832/839503105019740170/new_minion_command.mp4'
                });
                return;
            }
            if (commandOptions == 'top10') {
                let top10Embed = Utils.parsedJsonEmbed(Embeds.helpTop10Embed());
                InteractionUtils.responseInteraction(interactionID, interactionToken, top10Embed);
                return;
            }
            if (commandOptions == 'dprofile') {
                let dprofileEmbed = Utils.parsedJsonEmbed(Embeds.helpDprofileEmbed());
                InteractionUtils.responseInteraction(interactionID, interactionToken, dprofileEmbed);
                return;
            }
            if (commandOptions == 'link') {
                let linkEmbed = Utils.parsedJsonEmbed(Embeds.helpLinkEmbed());
                InteractionUtils.responseInteraction(interactionID, interactionToken, linkEmbed);
                return;
            }
            return;
        }

        // fully implemented
        if (command == 'donate') {
            let donateEmbed = Utils.parsedJsonEmbed(Embeds.donateEmbed());
            InteractionUtils.responseInteraction(interactionID, interactionToken, donateEmbed);
            return;
        }

        if (command == 'craft') {
            let commandOptions = InteractionUtils.parseInteractionOptions(data['d']['data']['options']);

            let calculatingEmbed = Utils.parsedJsonEmbed(Embeds.calculatingEmbed());
            InteractionUtils.responseInteraction(interactionID, interactionToken, calculatingEmbed);

            let endpoint = `minion/craft?minion_name=${commandOptions['minion']}`;
            endpoint += `&tier=${commandOptions['tier']}`;
            if (commandOptions['from'] != undefined) endpoint += `&from=${commandOptions['from']}`;

            let craftData = await APIUtils.getBestMinionAPIv2(endpoint);
            if (craftData['success'] == true) {
                let craftEmbed = Utils.parsedJsonEmbed(Embeds.craftEmbed(craftData, user));
                InteractionUtils.editResponseInteraction(interactionToken, craftEmbed);
                return;
            }

            let errorEmbed = Utils.parsedJsonEmbed(Embeds.errorEmbed(craftData));
            InteractionUtils.editResponseInteraction(interactionToken, errorEmbed);
            return;
        }

        // fully implemented
        if (command == 'dprofile') {
            let fetchingEmbed = Utils.parsedJsonEmbed(Embeds.fetchingEmbed());
            InteractionUtils.responseInteraction(interactionID, interactionToken, fetchingEmbed);

            let commandOptions = InteractionUtils.parseInteractionOptions(data['d']['data']['options']);

            let playerData = await APIUtils.getBestMinionAPIv2(`player/dungeonprofile?minecraft_ign=${commandOptions['ign']}`);
            if (playerData['success'] == true) {
                let dprofileEmbed = Utils.parsedJsonEmbed(Embeds.dprofileEmbed(playerData, user));
                InteractionUtils.editResponseInteraction(interactionToken, dprofileEmbed);
                return;
            }

            let errorEmbed = Utils.parsedJsonEmbed(Embeds.errorEmbed(playerData));
            InteractionUtils.editResponseInteraction(interactionToken, errorEmbed);
            return;
        }

        if (command == 'essence') {
            let fetchingEmbed = Utils.parsedJsonEmbed(Embeds.fetchingEmbed());
            InteractionUtils.responseInteraction(interactionID, interactionToken, fetchingEmbed);

            let commandOptions = InteractionUtils.parseInteractionOptions(data['d']['data']['options']);

            let playerData = await APIUtils.getBestMinionAPIv2(`player/essences?minecraft_ign=${commandOptions['ign']}`);
            if (playerData['success'] == true) {
                let essenceEmbed = Utils.parsedJsonEmbed(Embeds.essencesEmbed(playerData, user));
                InteractionUtils.editResponseInteraction(interactionToken, essenceEmbed);
                return;
            }

            let errorEmbed = Utils.parsedJsonEmbed(Embeds.errorEmbed(playerData));
            InteractionUtils.editResponseInteraction(interactionToken, errorEmbed);
            return;
        }

        // fully implemented
        if (command == 'link') {
            let fetchingEmbed = Utils.parsedJsonEmbed(Embeds.fetchingEmbed());
            InteractionUtils.responseInteraction(interactionID, interactionToken, fetchingEmbed);

            let commandOptions = InteractionUtils.parseInteractionOptions(data['d']['data']['options']);

            let uuid = await APIUtils.getBestMinionAPIv2(`player/getuuid?minecraft_ign=${commandOptions['ign']}`);
            if (uuid['success'] == true) {
                UsersDB.push(`/users/${user['id']}`, {
                    'uuid': uuid['data']['undashed_uuid']
                }, true);

                let linkedEmbed = Utils.parsedJsonEmbed(Embeds.linkedEmbed(uuid));
                InteractionUtils.editResponseInteraction(interactionToken, linkedEmbed);
                return;
            }

            let errorEmbed = Utils.parsedJsonEmbed(Embeds.errorEmbed(uuid));
            InteractionUtils.editResponseInteraction(interactionToken, errorEmbed);
            return;
        }

        // fully implemented
        if (command == 'minion') {
            let calculatingEmbed = Utils.parsedJsonEmbed(Embeds.calculatingEmbed());
            InteractionUtils.responseInteraction(interactionID, interactionToken, calculatingEmbed);

            let commandOptions = InteractionUtils.parseInteractionOptions(data['d']['data']['options']);

            let endpoint = 'minion/calculateminion?';
            commandOptions['minion'] == undefined ? '' : endpoint += `&minion_name=${commandOptions['minion']}`;
            commandOptions['tier'] == undefined ? '' : endpoint += `&minion_tier=${commandOptions['tier']}`;
            commandOptions['slot'] == undefined ? '' : endpoint += `&minion_slot=${commandOptions['slot']}`;
            commandOptions['upgrade1'] == undefined ? '' : endpoint += `&minion_upgrade1=${commandOptions['upgrade1']}`;
            commandOptions['upgrade2'] == undefined ? '' : endpoint += `&minion_upgrade2=${commandOptions['upgrade2']}`;
            commandOptions['fuel'] == undefined ? '' : endpoint += `&minion_fuel=${commandOptions['fuel']}`;
            commandOptions['storage'] == undefined ? '' : endpoint += `&minion_storage=${commandOptions['storage']}`;
            commandOptions['afk'] == undefined ? '' : endpoint += `&is_afk=${commandOptions['afk']}`;
            commandOptions['sell'] == undefined ? '' : endpoint += `&price_type=${commandOptions['sell']}`;
            commandOptions['bonus1'] == undefined ? '' : endpoint += `&minion_bonus1=${commandOptions['bonus1']}`;
            commandOptions['bonus2'] == undefined ? '' : endpoint += `&minion_bonus2=${commandOptions['bonus2']}`;
            commandOptions['bonus3'] == undefined ? '' : endpoint += `&minion_bonus3=${commandOptions['bonus3']}`;
            commandOptions['inferno_fuel'] == undefined ? '' : endpoint += `&inferno_fuel=${commandOptions['inferno_fuel']}`;

            let minionData = await APIUtils.getBestMinionAPIv2(endpoint);
            if (minionData['success'] == true) {
                let minionEmbed = Utils.parsedJsonEmbed(Embeds.minionEmbed(minionData, user));
                InteractionUtils.editResponseInteraction(interactionToken, minionEmbed);
                return;
            }

            let errorEmbed = Utils.parsedJsonEmbed(Embeds.errorEmbed(minionData));
            InteractionUtils.editResponseInteraction(interactionToken, errorEmbed);
            return;
        }

        // fully implemented
        if (command == 'next') {
            let fetchingEmbed = Utils.parsedJsonEmbed(Embeds.fetchingEmbed());
            InteractionUtils.responseInteraction(interactionID, interactionToken, fetchingEmbed);

            if (Utils.isDatabaseExist(UsersDB, `/users/${user['id']}`)) {
                let userData = UsersDB.getData(`/users/${user['id']}`);

                if (userData['uuid'] == undefined) {
                    let uuid = await APIUtils.getBestMinionAPIv2(`player/getuuid?minecraft_ign=${userData['ign']}`);

                    if (uuid['success'] == false) {
                        let errorCause = 'Your minecraft username have been changed!, make sure to link again';
                        let errorEmbed = Utils.parsedJsonEmbed(Embeds.errorEmbed({ cause: errorCause }));

                        InteractionUtils.editResponseInteraction(interactionToken, errorEmbed);
                        return;
                    }

                    userData['uuid'] = uuid['data']['undashed_uuid'];
                    UsersDB.push(`/users/${user['id']}`, {
                        'uuid': userData['uuid']
                    }, true);
                }

                let nextData = await APIUtils.getBestMinionAPIv2(`player/cheapestupgrade?&minecraft_uuid=${userData['uuid']}`);
                if (nextData['success'] == true) {
                    let nextEmbed = Utils.parsedJsonEmbed(Embeds.nextEmbed(nextData, user));
                    InteractionUtils.editResponseInteraction(interactionToken, nextEmbed);
                    return;
                }

                let errorEmbed = Utils.parsedJsonEmbed(Embeds.errorEmbed(nextData));
                InteractionUtils.editResponseInteraction(interactionToken, errorEmbed);
                return;
            }

            let errorCause = 'Your account haven\'t linked/verified with BestMinion bot!';
            let errorEmbed = Utils.parsedJsonEmbed(Embeds.errorEmbed({ cause: errorCause }));

            InteractionUtils.editResponseInteraction(interactionToken, errorEmbed);
            return;
        }

        if (command == 'nextmax') {
            let fetchingEmbed = Utils.parsedJsonEmbed(Embeds.fetchingEmbed());
            InteractionUtils.responseInteraction(interactionID, interactionToken, fetchingEmbed);

            if (Utils.isDatabaseExist(UsersDB, `/users/${user['id']}`)) {
                let userData = UsersDB.getData(`/users/${user['id']}`);

                if (userData['uuid'] == undefined) {
                    let uuid = await APIUtils.getBestMinionAPIv2(`player/getuuid?minecraft_ign=${userData['ign']}`);

                    if (uuid['success'] == false) {
                        let errorCause = 'Your minecraft username have been changed!, make sure to link again';
                        let errorEmbed = Utils.parsedJsonEmbed(Embeds.errorEmbed({ cause: errorCause }));

                        InteractionUtils.editResponseInteraction(interactionToken, errorEmbed);
                        return;
                    }

                    userData['uuid'] = uuid['data']['undashed_uuid'];
                    UsersDB.push(`/users/${user['id']}`, {
                        'uuid': userData['uuid']
                    }, true);
                }

                let nextMaxData = await APIUtils.getBestMinionAPIv2(`player/cheapestmax?&minecraft_uuid=${userData['uuid']}`);
                if (nextMaxData['success'] == true) {
                    let nextMaxEmbed = Utils.parsedJsonEmbed(Embeds.nextMaxEmbed(nextMaxData, user));
                    InteractionUtils.editResponseInteraction(interactionToken, nextMaxEmbed);
                    return;
                }

                let errorEmbed = Utils.parsedJsonEmbed(Embeds.errorEmbed(nextMaxData));
                InteractionUtils.editResponseInteraction(interactionToken, errorEmbed);
                return;
            }

            let errorCause = 'Your account haven\'t linked/verified with BestMinion bot!';
            let errorEmbed = Utils.parsedJsonEmbed(Embeds.errorEmbed({ cause: errorCause }));

            InteractionUtils.editResponseInteraction(interactionToken, errorEmbed);
            return;
        }

        // fully implemented
        if (command == 'top10') {
            let calculatingEmbed = Utils.parsedJsonEmbed(Embeds.calculatingEmbed());
            InteractionUtils.responseInteraction(interactionID, interactionToken, calculatingEmbed);

            let commandOptions = InteractionUtils.parseInteractionOptions(data['d']['data']['options']);

            let endpoint = 'minion/top10?';
            commandOptions['tier'] == undefined ? '' : endpoint += `&minion_tier=${commandOptions['tier']}`;
            commandOptions['sell'] == undefined ? '' : endpoint += `&price_type=${commandOptions['sell']}`;

            let top10Data = await APIUtils.getBestMinionAPIv2(endpoint);
            if (top10Data['success'] == true) {
                let top10Embed = Utils.parsedJsonEmbed(Embeds.top10Embed(top10Data, user, commandOptions['except']));
                InteractionUtils.editResponseInteraction(interactionToken, top10Embed);
                return;
            }

            let errorEmbed = Utils.parsedJsonEmbed(Embeds.errorEmbed(top10Data));
            InteractionUtils.editResponseInteraction(interactionToken, errorEmbed);
            return;
        }

        else {
            var fieldOptions = '';
            for (var key in data['d']['data']['options']) {
                fieldOptions += `\n- ${data['d']['data']['options'][key].name}: ${data['d']['data']['options'][key].value}`;
            }

            InteractionUtils.responseInteraction(interactionID, interactionToken, {
                tts: false,
                content: `[DEBUG]: Unsupported ${command} - ${fieldOptions}`
            })
        }
        return;
    }
});

client.on('message', async message => {
    let prefix = '!';

    if (message['author']['bot']) return;
    if (message['content'].indexOf(prefix) !== 0) return;

    const args = message.content.slice(prefix.length).trim().split(/ +/g);
    const command = args.shift().toLowerCase();

    let isSupporter = Utils.hasRank(client, GuildsDB, message['author']['id'], 'supporter');

    // if bot is running in developing environment
    if (developingMode) {
        // if dm
        if (message['guild'] == undefined) return;

        let botData = GuildsDB.getData('/bot/environments/development');
        let allowedGuilds = botData['allowed_guilds'];

        if (allowedGuilds.length == 0) {
            console.log('[ERROR]: Developing environment must not run in every guild!');
            process.exit(1);
        }

        if (!allowedGuilds.includes(message['guild']['id'])) return;
        if (Utils.isDatabaseExist(GuildsDB, `/guilds/${message['guild']['id']}`)) {
            let guildData = GuildsDB.getData(`/guilds/${message['guild']['id']}`);
            let allowedChannels = guildData['allowed_channels'];

            if (allowedChannels.length != 0 && !allowedChannels.includes(message['channel']['id'])) return;
        } else {
            GuildsDB.push(`/guilds/${message['guild']['id']}`, {
                'allowed_channels': []
            }, true);
        }
    } else {
        if (message['guild'] == undefined && !isSupporter) {
            let needSupporterEmbed = Embeds.directMessageWarningEmbed();
            return message['channel'].send(needSupporterEmbed);
        }

        if (message['guild'] != undefined) {
            let botData = GuildsDB.getData('/bot/environments/production');
            let allowedGuilds = botData['allowed_guilds'];
            let blockedGuilds = botData['blocked_guilds'];

            if (blockedGuilds.includes(message['guild']['id'])) return;

            // if there are allowed guilds, only allowed guild will work
            // else work every where
            if (allowedGuilds.length != 0 && !allowedGuilds.includes(message['guild']['id'])) return;

            if (Utils.isDatabaseExist(GuildsDB, `/guilds/${message['guild']['id']}`)) {
                let guildData = GuildsDB.getData(`/guilds/${message['guild']['id']}`);
                let allowedChannels = guildData['allowed_channels'];

                if (allowedChannels.length != 0 && !allowedChannels.includes(message['channel']['id'])) return;
            } else {
                GuildsDB.push(`/guilds/${message['guild']['id']}`, {
                    'allowed_channels': []
                }, true);
            }
        }
    }

    let channel = message['channel'];
    if (command == 'help') {
        if (args.length == 0) {
            channel.send(Embeds.helpEmbed());
            return;
        }

        if (args[0] == 'craft') {
            return channel.send(Embeds.helpCraftEmbed());
        }
        if (args[0] == 'minion' || args[0] == 'm') {
            return channel.send(Embeds.helpMinionEmbed());
        }
        if (args[0] == 'dprofile' || args[0] == 'dp') {
            return channel.send(Embeds.helpDprofileEmbed());
        }
        if (args[0] == 'link') {
            return channel.send(Embeds.helpLinkEmbed());
        }
        if (args[0] == 'talisman' || args[0] == 't') {
            return channel.send(embeds.helpTalismanEmbed());
        }
        if (args[0] == 'top10') {
            return channel.send(Embeds.helpTop10Embed());
        }
        return;
    }

    if (command == 'donate') {
        let donateEmbed = Embeds.donateEmbed();
        return channel.send(donateEmbed);
    }

    if (command == 'about') {
        return channel.send(Embeds.aboutMeEmbed());
    }

    if (command == 'craft') {
        if (args.length < 2) return channel.send(Embeds.helpCraftEmbed());

        let endpoint = `minion/craft?minion_name=${args[0].split('_').join(' ')}`;
        endpoint += `&tier=${args[1]}`;
        if (args[2] != undefined) endpoint += `&from=${args[2]}`;

        let craftData = await APIUtils.getBestMinionAPIv2(endpoint);
        if (craftData['success'] == true) {
            return channel.send(Embeds.craftEmbed(craftData, message['author']));
        }

        return channel.send(Embeds.errorEmbed(craftData));
    }

    if (command == 'dprofile' || command == 'dp') {
        if (args.length == 0) {
            let dprofileEmbed = Embeds.helpDprofileEmbed();
            return channel.send(dprofileEmbed);
        }

        let playerData = await APIUtils.getBestMinionAPIv2(`player/dungeonprofile?minecraft_ign=${args[0]}`);
        if (playerData['success'] == true) {
            let dprofileEmbed = Embeds.dprofileEmbed(playerData, message['author']);
            return channel.send(dprofileEmbed);
        }

        let errorEmbed = Embeds.errorEmbed(playerData);
        return channel.send(errorEmbed);
    }

    if (command == 'essence' || command == 'essences') {
        if (args.length == 0) {
            channel.send(Embeds.helpEssencesEmbed());
            return;
        }

        let essencesData = await APIUtils.getBestMinionAPIv2(`player/essences?minecraft_ign=${args[0]}`);
        if (essencesData['success'] == true) {
            channel.send(Embeds.essencesEmbed(essencesData, message['author']))
            return;
        }

        channel.send(Embeds.errorEmbed(essencesData));
    }

    if (command == 'link' || command == 'verify') {
        if (args.length == 0) {
            channel.send(Embeds.helpLinkEmbed());
            return;
        }

        let uuid = await APIUtils.getBestMinionAPIv2(`player/getuuid?minecraft_ign=${args[0]}`);
        if (uuid['success'] == true) {
            UsersDB.push(`/users/${message['author']['id']}`, {
                'uuid': uuid['data']['undashed_uuid']
            }, true);

            channel.send(Embeds.linkedEmbed(uuid));
            return;
        }

        channel.send(Embeds.errorEmbed(uuid));
        return;
    }

    if (command == 'minion' || command == 'm') {
        if (args[0] == 'help') {
            let minionEmbed = Embeds.helpMinionEmbed();
            return channel.send(minionEmbed);
        }

        if (args.length < 7) {
            let errorCause = 'Invalid minion options, please checkout more information\n';
            errorCause += 'in #rules-info at BestMinion Official Server discord.gg/yw9bNwR\n';
            errorCause += 'or do !m help ( it\'s really long! )';
            let errorEmbed = Embeds.errorEmbed({ cause: errorCause });
            return channel.send(errorEmbed);
        }

        let minionOptions = Utils.getMinionOptions();

        let endpoint = 'minion/calculateminion?';
        endpoint += `&minion_name=${args[0].split('_').join(' ')}`;
        endpoint += `&minion_tier=${args[1]}`;
        endpoint += `&minion_slot=${args[2]}`;
        endpoint += `&minion_upgrade1=${minionOptions['upgrades'][args[3]]}`;
        endpoint += `&minion_upgrade2=${minionOptions['upgrades'][args[4]]}`;
        endpoint += `&minion_fuel=${minionOptions['fuels'][args[5]]}`;
        endpoint += `&minion_storage=${minionOptions['storages'][args[6]]}`;

        if (args[7] != undefined) endpoint += `&is_afk=${args[7]}`;
        if (args[8] != undefined) endpoint += `&price_type=${args[8]}`;
        if (args[9] != undefined) endpoint += `&minion_bonus1=${minionOptions['bonus1'][args[9]]}`;
        if (args[10] != undefined) endpoint += `&minion_bonus2=${minionOptions['bonus2'][args[10]]}`;
        if (args[11] != undefined) endpoint += `&minion_bonus3=${minionOptions['bonus3'][args[11]]}`;

        let minionData = await APIUtils.getBestMinionAPIv2(endpoint);
        if (minionData['success'] == true) {
            let minionEmbed = Embeds.minionEmbed(minionData, message['author']);
            return channel.send(minionEmbed);
        }

        let errorEmbed = Embeds.errorEmbed(minionData);
        return channel.send(errorEmbed);
    }

    if (command == 'next') {
        if (Utils.isDatabaseExist(UsersDB, `/users/${message['author']['id']}`)) {
            let userData = UsersDB.getData(`/users/${message['author']['id']}`);

            if (userData['uuid'] == undefined) {
                let uuid = await APIUtils.getBestMinionAPIv2(`player/getuuid?minecraft_ign=${userData['ign']}`);

                if (uuid['success'] == false) {
                    let errorCause = 'Your minecraft username have been changed!, make sure to link again';
                    let errorEmbed = Embeds.errorEmbed({ cause: errorCause });

                    return channel.send(errorEmbed);
                }

                userData['uuid'] = uuid['data']['undashed_uuid'];
                UsersDB.push(`/users/${user['id']}`, {
                    'uuid': userData['uuid']
                }, true);
            }

            let nextData = await APIUtils.getBestMinionAPIv2(`player/cheapestupgrade?&minecraft_uuid=${userData['uuid']}`);
            if (nextData['success'] == true) {
                let nextEmbed = Embeds.nextEmbed(nextData, message['author']);
                return channel.send(nextEmbed);
            }

            let errorEmbed = Embeds.errorEmbed(nextData);
            return channel.send(errorEmbed);
        }

        let errorCause = 'Your account haven\'t linked/verified with BestMinion bot!';
        let errorEmbed = Embeds.errorEmbed({ cause: errorCause });
        return channel.send(errorEmbed);
    }

    if (command == 'nextmax' || command == 'nm') {
        if (Utils.isDatabaseExist(UsersDB, `/users/${message['author']['id']}`)) {
            let userData = UsersDB.getData(`/users/${message['author']['id']}`);

            if (userData['uuid'] == undefined) {
                let uuid = await APIUtils.getBestMinionAPIv2(`player/getuuid?minecraft_ign=${userData['ign']}`);

                if (uuid['success'] == false) {
                    let errorCause = 'Your minecraft username have been changed!, make sure to link again';
                    let errorEmbed = Embeds.errorEmbed({ cause: errorCause });

                    return channel.send(errorEmbed);
                }

                userData['uuid'] = uuid['data']['undashed_uuid'];
                UsersDB.push(`/users/${user['id']}`, {
                    'uuid': userData['uuid']
                }, true);
            }

            let nextMaxData = await APIUtils.getBestMinionAPIv2(`player/cheapestmax?&minecraft_uuid=${userData['uuid']}`);
            if (nextMaxData['success'] == true) {
                let nextMaxEmbed = Embeds.nextMaxEmbed(nextMaxData, message['author']);
                return channel.send(nextMaxEmbed);
            }

            let errorEmbed = Embeds.errorEmbed(nextMaxData);
            return channel.send(errorEmbed);
        }

        let errorCause = 'Your account haven\'t linked/verified with BestMinion bot!';
        let errorEmbed = Embeds.errorEmbed({ cause: errorCause });
        return channel.send(errorEmbed);
    }

    if (command == 'skills' || command == 'skill' || command == 's') {
        if (args[0] == undefined || args[0] == 'help') {
            return channel.send(Embeds.helpSkillsEmbed());
        }

        if (args[0] == 'boost') {
            if (args.length < 3 || args[1] == 'help') {
                return channel.send(Embeds.skillsBoostHelpEmbed());
            }

            let xp = Number(args[1].split(',').join(''));
            let booster = args[2].split('+');

            if (isNaN(xp)) {
                return channel.send(Embeds.errorEmbed({ cause: 'XP is not a number!' }));
            }
            if (booster.length == 0) {
                return channel.send(Embeds.skillsBoostHelpEmbed());
            }

            let multiplier = 1;
            for (let i = 0; i < booster.length; i++) {
                if (isNaN(booster[i])) {
                    return channel.send(Embeds.errorEmbed({ cause: 'Booster multiplier is not a number!' }));
                }

                multiplier += Number(booster[i]) / 100;
            }

            return channel.send(Embeds.skillsBoostEmbed(xp * multiplier));
        }

        if (args[0] == 'invboost') {
            if (args.length < 3 || args[1] == 'help') {
                return channel.send(Embeds.skillsInvertBoostHelpEmbed());
            }

            let xp = Number(args[1].split(',').join(''));
            let booster = args[2].split('+');

            if (isNaN(xp)) {
                return channel.send(Embeds.errorEmbed({ cause: 'XP is not a number!' }));
            }
            if (booster.length == 0) {
                return channel.send(Embeds.skillsInvertBoostHelpEmbed());
            }

            let multiplier = 1;
            for (let i = 0; i < booster.length; i++) {
                if (isNaN(booster[i])) {
                    return channel.send(Embeds.errorEmbed({ cause: 'Booster multiplier is not a number!' }));
                }

                multiplier += Number(booster[i]) / 100;
            }

            return channel.send(Embeds.skillsBoostEmbed(xp * (1 / multiplier)));
        }
    }

    if (command == 'talisman' || command == 't') {
        if (isSupporter == false && developingMode == false) {
            return channel.send(Embeds.commandWarningEmbed());
        }

        const subCommand = args[0];
        if (subCommand == undefined || subCommand == 'help') {
            return channel.send(Embeds.helpTalismanEmbed());
        }

        // if (subCommand == 'missing' || subCommand == 'm') {
        //     let ign = args[1];
        //     if (ign == undefined) {
        //         return channel.send(Embeds.helpTalismanMissingEmbed());
        //     }

        //     return;
        // }

        if (subCommand == 'missing5' || subCommand == 'm5') {
            if (Utils.isDatabaseExist(UsersDB, `/users/${message['author']['id']}`)) {
                let userData = UsersDB.getData(`/users/${message['author']['id']}`);

                if (userData['uuid'] == undefined) {
                    let uuid = await APIUtils.getBestMinionAPIv2(`player/getuuid?minecraft_ign=${userData['ign']}`);

                    if (uuid['success'] == false) {
                        let errorCause = 'Your minecraft username have been changed!, make sure to link again';
                        let errorEmbed = Embeds.errorEmbed({ cause: errorCause });

                        return channel.send(errorEmbed);
                    }

                    userData['uuid'] = uuid['data']['undashed_uuid'];
                    UsersDB.push(`/users/${user['id']}`, {
                        'uuid': userData['uuid']
                    }, true);
                }

                let talismanData = await APIUtils.getBestMinionAPIv2(`player/cheapesttalisman?&minecraft_uuid=${userData['uuid']}`);
                if (talismanData['success'] == true) {
                    let nextEmbed = Embeds.talismanMissing5Embed(talismanData, message['author']);
                    return channel.send(nextEmbed);
                }

                let errorEmbed = Embeds.errorEmbed(talismanData);
                return channel.send(errorEmbed);
            }

            let errorCause = 'Your account haven\'t linked/verified with BestMinion bot!';
            let errorEmbed = Embeds.errorEmbed({ cause: errorCause });
            return channel.send(errorEmbed);
        }

        return;
    }

    if (command == 'top10' || command == 't10') {
        if (args.length == 0) {
            let top10Embed = Embeds.helpTop10Embed();
            return channel.send(top10Embed);
        }

        let endpoint = 'minion/top10?';
        endpoint += `&minion_tier=${args[0]}`;
        if (args[1] != undefined) endpoint += `&price_type=${args[1]}`;

        let top10Data = await APIUtils.getBestMinionAPIv2(endpoint);
        if (top10Data['success'] == true) {
            let top10Embed = Embeds.top10Embed(top10Data, message['author'], args[2]);
            return channel.send(top10Embed);
        }

        let errorEmbed = Embeds.errorEmbed(top10Data);
        return channel.send(errorEmbed);
    }

    if (command == 'supporter') {
        let supporterPerksEmbed = Embeds.supporterPerksEmbed();
        return channel.send(supporterPerksEmbed);
    }

    if (command == 'star') {
        return channel.send('```✪```');
    }
});

client.login(process.env.BOT_TOKEN);