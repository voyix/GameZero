import sqlite3
import GameZero.resources as GS

def run(dbPath):
    with sqlite3.connect(dbPath) as db:
        cursor = db.cursor()
        cursor.execute('pragma user_version')
        version = cursor.fetchone()[0]
        if(version==0 or version==1):

            db.execute("CREATE TABLE IF NOT EXISTS Systems (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,console TEXT,system TEXT, Yr TEXT,ROMEXT TEXT,BIOS TEXT,pid TEXT,alias TEXT)")
            db.execute("CREATE TABLE IF NOT EXISTS Configs (Config_Name TEXT, Config_Value TEXT)")
            db.execute("CREATE TABLE IF NOT EXISTS WantedGames (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,SystemID TEXT, GameID TEXT, GameName TEXT, Status TEXT)")
            db.execute("CREATE TABLE IF NOT EXISTS Log (ID INTEGER PRIMARY KEY AUTOINCREMENT, Level TEXT, Message TEXT, MessageDateTime TEXT)")
            db.execute("CREATE TABLE IF NOT EXISTS SearchHistory (ID INTEGER PRIMARY KEY AUTOINCREMENT,Searcher TEXT,SearcherID TEXT)")
            
            #Insert Configs
            cursor.execute("INSERT INTO Configs VALUES ('browser','1')")
            cursor.execute("INSERT INTO Configs VALUES ('theme','GameZero')")
            cursor.execute("INSERT INTO Configs VALUES ('uname','gamezero')")
            cursor.execute("INSERT INTO Configs VALUES ('pw','gamezero1')")
            cursor.execute("INSERT INTO Configs VALUES ('host','127.0.0.1')")
            cursor.execute("INSERT INTO Configs VALUES ('port','7135')")
            cursor.execute("INSERT INTO Configs VALUES ('update','0')")
            cursor.execute("INSERT INTO Configs VALUES ('version','0.0.1')")
            cursor.execute("INSERT INTO Configs VALUES ('recomendations','id212;id28')")
            cursor.execute("INSERT INTO Configs VALUES ('updateurl','http://noami.mooo.com/')")
            cursor.execute("INSERT INTO Configs VALUES ('RPSYSURL','https://retropie.org.uk/about/systems/')")
            cursor.execute("INSERT INTO Configs VALUES ('APIGDBGGL','http://thegamesdb.net/api/GetGamesList.php?name=')")
            cursor.execute("INSERT INTO Configs VALUES ('APIGDBGG','http://thegamesdb.net/api/GetGame.php?id=')")
            cursor.execute("INSERT INTO Configs VALUES ('APIGDBGPL','http://thegamesdb.net/api/GetPlatformsList.php')")  

            platformlist = GS.infoprovider.thegamesdb.getplatformslist()
            platlist = GS.infoprovider.retropie.getlist() 
            
            for pid, nm, alias in platformlist:
                for console, system, yr, rom, bios in platlist:
                    if system.lower() in nm.lower():
                        sql = "INSERT INTO Systems (console,system, Yr, ROMEXT, BIOS, pid, alias) VALUES (?,?,?,?,?,?,?)"          
                        db.execute(sql,[console, nm, yr, rom, bios, pid, alias])
        
        cursor.execute('pragma user_version=1')
        db.commit()
        return;