

def createbutton(object):
     buf = """<form method=post action='functions'>"""
     
     buf = buf + """ <input type="hidden" id="gid" name="gid" value= """ + object[0] + """   > """
     buf = buf + """ <input type="hidden" id="gtitle" name="gtitle" value= """ + object[1] + """   > """
     buf = buf + """ <input type="hidden" id="PlatformId" name="PlatformId" value= """ + object[2] + """   > """
     buf = buf + """ <input type="hidden" id="Platform" name="Platform" value= """ + object[3] + """   > """
     buf = buf + """ <input type="hidden" id="addWantedGame" name="addWantedGame">"""
     buf = buf + """<button type='submit'>Add</button>"""
     
     buf = buf + """</form>"""
     return buf

@cherrypy.expose
def addWantedGame():
     pass