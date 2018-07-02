import GameZero
from GameZero import db
from GameZero import site
from GameZero import tasks

import install
import cherrypy
from cherrypy.process.plugins import Monitor
import webbrowser, os

def main():    
     # do some preliminary stuff
    GameZero.MY_FULLNAME = os.path.normpath(os.path.abspath(__file__))
    GameZero.MY_NAME = os.path.split(os.path.dirname(GameZero.MY_FULLNAME))[1]
    GameZero.PROG_DIR = os.path.dirname(GameZero.MY_FULLNAME)
    GameZero.DATABASE_PATH = os.path.join(GameZero.PROG_DIR, GameZero.MY_NAME, "DATABASE.DB")
    
    # Make sure we can write to the data dir
    if not os.access(GameZero.PROG_DIR, os.W_OK):
        sys.exit("Data directory: " + GameZero.PROG_DIR + " must be writable (write permissions). Exiting.") 
    
    #CANT FIND DATABASE - RUN INSTALL    
    if not os.path.exists(GameZero.DATABASE_PATH):
        install.run(GameZero.DATABASE_PATH)#run the install
            
    #Load the configs
    db.LogMessage(GameZero.DATABASE_PATH, "Loading Configurations to memory", "Info")
    LoadConfigs(db.config(GameZero.DATABASE_PATH))
        
    #get cherrypy ready
    db.LogMessage(GameZero.DATABASE_PATH, "Registering Background Processes", "Info")
    
    GameZero.THEMEPATH = os.path.join(GameZero.PROG_DIR, GameZero.MY_NAME,"resources","interface",GameZero.THEME)
        
    cherrypy.config.update({'server.socket_port': int(GameZero.SERVERPORT), 'server.socket_host': GameZero.HOST, 'response.timeout':900})
    appConfig = {'/static': {'tools.staticdir.on': True, 'tools.staticdir.dir': GameZero.THEMEPATH}}
    cherrypy.tree.mount(site.site(), '/', appConfig)
      
    Monitor(cherrypy.engine, tasks.Task().CheckUpdates, frequency=86400).subscribe()
    Monitor(cherrypy.engine, tasks.Task().PostProcess, frequency=86400).subscribe()
    #Monitor(cherrypy.engine, Task.Task().PostProcess, frequency=86400).subscribe()
    
    db.LogMessage(GameZero.DATABASE_PATH, "Starting Service", "Info")
    cherrypy.engine.start()
 
    if(GameZero.BROWSER == '1'):
        webbrowser.open("http://" + cherrypy.server.socket_host + ":" + str(cherrypy.server.socket_port) + '/')
    
    cherrypy.engine.block()
    
def LoadConfigs(configs):
    for row in configs:
        if row[0] == "browser":
            GameZero.BROWSER = row[1]
        if row[0] == "host":
            GameZero.HOST = row[1]
        if row[0] == "theme":
            GameZero.THEME = row[1]
        if row[0] == "port":
            GameZero.SERVERPORT = row[1]
        if row[0] == "version":
            GameZero.VERSION = row[1]
        if row[0] == "updateurl":
            GameZero.UPDATEURL = row[1]
        if row[0] == "uname": 
            GameZero.USERNAME = row[1]
        if row[0] == "pw":
            GameZero.PASSWORD = row[1]
        if row[0] == "RPSYSURL":
            GameZero.RPSYSURL = row[1]
        if row[0] == "APIGDBGGL":
            GameZero.APIGDBGGL = row[1]
        if row[0] == "APIGDBGG":
            GameZero.APIGDBGG = row[1]
        if row[0] == "APIGDBGPL":
            GameZero.APIGDBGPL= row[1]
        if row[0] == "recomendations":
            GameZero.RECOMENDATIONS= row[1]

if __name__ == "__main__":
    main()