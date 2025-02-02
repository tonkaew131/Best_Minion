const request = require('request');

require('dotenv').config();
const developingMode = process.env.DEV_MODE== 'true' ? true : false;
const applicationID = process.env.APPLICATION_ID;

module.exports = {
    responseInteraction: function (interactionID, interactionToken, data) {
        let url = `https://discord.com/api/v8/interactions/${interactionID}/${interactionToken}/callback`;
        let options = {
            method: 'POST',
            url: url,
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify({
                type: 4,
                data: data
            })
        }

        request(options, function (error, response, body) {
            if (error) {
                console.error(error);
            }

            if (developingMode) {
                console.log(response.statusCode);
                console.log(body);
            }
        });
    },
    editResponseInteraction: function (interactionToken, data) {
        let url = `https://discord.com/api/v8/webhooks/${applicationID}/${interactionToken}/messages/@original`;
        let options = {
            method: 'PATCH',
            url: url,
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify(data)
        }

        request(options, function (error, response, body) {
            if (error) {
                console.error(error);
            }

            if (developingMode) {
                console.log(response.statusCode)
                if (!(response.statusCode == 204 || response.statusCode == 200)) {
                    console.log(body);
                }
            }
        });
    },
    parseInteractionOptions: function(options) {
        if(options == undefined) return;
        let data = {};

        for(var key in options) {
            data[options[key]['name']] = options[key]['value'];
        }

        return data;
    }
}