const request = require('request');

const bestMinionAPIv2 = 'http://127.0.0.1:5001/api/v2/';

module.exports = {
    getBestMinionAPIv2: function (endpoint) {
        return new Promise(function (resolve, reject) {
            let url = bestMinionAPIv2 + endpoint;
            request(url, function (error, res, body) {
                if (!error && res.statusCode == 200) {
                    resolve(JSON.parse(body));
                } else {
                    let errorCause = 'There is problem talking to BestMinion APIv2⏰';

                    if (error != null && error.toString().includes('ECONNREFUSED')) errorCause = 'BestMinion APIv2 is offline⏰';

                    resolve({
                        success: false,
                        cause: errorCause
                    });
                }
            });
        })
    }
}