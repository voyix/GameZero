import urllib2
from bs4 import BeautifulSoup

def getlist():
    dat = []
    url = "https://retropie.org.uk/about/systems/"
    webRequest = urllib2.Request(url, headers={'User-Agent' : "GameZero Browser"})
    try:
        response = urllib2.urlopen(webRequest)
        platformData = response.read()
        soup = BeautifulSoup(platformData, 'html.parser')        
        table = soup.find("table")
        tbody = table.find('tbody')
        for rows in tbody.find_all("tr"):
            cols = rows.find_all("td")
            tmp = unicode(cols[0].contents[1])  
            cols = [ele.text.strip() for ele in cols]    
            dat.append([tmp,cols[1],cols[2],cols[3],cols[4]])
        
        return dat
    except URLError as e:
        return dat
    
    