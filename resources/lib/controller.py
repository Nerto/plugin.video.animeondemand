import json
import requests
import sys
from bs4 import BeautifulSoup

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
from . import view
from . import util

def showTop10(args):
    page = requests.get(args._baseUrl)
    soup = BeautifulSoup(page.content, 'html.parser')
    top10List = soup.findAll("div", {"class": "jcarousel-container jcarousel-container-top10"})
    i = 1
    for top10item in top10List:
        if i == 2:
            top10Divs = top10item.findAll("div", {"class": "jcarousel"})
            for top10div in top10Divs:                
                top10li = top10div.findAll("li")
                for liItem in top10li:
                    view.add_item(args,
                                {"url":         liItem.contents[4]['href'],
                                    "title":       liItem.contents[4].text,
                                    "tvshowtitle": liItem.contents[4].text,
                                    "mode":        "list_episodes",
                                    "thumb":       liItem.contents[1].next['src'],
                                    "fanart":      liItem.contents[1].next['src'],
                                    "rating":      "",
                                    "plot":        "",
                                    "year":        ""},                                
                                    isFolder=True, mediatype="video")
        i = i+1                           
    view.endofdirectory(args)

def showNewSimualcasts(args):
    page = requests.get(args._baseUrl)
    soup = BeautifulSoup(page.content, 'html.parser')
    newSimualcastsList = soup.findAll("div", {"class": "jcarousel-container jcarousel-container-top10"})
    i = 1
    for newSimualcastsIten in newSimualcastsList:
        if i == 1:
            newSimualcastsDivs = newSimualcastsIten.findAll("div", {"class": "jcarousel"})
            for newSimualcastsDiv in newSimualcastsDivs:                
                newSimualcastsLi = newSimualcastsDiv.findAll("li")
                for liItem in newSimualcastsLi:
                    view.add_item(args,
                                {"url":        liItem.contents[4]['href'],
                                    "title":       liItem.contents[4].text,
                                    "tvshowtitle": liItem.contents[4].text,
                                    "mode":        "list_episodes",
                                    "thumb":       liItem.contents[1].next['src'],
                                    "fanart":      liItem.contents[1].next['src'],
                                    "rating":      "",
                                    "plot":        "",
                                    "year":        ""},                                
                                    isFolder=True, mediatype="video")
        i = i+1                            
    view.endofdirectory(args)

def showNewAnime(args):
    page = requests.get(args._baseUrl)
    soup = BeautifulSoup(page.content, 'html.parser')
    mydivs = soup.findAll("div", {"class": "jcarousel-container jcarousel-container-new"})
    i = 1
    for item in mydivs:
        if i == 2:
            mydivs2 = item.findAll("div", {"class": "jcarousel"})
            for item2 in mydivs2:                
                mydivs3 = item2.findAll("li")
                for item3 in mydivs3:
                    url = item3.contents[4]['href']
                    view.add_item(args,
                                {"url":         url,
                                    "title":       item3.contents[4].text,
                                    "tvshowtitle": item3.contents[4].text,
                                    "mode":        "list_episodes",
                                    "thumb":       item3.contents[1].next['src'],
                                    "fanart":      item3.contents[1].next['src'],
                                    "rating":      "",
                                    "plot":        "",
                                    "year":        ""},                                
                                    isFolder=True, mediatype="video")
        i = i+1                            
    view.endofdirectory(args)

def showNewEpisode(args):
    page = requests.get(args._baseUrl)
    soup = BeautifulSoup(page.content, 'html.parser')
    mydivs = soup.findAll("div", {"class": "jcarousel-container jcarousel-container-new"})
    episodenListe = []
    i = 1
    for item in mydivs:
        if i == 1:
            mydivs2 = item.findAll("div", {"class": "jcarousel"})
            for item2 in mydivs2:
                mydivs3 = item2.findAll("li")
                for item3 in mydivs3:
                    episodenArray = util.returnEpisoden(item3.contents[7].text)
                    episodenListe.extend(util.listEpisodesByArray(item3.contents[4]['href'], episodenArray, args ))
        i = i + 1         

    for item in episodenListe:
        view.add_item(args,
                   {"url":         item['url'],
                    "title":       item['title'],
                    "tvshowtitle": item['tvshowtitle'],
                    "mode":        "videoplay",
                    "thumb":       item['img'],
                    "fanart":      item['img'],                    
                    "plot":        item['plot'],
                    "playcount": "0",
                    "progress":  ""
                    },
                    isFolder=False, mediatype="video")
    view.endofdirectory(args)   

def showNewEpisodesSerie(args):
    page = requests.get(args._baseUrl)
    soup = BeautifulSoup(page.content, 'html.parser')
    mydivs = soup.findAll("div", {"class": "jcarousel-container jcarousel-container-new"})
    i = 1
    for item in mydivs:
        if i == 1:
            mydivs2 = item.findAll("div", {"class": "jcarousel"})
            for item2 in mydivs2:                
                mydivs3 = item2.findAll("li")
                for item3 in mydivs3:
                    url = item3.contents[4]['href']
                    view.add_item(args,
                                {"url":         url,
                                    "title":       item3.contents[4].text,
                                    "tvshowtitle": item3.contents[4].text,
                                    "mode":        "list_episodes",
                                    "thumb":       item3.contents[1].next['src'],
                                    "fanart":      item3.contents[1].next['src'],
                                    "rating":      "",
                                    "plot":        "",
                                    "year":        ""},                                
                                    isFolder=True, mediatype="video")
        i = i+1                            
    view.endofdirectory(args)      



def showAll(args):
    page = requests.get(args._baseUrl + "/animes")
    soup = BeautifulSoup(page.content, 'html.parser')
    mydivs = soup.findAll("div", {"class": "three-box animebox"})
    for item in mydivs:
        animePlot  = item.findAll("p", {"class": "animebox-shorttext"})[0].text
        animeTitle = item.findAll("h3", {"class": "animebox-title"})[0].text
        animeImg   = item.findAll("p", {"class": "animebox-image"})[0].next['src']
        animeUrl   = item.findAll("p", {"class": "animebox-link"})[0].contents[1]['href']
        view.add_item(args,
                   {"url":         animeUrl,
                    "title":       animeTitle,
                    "tvshowtitle": animeTitle,
                    "mode":        "list_episodes",
                    "thumb":       animeImg,
                    "fanart":      animeImg,
                    "rating":      "",
                    "plot":        animePlot,
                    "year":        ""},
                    isFolder=True, mediatype="video")
    view.endofdirectory(args)

def showAtoZ(args):
    letters = [chr(i) for i in xrange(ord('a'), ord('z')+1)]
    for letter in letters:
        animeUrl = "https://www.anime-on-demand.de/animes/begins_with/"+letter.upper()
        view.add_item(args,
                   {"url":         animeUrl,
                    "title":       letter.upper(),
                    "tvshowtitle": letter.upper(),
                    "mode":        "showCharacter",
                    "thumb":       "",
                    "fanart":      "",
                    "rating":      "",
                    "plot":        "",
                    "year":        ""},
                    isFolder=True, mediatype="video")
    view.endofdirectory(args)

def showCharacter(args):
    page = requests.get(args.url)
    soup = BeautifulSoup(page.content, 'html.parser')
    mydivs = soup.findAll("div", {"class": "three-box animebox"})
    for item in mydivs:
        animePlot  = item.findAll("p", {"class": "animebox-shorttext"})[0].text
        animeTitle = item.findAll("h3", {"class": "animebox-title"})[0].text
        animeImg   = item.findAll("p", {"class": "animebox-image"})[0].next['src']
        animeUrl   = item.findAll("p", {"class": "animebox-link"})[0].contents[1]['href']
        view.add_item(args,
                   {"url":         animeUrl,
                    "title":       animeTitle,
                    "tvshowtitle": animeTitle,
                    "mode":        "list_episodes",
                    "thumb":       animeImg,
                    "fanart":      animeImg,
                    "rating":      "",
                    "plot":        animePlot,
                    "year":        ""},
                    isFolder=True, mediatype="video")
    view.endofdirectory(args)

def listEpisodes(args):
    page = requests.get("https://www.anime-on-demand.de" + args.url, cookies=args._cookie)
    soup = BeautifulSoup(page.content, 'html.parser')
    mydivs = soup.findAll("div", {"class": "three-box episodebox flip-container"})          
    for item in mydivs:
        episodeTitle = item.findAll("h3", {"class": "episodebox-title"})[0]['title']
        episodeImg   = item.findAll("p", {"class": "episodebox-image"})[0].next['src']
        episodeUrl      = item.findAll("input", {"title": "Deutschen Stream starten"})
        if len(episodeUrl) > 0:
            episodeUrl = episodeUrl[0]['data-playlist']
            view.add_item(args,
                {"url":       episodeUrl,
                    "title":     episodeTitle + "(Ger)",
                    "mode":      "videoplay",
                    "thumb":     episodeImg,
                    "fanart":    episodeImg,
                    "playcount": "0",
                    "progress":  ""},
                    isFolder=False, mediatype="video")
        
        episodeUrl      = item.findAll("input", {"title": "Japanischen Stream mit Untertiteln starten"})
        if len(episodeUrl) > 0:
            episodeUrl = episodeUrl[0]['data-playlist']
            view.add_item(args,
                {"url":       episodeUrl,
                    "title":     episodeTitle + "(Jap)",
                    "mode":      "videoplay",
                    "thumb":     episodeImg,
                    "fanart":    episodeImg,
                    "playcount": "0",
                    "progress":  ""},
                    isFolder=False, mediatype="video")         
    view.endofdirectory(args)

def startplayback(args):    
    addon = xbmcaddon.Addon()
    url = args._baseUrl + args.url
    xbmc.log("test123" + url,xbmc.LOGNOTICE)    
    pluginhandle = int(sys.argv[1])    
    headers = {'X-CSRF-Token' : args._crsftoken,
                'X-Requested-With' :  "XMLHttpRequest",
                'Accept' : "application/json, text/javascript, */*; q=0.01"
              }      
    page = requests.get(url, cookies=args._cookie, headers=headers)
    fileSoup = BeautifulSoup(page.content)
    test = json.loads(page.content.decode("utf-8"))
    url = test['playlist'][0]['sources'][0]['file']
    listitem = xbmcgui.ListItem (path=url)  
    listitem.setProperty('inputstreamaddon', 'inputstream.adaptive')
    listitem.setProperty('inputstream.adaptive.manifest_type', 'hls')
    xbmcplugin.setResolvedUrl(int(args._argv[1]),True, listitem)    

