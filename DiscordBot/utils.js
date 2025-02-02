module.exports = {
    isDatabaseExist: function (database, path) {
        try {
            var data = database.getData(path);
            return true;
        } catch (error) {
            return false;
        }
    },
    hasRank: function (client, guildsDB, userID, rankName) {
        if (client == undefined) return false;
        if (guildsDB == undefined) return false;
        if (userID == '' || userID == undefined) return false;
        if (rankName == '' || rankName == undefined) return false;

        if (!this.isDatabaseExist(guildsDB, `/bot/roles/${rankName}`)) return false;
        let roleData = guildsDB.getData(`/bot/roles/${rankName}`);
        let guild = client.guilds.cache.get(roleData['guild_id']);
        if (guild == undefined) return false;

        // not in BestMinion lmao
        let member = guild.members.cache.get(userID);
        if (member == undefined) return;

        let roleID = roleData['role_id'];
        if (member.roles.cache.find(r => r.id === roleID) != undefined) return true;

        return false;
    },
    parsedIntColorCode: function (color) {
        if (color == undefined) return (parseInt('#f9eb45', 16));
        if (color == null) return (parseInt('#f9eb45', 16));

        color = color.replace('#', '0x');
        return (parseInt(color, 16));
    },
    getDefaultProfilePicture: function () {
        return 'https://vignette.wikia.nocookie.net/hypixel-skyblock/images/1/13/Wheat_Minion_I.png/revision/latest/scale-to-width-down/310?cb=20190724144437';
    },
    formattedCurrency: function (number) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(number)
    },
    formattedNumber: function (number) {
        let fractionDigits = 0;
        if (number % 1 != 0) {
            fractionDigits = number <= 0.01 ? 5 : 2;
        }
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: fractionDigits,
        }).format(number).substring(1);
    },
    parsedJsonEmbed: function (embed) {
        return {
            tts: false,
            embeds: [embed.toJSON()]
        }
    },
    capitalized: function (str) {
        if (typeof str !== 'string') return '';
        return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
    },
    titled: function (str) {
        let strList = str.split(' ');
        let result = [];
        for (let i = 0; i < strList.length; i++) {
            result.push(this.capitalized(strList[i]));
        }
        return result.join(' ');
    },
    getMinionOptions: function () {
        let minionOptions = {
            upgrades: [
                'None',
                'Compactor',
                'Super Compactor 3000',
                'Dwarven Super Compactor',
                'Diamond Spreading',
                'Potato Spreading',
                'Krampus Helmet',
                'Enchanted Egg',
                'Lesser Soulflow Engine',
                'Soulflow Engine',
                'Auto Smelter',
                'Budget Hopper',
                'Enchanted Hopper',
                'Flint Shovel',
                'Flycatcher',
                'Minion Expander'
            ],
            fuels: [
                'None',
                'Coal',
                'Block of Coal',
                'Enchanted Bread',
                'Enchanted Coal',
                'Enchanted Charcoal',
                'Solar Panel',
                'Enchanted Lava Bucket',
                'Magma Bucket',
                'Plasman Bucket',
                'Hamster Wheel',
                'Foul Flesh',
                'Catalyst',
                'Hyper Catalyst'
            ],
            storages: [
                'None',
                'Small Storage',
                'Medium Storage',
                'Large Storage',
                'X-Large Storage',
                'XX-Large Storage'
            ],
            bonus1: [
                'None',
                'Farm Crystal',
                'Mithril Crystal',
                'Woodcutting Crystal'
            ],
            bonus2: [
                'None',
                'Beacon I',
                'Beacon II',
                'Beacon III',
                'Beacon IV',
                'Beacon V',
            ],
            bonus3: [
                'None',
                'Legendary Rabbit Pet Lv. 100',
                'Legendary Ocelot Pet Lv. 100',
                'Legendary Magma Cube Pet Lv. 100',
                'Legendary Spider Pet Lv. 100',
                'Legendary Chicken Pet Lv. 100'
            ]
        };

        return minionOptions;
    },
    secondsToString: function (seconds) {
        var numyears = Math.floor(seconds / 31536000);
        var numdays = Math.floor((seconds % 31536000) / 86400);
        var numhours = Math.floor(((seconds % 31536000) % 86400) / 3600);
        var numminutes = Math.floor((((seconds % 31536000) % 86400) % 3600) / 60);
        var numseconds = (((seconds % 31536000) % 86400) % 3600) % 60;

        var output = 'Full in ';
        if(numyears != 0) output += `**${numyears}** years`;
        if(numdays != 0) output += ` **${numdays}** days`;
        if(numhours != 0) output += ` **${numhours}** hours`;
        if(numminutes != 0) output += ` **${numminutes}** minutes`;
        var roundedSecond = Math.round(numseconds);
        if(output == 'Full in ' && roundedSecond == 0) {
            return '**Full immediately!**';
        }
        
        output += ` **${Math.round(numseconds)}** seconds`;
        return output;
    }
}