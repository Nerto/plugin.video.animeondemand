import sys

import requests
from bs4 import BeautifulSoup

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

def py2_enc(s, encoding='utf-8'):
	if PY2 and isinstance(s, unicode):
		s = s.encode(encoding)
	return s

def py3_dec(d, encoding='utf-8'):
	if PY3 and isinstance(d, bytes):
		d = d.decode(encoding)
	return d

def translation(id,addon):
	LANGUAGE = addon.getLocalizedString(id)
	LANGUAGE = py2_enc(LANGUAGE)
	return LANGUAGE

def login(args):
    session = requests.Session()
    page = session.get("https://www.anime-on-demand.de/users/sign_in")
    soup = BeautifulSoup(page.content, 'html.parser')
    authenticity_token = soup.find("input", {"name": "authenticity_token"})['value']
    values = {'user[login]' : args._addon.getSetting("user"),
        'user[password]' : args._addon.getSetting("pass"),
        'user[remember_me]' : '1',
        'commit' : 'Einloggen' ,
        'authenticity_token' : authenticity_token
    }
    pageLogin = session.post("https://www.anime-on-demand.de/users/sign_in",data=values)
    soupLogin = BeautifulSoup(page.content, 'html.parser')   
    args.set_cookie(pageLogin.cookies)   
    args.set_crsftoken((soupLogin.find("meta", {"name" : "csrf-token"})["content"]))

def listEpisodesByArray(url, array,args):
    page = requests.get("https://www.anime-on-demand.de" + url, cookies=args._cookie)
    soup = BeautifulSoup(page.content, 'html.parser')
    serienName = soup.findAll("h1", {"itemprop": "name"})[0].next.replace("\t","").replace("\n","")
    episodeList = []
    mydivs = soup.findAll("div", {"class": "three-box episodebox flip-container"})
    for item in mydivs: 
        episodeTitle = ""      
        episodeImg = ""
        episodePlot  = ""
        try:       
            episodeTitle = item.find("h3", {"class": "episodebox-title"})['title']        
            episodeImg = item.find("p", {"class": "episodebox-image"}).next['src']
            text = item.findAll("div", {"class": "besides-box"})
            episodePlot  = item.findAll("p", {"class": "episodebox-shorttext"})[0].text
        except:
            pass
        try:
            episodeUrl = text[0].contents[1].contents[0].attrs['data-playlist']
            episodeLang = text[0].contents[1].contents[0].attrs['data-lang']
            for arrayItem in array:
                stringTemp =  "Episode " + str(arrayItem) + " -"
                if(stringTemp in episodeTitle):
                    mydict = { "title" : (serienName + " - " + episodeTitle +  " [" + episodeLang + "]"),
                            "tvshowtitle" : serienName, 
                            "plot" : episodePlot,
                            "img" : episodeImg ,
                            "url" : episodeUrl }
                    episodeList .append(mydict)    
        except:
            pass           
        try:
            episodeUrl = text[1].contents[1].contents[0].attrs['data-playlist']
            episodeLang = text[1].contents[1].contents[0].attrs['data-lang']
            for arrayItem in array:
                stringTemp =  "Episode " + str(arrayItem) + " -"
                if(stringTemp in episodeTitle):
                    mydict = { "title" : (serienName + " - " + episodeTitle +  " [" + episodeLang + "]"),
                            "tvshowtitle" : serienName, 
                            "plot" : episodePlot,
                            "img" : episodeImg ,
                            "url" : episodeUrl }
                    episodeList .append(mydict)    
        except:
            pass
    return episodeList


def returnEpisoden(episodenString):
    tempString1 = episodenString.replace("Episode ", "")
    tempint1 = 0
    tempint2 = 0
    if "-" in tempString1:
        tempArray = tempString1.split("-")
        tempint1 = int(tempArray[0])
        tempint2 = int(tempArray[1])+1    
    else:
        tempint1 = int(tempString1)
        tempint2 = int(tempString1)+1
    episodenArray = list(range(tempint1, tempint2))
    return episodenArray
