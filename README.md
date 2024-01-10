
# Twitch Chat Bot

Uses [twitchio](https://pypi.org/project/twitchio/).  


### Features so far
* Basic chat commands.


### Future Features
* [ ] Messages in response to PubSub events.


## Connecting to twitch via IRC with SSL
Get your oauth token [here](https://twitchapps.com/tmi/).
Example using `irssi`, with SSL enabled:
```lua
-- Server block
server = {
    address = "irc.chat.twitch.tv";
    chatnet = "twitch";
    port = "6697";
    password = "oauth:changeme";
    use_ssl = "yes";
    ssl_verify = "yes";
    autoconnect = "no";
}


-- Chatnet block
chatnets = {
    twitch = {
        type = "IRC";
        nick = "your_twitch_username";
    };
}

```
Use `/connect twitch` and `/disconnect twitch`.  
If you want to autoconnect, just set `autoconnect = "yes"`.
