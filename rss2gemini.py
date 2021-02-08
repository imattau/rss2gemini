from time import sleep
import asyncio

from html2text import HTML2Text
import feedparser
from bs4 import BeautifulSoup
from configparser import ConfigParser

feedCfg = ConfigParser()
feedCfg.read('config.ini')

serverCfg = ConfigParser()
serverCfg.read('server.ini')

contentdir = serverCfg['SERVERINFO']['basedir']
feeddir = serverCfg['SERVERINFO']['feeddir']


'''
def cleanDate(mDate):
    mDate.replace(",","-")
    mDate.replace(" ", "-")
    mDate.replace(":", "-")
    return mDate
'''

def buildEntry(title, htmlarticle, link):
    title = "## " + title
    link = "=> " + link
    h = HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    article = h.handle(htmlarticle)
    
    entry = "\n" + title + "\n" + article + "\n" + link + "\n"
    
    return entry

def createGMIFile(gmiEntry, rssname, feedcount):
    filename = contentdir + feeddir + rssname + ".gmi"
    
    if feedcount >= 20:
        with open(filename, 'w') as writer:
            writer.write(gmiEntry)
            print('File Updated')
        feedcount = 0
        return feedcount
    elif feedcount < 20:
        with open(filename, 'e') as writer:
            writer.write(gmiEntry)
            print('File Updated')
        return feedcount
        
      
    

def updateIndex():
    indexFile = contentdir + feeddir + 'index.gmi'

    with open(indexFile, 'w') as header:
        header.write('## RSS Feeds \n')
        header.write("=> " + serverCfg['SERVERINFO']['home'] + " << Home >> \n")

    for item in feedCfg.sections():
        link = "=> " + item + '.gmi ' + feedCfg[item]['feedtitle'] + " Updated: " + feedCfg[item]['modified'] + "\n"
        with open(indexFile, 'a') as update:
            update.write(link)

async def rss2text():
    

    for fn in feedCfg.sections():
        print(fn)
        feedcount = 0
        if feedCfg[fn]['modified'] == "":
            feed = feedparser.parse(feedCfg[fn]['url'])
            feedCfg[fn]['modified'] = feed.modified
            print(feedCfg[fn]['modified'])
            with open('config.ini', 'w') as cfgWriter:
                feedCfg.write(cfgWriter)
            
            

            for entry in feed.entries:
                feedcount += 1
                title = entry.title
                htmlarticle = ""
                link = entry.link
                if 'content' in entry:
                    htmlarticle = BeautifulSoup(entry.content[0].value, "html5lib").prettify()
                    #print(htmlarticle) 
                elif 'description' in entry:
                    htmlarticle = BeautifulSoup(entry.description, "html5lib").prettify()
                    #print('Has description')
                #Build up the GMI file entry with the correct formatting
                gmiEntry = buildEntry(title, htmlarticle, link)
                
                createGMIFile(gmiEntry, fn, feed.modified)
                
        else:
            feed = feedparser.parse(feedCfg[fn]['url'], modified=feedCfg[fn]['modified'])
               
            if feed == {}:
                print('No new feed items')
                #Do nothing as the feed has not been updated
                continue
            elif hasattr(feed, 'modified') and feed.modified < feedCfg[fn]['modified']:
                for entry in feed.entries:
                
                    title = entry.title
                    htmlarticle = ""
                    link = entry.link
                    if 'content' in entry:
                        htmlarticle = BeautifulSoup(entry.content[0].value, "html5lib").prettify()
                        #print(htmlarticle) 
                    elif 'description' in entry:
                        htmlarticle = BeautifulSoup(entry.description, "html5lib").prettify()
                        #print('Has description')
                    #Build up the GMI file entry with the correct formatting
                    gmiEntry = buildEntry(title, htmlarticle, link)
                    
                    feedcount = createGMIFile(gmiEntry, fn, feedcount)
        updateIndex()                    
        sleeptime = int(serverCfg['SERVERINFO']['sleeptime']) / len(feedCfg.items())
        print('Sleeping for ', sleeptime)
        await asyncio.sleep(sleeptime)
        asyncio.ensure_future(rss2text())
        
async def main():
    await rss2text()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(main())
    loop.run_forever()
    