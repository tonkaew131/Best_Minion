const request = require('request');
require('dotenv').config();

const COMMANDS = require('./commands.json')['Commands'];
const DISCORD_API = 'https://discord.com/api/v9';

const GLOBAL_MODE = true;
// if true, commands will available to all guilds.

function get(url, method, requestBody) {
    return new Promise(function (resolve, reject) {
        let requestOptions = {
            method: method,
            url: url,
            headers: {
                'Authorization': `Bot ${process.env.BOT_TOKEN}`,
                'content-type': 'application/json'
            }
        }

        if (requestBody) requestOptions['body'] = JSON.stringify(requestBody);

        request(requestOptions, function (error, res, body) {
            if (!error && (res.statusCode >= 200 && res.statusCode < 300)) {
                let data = {};
                try {
                    data = JSON.parse(body);
                } catch (error) {
                    throw error;
                }

                resolve({
                    success: true,
                    data: data
                });
            } else {
                let statusCode = ` ${res?.statusCode}` || '';
                let cause = '';
                try {
                    let result = JSON.parse(body);
                    if ('message' in result) cause = result['message'];
                    else cause = `Unknown error${statusCode}`;
                } catch (error) {
                    cause = `Unknown error${statusCode}`;
                    throw error;
                }

                resolve({
                    success: false,
                    cause: cause
                });
            }
        });
    })
}

async function getCommands() {
    let applicationID = process.env.APPLICATION_ID;
    let guildID = process.env.GUILD_ID;

    let url = `${DISCORD_API}/applications/${applicationID}`;
    if (GLOBAL_MODE) {
        url += `/commands`;
    } else {
        url += `/guilds/${guildID}/commands`;
    }

    let result = await get(url, 'GET', undefined);
    if (result['success'] == true) {
        console.log(GLOBAL_MODE ? 'Global commands' : 'Guild commands');
        if (result['data'].length == 0) {
            console.log('- EMPTY -');
            return;
        }

        for (let i = 0; i < result['data'].length; i++) {
            let currentCommand = result['data'][i];
            console.log(`- ${currentCommand['name']}: ${currentCommand['id']}`);
        }

        return;
    }

    console.log(`Failed to get commands! ${result['cause']}`);
}

async function createCommand(name) {
    let applicationID = process.env.APPLICATION_ID;
    let guildID = process.env.GUILD_ID;

    let url = `${DISCORD_API}/applications/${applicationID}`;
    if (GLOBAL_MODE) {
        url += `/commands`;
    } else {
        url += `/guilds/${guildID}/commands`;
    }

    let data = {};
    if (name in COMMANDS) data = COMMANDS[name];
    else {
        console.log(`Command ${name} not found!`);
        return;
    }

    let result = await get(url, 'POST', data);
    if (result['success'] == true) {
        console.log(`Command ${result['data']['name']} created!: ${result['data']['id']}`);
        return;
    }

    console.log(`Failed to create command ${name}`);
    console.log(result);
}

async function deleteCommand(id) {
    let applicationID = process.env.APPLICATION_ID;
    let guildID = process.env.GUILD_ID;

    let url = `${DISCORD_API}/applications/${applicationID}`;
    if (GLOBAL_MODE) {
        url += `/commands/${id}`;
    } else {
        url += `/guilds/${guildID}/commands/${id}`;
    }

    let result = await get(url, 'DELETE', undefined);
    if (result['success'] == true) {
        console.log(`Command ${id} deleted!`);
        return;
    }

    console.log(`Failed to delete command ${id}`);
    console.log(result);
}

// getCommands();
createCommand('minion');
// deleteCommand('992399407943270490');