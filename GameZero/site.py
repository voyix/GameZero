import cherrypy
import GameZero
import os

import resources.infoprovider as infopro

from GameZero import db
from GameZero import search
from GameZero import tasks
from GameZero import update
from GameZero import functions

class site(object):
       
    @cherrypy.expose
    def index(self):        
        return self.LoadTheme("Index")
    
    @cherrypy.expose
    def Games(self, Wanted=""):
        return self.LoadTheme("Games<br>" + db.wantedLIST(GameZero.DATABASE_PATH, Wanted))

    @cherrypy.expose
    def Platforms(self):
        content = "<br /><table border='1'><thead><tr><th style='text-align:center; font-size: 10px'>Console</th><th style='text-align:center; font-size: 10px'>System</th><th style='text-align:center; font-size: 10px'>Year</th><th style='text-align:center; font-size: 10px'>ROM Extension(s)</th><th style='text-align:center; font-size: 10px'>BIOS</th></tr></thead>"

        table_content = db.getinfo(GameZero.DATABASE_PATH, "Systems")
        table_data = "<tbody>"
        for row in table_content:
            table_data = table_data + "<tr>"
            table_data = table_data + "<td style='text-align:center;'>" + str(row[1]) + "</td>"
            table_data = table_data + "<td style='text-align:center; font-size: 11px'>" + str(row[2]) + "</td>"
            table_data = table_data + "<td style='text-align:center; font-size: 10px'>" + str(row[3]) + "</td>"
            table_data = table_data + "<td style='text-align:center; font-size: 10px'>" + str(row[4].replace(" .","<br/>.")) + "</td>"
            table_data = table_data + "<td style='text-align:center; font-size: 10px'>" + str(row[5]) + "</td>"
            table_data = table_data + "</tr>"
        table_data = table_data + "</tbody></table>"
        content = content + table_data

        return self.LoadTheme(content)

    @cherrypy.expose
    def Stats(self):
        return self.LoadTheme("STATS")
    
    @cherrypy.expose
    def search(self, keyword):
        data = ""
        gamesdata = infopro.thegamesdb.getgamelist(keyword)
        
        for dat in gamesdata:
            #data = data + str(dat[0]) + "<br>"
            db.insertSearchHistory(GameZero.DATABASE_PATH, keyword, dat[0])
            gamedata = infopro.thegamesdb.getgame(dat[0])
            for gid, gtitle, PlatformId, Platform, ReleaseDate, Overview, Coop, boxart, YouTube, Publisher, Developer, Rating in gamedata:
                
                button = functions.createbutton([gid,gtitle,PlatformId,Platform])
                
                data = data + """<table style="border: 1; width:100%; border-spacing: 2; table-layout: fixed">"""
                data = data + """<tr>"""
                data = data + """<td rowspan="3" valign="top" style="text-align: center; padding: 5px">"""
                data = data + """<a href=http://legacy.thegamesdb.net/game/""" + gid + """/>
                <img width='100' height='158' src='http://legacy.thegamesdb.net/banners/""" + boxart + """' alt='""" + gtitle + """' style='border: 1px solid #666;'></a><br/><br/>""" +button+""" </td>"""
                data = data + """<td style="padding: 5px; font-size: 10px"><a href=http://legacy.thegamesdb.net/game/""" + gid + """/>""" + gtitle + """</a></td>"""
                data = data + """<td style="padding: 5px; text-align: right; font-size: 10px">""" + ReleaseDate + """</td>"""
                data = data + """</tr><tr>"""
                data = data + """<td colspan="2" style="padding: 5px;font-size: 10px">Rating: """ + Rating + """ <br/> <br/>""" + Overview + """<br/><br/>Co-op: """ + Coop + """<br/>Publisher: """ + Publisher + """<br/>Developer: """ + Developer + """</td>"""
                data = data + """</tr><tr>"""
                data = data + """<td width="70%" style="padding: 5px; font-size: 10px"><a href=http://legacy.thegamesdb.net/platform/""" + Platform.replace(" ", "-") + """ />""" + Platform + """</a></td>"""
                data = data + """<td style="padding: 5px; font-size: 10px; text-align: right">"""
                
                if (YouTube=="N/A"):
                    data = data + """ Youtube: """ + YouTube
                else:
                    data = data + """ <a href=""" + YouTube + """> Youtube </a>"""
                
                data = data + """</td></tr></table><br/><br/>"""
                data = data + """ <br/><br/> """
        return self.LoadTheme(data)

    @cherrypy.expose
    def Settings(self):

        if(GameZero.BROWSER == "1"):
            launchBrowser = "checked"
        else:
            launchBrowser = ""

        themebox = "<select>"
        for item in os.listdir(os.path.join(GameZero.PROG_DIR, GameZero.MY_NAME,"resources","interface")):
            if (GameZero.THEME == item):
                themebox = themebox + "<option selected value=""" + item + """>""" +  item + "</option>"
            else:
                themebox = themebox + "<option value=""" + item + """>""" +  item + "</option>"
        themebox = themebox + "</select>"      

        content = ""
        content = content + """
            <br />
            <div align="right">
                <button id="saveButton">Save</button>
            </div>
            <ul class="idTabs">
                <li><a href="#GamezServer">Gamez Server</a></li>
                <li><a href="#Downloaders">Downloaders</a></li>
                <li><a href="#Searchers">Searchers</a></li>
                <li><a href="#PostProcess">Post Process</a></li>
            </ul>
            <div class="tab-container">
                <div id="GamezServer">
                    <fieldset align="left">
                        <legend>General</legend>
                        <div>
                            Current Version: """ + str(GameZero.VERSION) + """
                        </div>
                        <br />
                        <div>
                            Host / Port<br />
                            <input type="input" size="45" id="host" value='""" + str(GameZero.HOST) + """' />
                            <input type="input" size="5" id="port" value='""" + str(GameZero.SERVERPORT) + """' />
                        </div>
                        <br />
                        <div>
                            <input type="checkbox" name="launchBrowser" id="launchBrowser" """ + launchBrowser + """ />
                             Launch browser on startup
                        </div>
                    </fieldset>
                    <br /> 
                    <fieldset align="left">
                        <legend>Theme</legend>
                        <div>
                            Default Theme """                            
        content = content + themebox                            
        content = content + """
                        </div>
                    </fieldset>
                    <br />
                    <fieldset align="left">
                        <legend>Login</legend>
                        <div>
                            <label for="host">Username</label><br />
                            <input type="input" size="50" id="username" value='""" + str(GameZero.USERNAME) + """' />
                        </div>
                        <div>
                            <label for="host">Password</label><br />
                            <input type="input" size="50" id="password" value='""" + str(GameZero.PASSWORD) + """' />
                        </div>
                    </fieldset>
                     <br /> 
                    <fieldset align="left">
                        <legend>Recommendations</legend> <div>"""
        content = content + """\n <table style="width:100%;" border=1>\n"""
        
        sys = db.getinfo(GameZero.DATABASE_PATH, "Systems")
        c = str(GameZero.RECOMENDATIONS).split(";")
        count = 0
        rcnt = 0
        
        for row in sys:
            if count == 0:
                content = content + """<tr>\n"""
                rcnt = rcnt + 1
                
            chkid = str(count) + str(rcnt)
            
            chk = ""
            
            for tmp in c:
                if tmp == chkid:
                    chk = " checked=checked "
                            
            content = content + """<td style='font-size: 10px'><input id=" """ + str(chkid) + """ " type="checkbox" """ + chk + """ /><label for="host">""" + str(row[2]).strip() + """<td/>\n"""
                        
            count = count + 1
            
            if count == 3:
                content = content + """</tr>\n"""
                count = 0

        content = content + """</table>\n</div>                        
                    </fieldset>
                    <br /> 
                    <fieldset align="left">
                        <legend>Updates</legend>
                        <div>
                            <label for="host">Update URL</label><br />
                            <input type="input" size="50" id="updateurl" value='""" + str(GameZero.UPDATEURL) + """' />
                        </div>
                        <br />
                        <div align="right">                           
                            <a href="Update">Run update NOW!</a> 
                        </div>
                    </fieldset>
                </div>
                
                <div id="Downloaders">Downloaders</div>
                
                <div id="Searchers">                
                    <fieldset align="left">
                        <legend>General</legend>                        
                        <br />
                        <div>
                            Retropie System URL <br />
                            <input type="input" size="50" id="host" value='""" + str(GameZero.RPSYSURL) + """' />                            
                        </div>
                        <br />
                        <div>
                            THEGAMEDB api [GetGamesList] URL<br />
                            <input type="input" size="50" id="host" value='""" + str(GameZero.APIGDBGGL) + """' />
                        </div>
                        <br />
                        <div>
                            THEGAMEDB api [GetGame] URL<br />
                            <input type="input" size="50" id="host" value='""" + str(GameZero.APIGDBGG) + """' />                            
                        </div>
                        <br />
                        <div>
                            THEGAMEDB api [GetPlatformsList] URL<br />
                            <input type="input" size="50" id="host" value='""" + str(GameZero.APIGDBGPL) + """' />
                        </div>
                    </fieldset>
                </div>                
                <div id="PostProcess">PostProcess</div>
            </div>            
            
            <br />
            <div align="right">
                <button id="saveButton">Save</button>
            </div>
        """
        return self.LoadTheme(content)

    @cherrypy.expose
    def LoadTheme(self, content):
        with open(os.path.join(GameZero.THEMEPATH, "tmpl","header.tpl"), 'r') as thefile:
            header = thefile.read()

        with open(os.path.join(GameZero.THEMEPATH, "tmpl","footer.tpl"), 'r') as thefile:
            footer = thefile.read()

        with open(os.path.join(GameZero.THEMEPATH, "tmpl","nav.tpl"), 'r') as thefile:
            nav = thefile.read().replace("_WANTEDNAV", db.wantedLIST(GameZero.DATABASE_PATH))

        with open(os.path.join(GameZero.THEMEPATH, "tmpl","searchbox.tpl"), 'r') as thefile:
            searchbox = thefile.read()

        try:
            stuff = header + nav + searchbox + content + footer
        except:
            stuff = header + nav + searchbox + content.encode('ascii', 'ignore') + footer
        return stuff