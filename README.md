# rss2gemini

## Requirements
python3 <br/>
pip <br/>

## Additional Python Libraries
pip3 install html2text <br/>
pip3 install feedparser <br/>
pip3 install configparser <br/>
pip3 install bs4 <br/>

## Config Files
There are two config files, _config.ini_ and _server.ini_ <br/>
**config.ini format** <br/>
[RSSFEEDNAME] <br/>
feedtitle = _Title of the feed_ <br/>
url = _http url of the rss feed_ <br/>
modified = _leave this section blank_ <br/>

<br/>

**server.ini format** <br/>
[SERVERINFO] <br/>
#The base directory for your Gemini content <br/>
basedir = /gemini/base/directory/ <br/>
feeddir = feeds/ <br/>
#sleeptime in seconds (time is divided by the number of feed entries to avoid spamming servers) <br/>
sleeptime = 3600 <br/>
home = gemini://gemini.address.com <br/>
