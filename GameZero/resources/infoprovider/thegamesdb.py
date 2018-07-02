import urllib2
from xml.etree import ElementTree

def getgamelist(game):
    dat = []            
    #first we get thegamedb stuff
    url = "http://thegamesdb.net/api/GetGamesList.php?name=" + game
    webRequest = urllib2.Request(url, headers={'User-Agent' : "GameZero Browser"})
    response = urllib2.urlopen(webRequest)
    gameData = response.read()
    treeData = ElementTree.fromstring(gameData)
    for matchedElement in treeData.findall('./Game'):
        dat.append([matchedElement.find('id').text, matchedElement.find('GameTitle').text, matchedElement.find('ReleaseDate').text,matchedElement.find('Platform').text])
    
    return dat
        
def getgame(gameid):
    dat = []
    #first we get thegamedb stuff
    gameurl = "http://thegamesdb.net/api/GetGame.php?id=" + str(gameid)
    webRequest = urllib2.Request(gameurl, headers={'User-Agent' : "GameZero Browser"})
    response = urllib2.urlopen(webRequest)
    gameData = response.read()
    treeData = ElementTree.fromstring(gameData)
    
    for matchedElement in treeData.findall('./Game'):
        # id , GameTitle, PlatformId, Platform, ReleaseDate, Overview, Genres[multi], Co-op, Rating, Similar[multi], Images[multi]
        gid = matchedElement.find('id').text
        gtitle = matchedElement.find('GameTitle').text
        PlatformId = matchedElement.find('PlatformId').text
        Platform = matchedElement.find('Platform').text
        
        try:
            ReleaseDate = matchedElement.find('ReleaseDate').text
        except:
            ReleaseDate = "Unknown"
        
        try:
            Overview = matchedElement.find('Overview').text
        except:
            Overview = "No Overview"
        
        try:
            Coop = matchedElement.find('Co-op').text
        except:
            Coop = "Unknown"
            
        try:
            boxart = matchedElement.find('Images/boxart[@side="front"]').text
        except:
            boxart = ""
            
        try:
            YouTube = matchedElement.find('Youtube').text
        except:
            YouTube = "N/A"
        
        try:
            Publisher = matchedElement.find('Publisher').text
        except:
            Publisher = "Unknown"
            
        try:
            Developer = matchedElement.find('Developer').text
        except:
            Developer = "Unknown"
            
        try:
            Rating = matchedElement.find('Rating').text
        except:
            Rating = "0.00"
            
            
        dat.append([gid, gtitle, PlatformId, Platform, ReleaseDate, Overview, Coop, boxart, YouTube, Publisher, Developer, Rating])

    return dat

def getplatformslist():
    dat = []
    #first we get thegamedb stuff
    url = "http://thegamesdb.net/api/GetPlatformsList.php"
    webRequest = urllib2.Request(url, headers={'User-Agent' : "GameZero Browser"})
    response = urllib2.urlopen(webRequest)
    platformData = response.read()
    treeData = ElementTree.fromstring(platformData)
    for matchedElement in treeData.findall('./Platforms/Platform'):
        if matchedElement.find('id') != None and matchedElement.find('alias') != None and matchedElement.find('name') != None:
            dat.append([matchedElement.find('id').text, matchedElement.find('name').text, matchedElement.find('alias').text])

    return dat