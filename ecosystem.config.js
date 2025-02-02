module.exports = {
  apps: [{
    name: "Discord bot",
    script: "./DiscordBot/bot.js",
    node_args: '-r dotenv/config',
  }, {
    name: "API v2",
    script: "./API/handleAPIv2.py",
    interpreter: "/usr/bin/python3",
    env: {
      "FLASK_APP": "handleAPIv2.py",
    }
  }]
};