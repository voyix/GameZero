import sqlite3

def config(dbPATH):
    with sqlite3.connect(dbPATH) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Configs")
        return cursor.fetchall()

def LogMessage(dbPATH,message, level):
    with sqlite3.connect(dbPATH) as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO Log(Message,Level,MessageDateTime) SELECT ?,?,datetime()", [message, level])

def GetLogMessages(dbPATH,level=None):
    with sqlite3.connect(dbPATH) as db:
        cursor = db.cursor()
        sql = 'SELECT * FROM Log'
        if(level != None):
            sql = sql + " WHERE Level='" + level + "'"
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

def getinfo(dbPATH, dbname):
    with sqlite3.connect(dbPATH) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM " + dbname)
        return cursor.fetchall()

def wantedLIST(dbPATH, where=""):
    
    statment = ""
    
    if where == "All":
        statement = "SELECT * FROM WantedGames"
        table_data = "<div><ul>"
    elif where == "":
        statement = "SELECT * FROM WantedGames"
        table_data = "<div class=nav><ul>"
    else:
        statement = "SELECT * FROM WantedGames WHERE id = " + where
        table_data = "<div><ul>"
    
    with sqlite3.connect(dbPATH) as db:
        cursor = db.cursor()
        for row in cursor.execute(statement):
            table_data = table_data + "<li><a href=Games?Wanted=" + str(row[0]) + ">" + str(row[3]) + "</a></li>"
    table_data = table_data +  "<li class=readmore><a href=Games?Wanted=All>More Games</a></li></ul></div>"
    return table_data

def wantedLISTID(dbPATH, lid):
    with sqlite3.connect(dbPATH) as db:
        cursor = db.cursor()
        if (lid == "All"):
           row = cursor.execute("SELECT * FROM WantedGames")
        else:
            row = cursor.execute("SELECT * FROM WantedGames WHERE ID = " + lid)
    return row

def insertSearchHistory(dbPATH, Searchfor, Searchid):
    with sqlite3.connect(dbPATH) as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO SearchHistory(Searcher,SearcherID) VALUES (?,?)", [Searchfor,Searchid])
    

def ClearLog(dbPATH):
    conn = sqlite3.connect(dbPATH)
    conn.execute("DELETE FROM Log")
    conn.commit()
    conn.close()