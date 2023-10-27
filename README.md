
# Twitch Chat Bot

Using `[twitchio](https://pypi.org/project/twitchio/)`, this is my first attempt at creating a bot for my Twitch channel.


### Features so far:

* Basic chat commands.


### Features I want to add:

* [ ] Auto-thank anyone who follows channel
* [ ] Do the same for anyone who subscribes/cheers (when that's a thing for me)


### Current Roadblock:

400 Bad Request on webhook request. Reverse proxy was set up (using ngrox), however I spent quite a while trying to figure out why I was getting this response, trying different ports (Twitch API says to listen on port 443, reverse proxy is set to do that). 

The trainwreck that was my debugging attempt is on my [Twitch channel](https://www.twitch.tv/kolkhis) as a VOD.

