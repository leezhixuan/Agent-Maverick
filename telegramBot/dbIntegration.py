import pygsheets
import pandas as pd
from User import User

class GoogleSheet:

    def __init__(self, filePath = 'telegramBot/lifehack22pr-bros-2ad1b5adbcbc.json') -> None:
        #Authorize 
        gc = pygsheets.authorize(service_file=filePath)
        #Open GoogleSheet 
        self.sh = gc.open('botDB')
        #Select worksheet
        #self.wks = sh[0]
        wks = self.sh[0]
        self.lastRow = wks.cell('B1').value

    def updateUser(self, user:object):
        """
        Given a user, append to google sheet a new row and increment counter.
        """
        wks = self.sh[0]
        cellCol = {0:"A", 1:"B", 2:"C"}
        for idx,info in enumerate(user.getInfo()):
            cell = cellCol[idx] + str(self.lastRow)
            wks.update_value(cell,info)
        #Update last row
        wks.update_value("B1",int(self.lastRow) + 1)
        self.lastRow = wks.cell('B1').value


        

