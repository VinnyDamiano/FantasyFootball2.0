######################################
#This is the main and only file needed for fantasy football 2.0
#Created by Vinny Damiano
######################################

import requests
from requests import get
from bs4 import BeautifulSoup as bs
from tkinter import *
import json

#finds the best and worst defenses vs a given position
def defenses(position):
    url = 'https://www.cbssports.com/fantasy/football/stats/posvsdef/'\
                                            +str(position)+"/all/avg/standard"
    defenseList = []
    request = requests.get(url)
    content = request.content
    soup = bs(content, 'html.parser')
    table = soup.findChildren('table')[0]
    rows = table.findChildren('tr')
    numbers = [3,4,33,34]
    for i in range(len(numbers)):
        cells = rows[numbers[i]].findChildren('td')
        for cell in cells:
            cell_content = cell.getText()
            if cell_content.startswith(position):
                defenseList.append(cell_content[6:])
    return(defenseList)
    
#gets each players week by week stats
def getWeekStats(Lastname,Firstname,Week):
    url = ("https://www.pro-football-reference.com/players/"+Lastname[0]+"/"+\
                                        Lastname[:4]+Firstname[:2]+"00.htm#")
    statsList = []
    request = requests.get(url)
    content = request.content
    soup = bs(content, 'html.parser')
    table = soup.findChildren('table')[0]
    rows = table.findChildren('tr')
    headers = [x.getText() for x in rows[1].findChildren('th')]
    count = 0
    cells = rows[Week+1].findChildren('td')
    for cell in cells:
        count += 1
        cell_content = cell.getText()
        statsList.append((headers[count],cell_content))
    return statsList

def getBye(last,first):
    teams = getTeams(last,first)
    team = teams[len(teams)-1]
    return bye[team]
    

#gets the current nfl week that we are on
def getCurrentWeek():
    url = ("http://www.nfl.com/schedules")
    request = requests.get(url)
    content = request.content
    soup = bs(content, 'html.parser')
    body = soup.findChildren('body')[0]
    text = body.getText()
    for line in text.splitlines():
        if "NFL WEEK" in line:
            return line[8:].strip()
    
#clean the QB stats and leaves only the stats that count for fantasy
def cleanQBStats(lst):
    finalList = []
    rushList = []
    passList = lst[9:12]
    rushList.append(lst[18])
    rushList.append(lst[20])
    finalList += passList + rushList
    for i in range(len(lst)):
        if lst[i][0] == "Fmb":
            finalList.append(lst[i])
    return finalList

#clean the RB stats and leaves only the stats that count for fantasy
def cleanRBStats(lst):
    finalList = []
    finalList.append(lst[7])
    finalList.append(lst[9])
    finalList.append(lst[11])
    finalList.append(lst[12])
    finalList.append(lst[14])
    for i in range(len(lst)):
        if lst[i][0] == "Fmb":
            finalList.append(lst[i])
    return finalList

#clean the TE and WR stats and leaves only the stats that count for fantasy
def cleanWRTEStats(lst):
    finalList = []
    finalList.append(lst[7])
    finalList.append(lst[8])
    finalList.append(lst[10])
    for i in range(len(lst)):
        if lst[i][0] == "Fmb":
            finalList.append(lst[i])
    return finalList

#Gets the position of a given player
def getPosition(Lastname,Firstname):
    url = ("https://www.pro-football-reference.com/players/"+Lastname[0]+"/"+\
                                        Lastname[:4]+Firstname[:2]+"00.htm#")
    request = requests.get(url)
    content = request.content
    soup = bs(content, 'html.parser')
    body = soup.findChildren('body')[0]
    text = body.getText()
    for line in text.splitlines():
        if "Position" in line:
            return line[10:12]
            
#Creates a list of all the teams a given player has played on
def getTeams(Lastname,Firstname):
    teamList = []
    url = ("https://www.pro-football-reference.com/players/"+Lastname[0]+"/"+\
                                        Lastname[:4]+Firstname[:2]+"00.htm#")
    request = requests.get(url)
    content = request.content
    soup = bs(content, 'html.parser')
    table = soup.findChildren('table')[1]
    rows = table.findChildren('tr')
    headers = [x.getText() for x in rows[0].findChildren('th')]
    for row in rows:
        cells = row.findChildren('td')
        for cell in cells:
            cell_content = cell.getText()
            if cell_content.isalpha():
                if cell_content not in{"QB","qb","RB","rb","WR","wr","TE","te"}:
                    teamList.append(cell_content)
    
    #fixes glitch that adds all teams player has played for 
    teamSet = set(teamList)
    if len(teamSet) >1:
        for i in range(len(teamSet)):
            teamList.pop()
    return teamList

#assigning each team to their division to find rivalries
divs= {}
divs["TAM"] = "NS"
divs["CAR"] = "NS"
divs["NOR"] = "NS"
divs["ATL"] = "NS"
divs["GNB"] = "NN"
divs["DET"] = "NN"
divs["CHI"] = "NN"
divs["MIN"] = "NN"
divs["DAL"] = "NE"
divs["NYG"] = "NE"
divs["WAS"] = "NE"
divs["PHI"] = "NE"
divs["ARI"] = "NW"
divs["SEA"] = "NW"
divs["LAR"] = "NW"
divs["SFO"] = "NW"
divs["IND"] = "AS"
divs["HOU"] = "AS"
divs["TEN"] = "AS"
divs["JAX"] = "AS"
divs["CLE"] = "AN"
divs["PIT"] = "AN"
divs["BAL"] = "AN"
divs["CIN"] = "AN"
divs["NWE"] = "AE"
divs["MIA"] = "AE"
divs["NYJ"] = "AE"
divs["BUF"] = "AE"
divs["KAN"] = "AW"
divs["LAC"] = "AW"
divs["DEN"] = "AW"
divs["OAK"] = "AW"

#assigns each team to their bye
bye= {}
bye["TAM"] = 5
bye["CAR"] = 4
bye["NOR"] = 6
bye["ATL"] = 8
bye["GNB"] = 7
bye["DET"] = 6
bye["CHI"] = 5
bye["MIN"] = 10
bye["DAL"] = 8
bye["NYG"] = 9
bye["WAS"] = 4
bye["PHI"] = 9
bye["ARI"] = 9
bye["SEA"] = 7
bye["LAR"] = 12
bye["SFO"] = 11
bye["IND"] = 9
bye["HOU"] = 10
bye["TEN"] = 8
bye["JAX"] = 9
bye["CLE"] = 11
bye["PIT"] = 7
bye["BAL"] = 10
bye["CIN"] = 9
bye["NWE"] = 11
bye["MIA"] = 11
bye["NYJ"] = 11
bye["BUF"] = 11
bye["KAN"] = 12
bye["LAC"] = 8
bye["DEN"] = 10
bye["OAK"] = 7

#detrmines if players are current rivals are not
def currentRivals(Lastname1,Firstname1,Lastname2,Firstname2):
    player1Teams = getTeams(Lastname1,Firstname1)
    current1Team = player1Teams[len(player1Teams)-1]
    player2Teams = getTeams(Lastname2,Firstname2)
    current2Team = player2Teams[len(player2Teams)-1]
    division1 = divs[current1Team]
    division2 = divs[current2Team]
    if division1 == division2 and current1Team != current2Team:
        return True
    return False

#determines if players are current teammates
def currentTeammates(Lastname1,Firstname1,Lastname2,Firstname2):
    player1Teams = getTeams(Lastname1,Firstname1)
    current1Team = player1Teams[len(player1Teams)-1]
    player2Teams = getTeams(Lastname2,Firstname2)
    current2Team = player2Teams[len(player2Teams)-1]
    if current1Team == current2Team:
        return True
    return False
    
#Determines if players are past rivals, ie they played on teams 
#that were divison rivals at the the same time
def pastRivals(Lastname1,Firstname1,Lastname2,Firstname2):
    player1Teams = getTeams(Lastname1,Firstname1)
    player1Teams = player1Teams[::-1]
    player2Teams = getTeams(Lastname2,Firstname2)
    player2Teams = player2Teams[::-1]
    player1Years = len(player1Teams)
    player2Years = len(player2Teams)
    if player1Years > player2Years:
        player1Teams = player1Teams[0:player2Years]
    if player2Years > player1Years:
        player2Teams = player2Teams[0:player1Years]
    for i in range(len(player1Teams)):
        team1 = player1Teams[i]
        team2 = player2Teams[i]
        if team1 != team2:
            if divs[team1] == divs[team2]:
                return True
    return False

#Determines if two players were ever past teamamtes
def pastTeammates(Lastname1,Firstname1,Lastname2,Firstname2):
    player1Teams = getTeams(Lastname1,Firstname1)
    player1Teams = player1Teams[::-1]
    player2Teams = getTeams(Lastname2,Firstname2)
    player2Teams = player2Teams[::-1]
    player1Years = len(player1Teams)
    player2Years = len(player2Teams)
    if player1Years > player2Years:
        player1Teams = player1Teams[0:player2Years]
    if player2Years > player1Years:
        player2Teams = player2Teams[0:player1Years]
    for i in range(len(player1Teams)):
        team1 = player1Teams[i]
        team2 = player2Teams[i]
        if team1 == team2:
            return True
    return False

#finds fantasy points based on standard scoring
def getRBPoints(lst):
    totalPoints = 0
    yards = int(lst[0][1]) + int(lst[3][1])
    totalPoints += yards*.1
    totalPoints += int(lst[2][1])
    tds = int(lst[1][1]) + int(lst[4][1])
    totalPoints += tds*6
    if len(lst) == 6:
        totalPoints -= 2*int(lst[5][1])
    return round(totalPoints,2)

#finds fantasy points based on standard scoring
def getWRTEPoints(lst):
    totalPoints = 0
    yards = int(lst[1][1]) 
    totalPoints += yards*.1
    totalPoints += int(lst[0][1])
    tds = int(lst[2][1]) 
    totalPoints += tds*6
    if len(lst) == 4:
        totalPoints -= 2*int(lst[3][1])
    return round(totalPoints,2)

#finds fantasy points based on standard scoring
def getQBPoints(lst):
    totalPoints = 0
    yards = int(lst[0][1]) 
    totalPoints += yards*.04
    tds = int(lst[1][1]) + int(lst[4][1])
    totalPoints += tds*6
    rush = int(lst[3][1])
    totalPoints += rush*.1
    inter = int(lst[2][1])
    totalPoints -= 2*inter
    if len(lst) == 6:
        totalPoints -= 2*int(lst[5][1])
    return round(totalPoints,2)
     
    
################################################################################

def init(data):
    data.margin = 25
    data.recPos = 0
    data.radius = 25
    data.mode = "homeScreen"
    data.playerX = data.width/5
    data.playerY = data.height*4/5 -data.margin*2
    data.createX = data.width/5
    data.createY = data.height*2/5 -data.margin*2
    data.lineupX = data.width/5
    data.lineupY = data.height*3/5 -data.margin*2
    data.recX = data.width/5
    data.recY = data.height-data.radius -data.margin*2
    data.outline = 15
    data.cX = data.width - data.margin-data.outline
    data.cY = data.margin + data.outline
    data.bX = data.margin + data.radius
    data.bY = data.bX
    data.createBox=[]
    data.posList = ["QB","RB","RB","WR","WR","TE"]
    data.week = int(getCurrentWeek())
    data.totalScore = [0,0,0,0,0,0]
    data.pastPlayerStats = []
    data.pastPos = 0
    data.pastWeek = 0
    data.pastLineupWeek = 0
    data.pastLineupPlayers = []
    data.pastLineupChem = 0
    #loads reccomended defenses for all positions 
    data.rbMatchups = defenses("RB")
    data.wrMatchups = 0#defenses("WR")
    data.qbMatchups = 0#defenses("QB")
    data.teMatchups = defenses("TE")
    data.pastTotalScore = [0,0,0,0,0,0]
    data.chem = 1
    #checks to see if their is already a saved lineup/
    try:
        data.players = list(readFile(str(data.week)+".txt"))
    except:
        data.players = [0,0,0,0,0,0]
    #checks to see if their is already a saved chemistry
    try:
        data.chem = float(readFileChem(str(data.week)+"chem.txt"))
    except:
        data.chem = 1

#https://stackoverflow.com/questions/47166112/saving-
#lists-into-txt-python?noredirect=1&lq=1
def readFile(path):
    read_file = open(path,"r")
    my_list = json.load(read_file)
    return my_list
        
def createFile(lst):
    week = str(getCurrentWeek())
    file = open(week+".txt","w")
    json.dump(lst,file)

#https://www.guru99.com/reading-and-writing-files-in-python.html
def createFileChem(chem):
    week = int(getCurrentWeek())
    chemFile= open(str(week)+"chem.txt","w+")
    chemFile.write(chem)
    chemFile.close
    
def readFileChem(path):
    with open(path, "rt") as f:
        return f.read()

#finds the chemistry between two players
def getChemistry(Lastname1,Firstname1,Lastname2,Firstname2):
    chemFactor = 0
    a = getTeams(Lastname1,Firstname1)
    b = getTeams(Lastname2,Firstname2)
    a = a[::-1]
    b = b[::-1]
    if len(a) > len(b):
        a = a[0:len(b)]
    if len(b) > len(a):
        b = b[0:len(a)]
    for i in range(len(a)):
        if a[i] == b[i]:
            if i == 0:
                chemFactor +=.025
            else:
                chemFactor += .01
        elif divs[a[i]] == divs[b[i]]:
            if i == 0:
                chemFactor -= .025
            else:
                chemFactor -= .01
    return chemFactor
        
    

#calls MVC based on different screen player is on
def mousePressed(event, data):
    if (data.mode == "homeScreen"): homeScreenMousePressed(event, data)
    if (data.mode == "instructions"):instructionMousePressed(event, data)
    if (data.mode == "create"): createLineupMousePressed(event,data)
    if (data.mode == "past"): pastMousePressed(event,data)
    if (data.mode == "pastLineup"): pastLineupMousePressed(event,data)
    if (data.mode == "rec"): recMousePressed(event,data)
    if data.mode != "instructions":
        #can acess the instruction screen from anywhere in the game
        if event.x <= data.cX + data.radius and event.x >= data.cX-data.radius:
            if event.y <= data.cY +data.radius and event.y>=data.cY-data.radius:
                data.mode = "instructions"
    

def keyPressed(event, data):
    if (data.mode == "homeScreen"): homeScreenKeyPressed(event, data)
    if (data.mode == "instructions"):instructionKeyPressed(event, data)
    if (data.mode == "create"): createLineupKeyPressed(event,data)
    if (data.mode == "past"): pastKeyPressed(event,data)
    if (data.mode == "pastLineup"): pastLineupKeyPressed(event,data)
    if (data.mode == "rec"): recKeyPressed(event,data)

def timerFired(data):
    if (data.mode == "homeScreen"): homeScreenTimerFired(data)
    if (data.mode == "instructions"):instructionTimerFired(data)
    if (data.mode == "create"): createLineupTimerFired(data)
    if (data.mode == "past"): pastTimerFired(data)
    if (data.mode == "pastLineup"): pastLineupTimerFired(data)
    if (data.mode == "rec"): recTimerFired(data)
    

def redrawAll(canvas, data):
    #same backround for every screen
    canvas.create_rectangle(0,0,data.width,data.height,fill = "lawn green",
                                                outline = "white",width = 15)
    lineSpace = data.height//5
    for i in range(0,11):
        canvas.create_line(0,data.height - (lineSpace*i),
               data.width,data.height - (lineSpace*i),fill = "white",width = 15)
    if (data.mode == "homeScreen"): homeScreenRedrawAll(canvas, data)
    if (data.mode == "instructions"):instructionRedrawAll(canvas, data)
    if (data.mode == "create"): createLineupRedrawAll(canvas,data)
    if (data.mode == "past"): pastRedrawAll(canvas,data)
    if (data.mode == "pastLineup"): pastLineupRedrawAll(canvas,data)
    if (data.mode == "rec"): recRedrawAll(canvas,data)
    if data.mode != "instructions":
        canvas.create_oval(data.cX-data.radius,data.cY-data.radius,
                                        data.cX+data.radius,data.cY+data.radius)
        canvas.create_text(data.cX,data.cY,text="S",font="Times 30")
    

####################################
# homescreen mode
####################################


def homeScreenMousePressed(event, data):
    if event.x <= data.createX +data.radius and event.x >= data.createX-\
                                                                    data.radius:
        if event.y <= data.createY + data.radius and event.y >= data.createY-\
                                                                    data.radius:
            data.mode = "create"
    if event.x <= data.playerX + data.radius and event.x >= data.playerX-\
                                                                    data.radius:
        if event.y <= data.playerY + data.radius and event.y >= data.playerY-\
                                                                    data.radius:
            data.mode = "past"
    if event.x <= data.lineupX + data.radius and event.x >= data.lineupX-\
                                                                    data.radius:
        if event.y <= data.lineupY + data.radius and event.y >= data.lineupY-\
                                                                    data.radius:
            data.mode = "pastLineup"
    if event.x <= data.recX + data.radius and event.x >= data.recX-data.radius:
        if event.y <= data.recY + data.radius and event.y >= data.recY-\
                                                                    data.radius:
            data.mode = "rec"


def homeScreenKeyPressed(event, data):
    pass
    
def homeScreenTimerFired(data):
    pass

def homeScreenRedrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width,data.height,fill = "lawn green",
                                                outline = "white",width = 15)
    lineSpace = data.height//5
    for i in range(0,11):
        canvas.create_line(0,data.height - (lineSpace*i),
               data.width,data.height - (lineSpace*i),fill = "white",width = 15)
    #formats all of the button and mode positions
    canvas.create_text(data.width//2,data.height/4 - data.margin*2,
                                  text="Fantasy Football 2.0",font = "Times 30")
    canvas.create_rectangle(data.createX-data.radius,data.createY-data.radius,
                    data.createX+data.radius,data.createY+data.radius,width = 4)
    canvas.create_text(data.createX,data.createY,text="C",font="Times 30")
    canvas.create_text(data.width/2,data.createY,text="Create Lineup",
                                                                font="Times 30")
    
    canvas.create_rectangle(data.lineupX-data.radius,data.lineupY-data.radius,
                    data.lineupX+data.radius,data.lineupY+data.radius,width = 4)
    canvas.create_text(data.lineupX,data.lineupY,text="L",font="Times 30")
    canvas.create_text(data.width/2,data.lineupY,text="Lineups",font="Times 30")
    
    canvas.create_rectangle(data.playerX-data.radius,data.playerY-data.radius,
                    data.playerX+data.radius,data.playerY+data.radius,width = 4)
    canvas.create_text(data.playerX,data.playerY,text="P",font="Times 30")
    canvas.create_text(data.width/2,data.playerY,text="Player Stats",
                                                                font="Times 30")
                                                                
    canvas.create_rectangle(data.recX-data.radius,data.recY-data.radius,
                    data.recX+data.radius,data.recY+data.radius,width = 4)
    canvas.create_text(data.recX,data.recY,text="R",font="Times 30")
    canvas.create_text(data.width/2,data.recY,text="Recomendations",
                                                                font="Times 30")
                    
####################################
#rec screen
####################################
def recMousePressed(event, data):
    if event.x <= data.bX + data.radius and event.x >= data.bX-data.radius:
        if event.y <= data.bY + data.radius and event.y >= data.bY-data.radius:
            data.mode = "homeScreen"
    if event.x <= data.width/2 + data.radius and event.x >= data.width/2-\
                                                                    data.radius:
        if event.y <= data.bY + data.radius and event.y >= data.bY-data.radius:
            #https://www.python-course.eu/tkinter_entry_widgets.php
            #creates an entry box if button is pressed
            master = Tk()
            Label(master, text="Position").grid(row=0)
            e1 = Entry(master)
            e1.grid(row=0, column=1)
            Button(master, text='Enter', command=master.quit).grid(row=3, 
                                                    column=0, sticky=W, pady=4)
            mainloop()
            data.recPos = e1.get()


def recKeyPressed(event, data):
    pass
    

def recTimerFired(data):
    pass

def recRedrawAll(canvas, data):
    canvas.create_rectangle(data.bX-data.radius,data.bY-data.radius,
                                        data.bX+data.radius,data.bY+data.radius)
    canvas.create_text(data.bX,data.bY,text="B",font="Times 30")
    canvas.create_rectangle(data.width/2-data.radius,data.bY-data.radius,
                                data.width/2+data.radius,data.bY+data.radius)
    canvas.create_text(data.width/2,data.bY,text="R",font="Times 30")
    canvas.create_text(data.width/2,data.height/5,text = "Start 'em",
                                            font = "Times 30",fill = "Green")
    canvas.create_text(data.width/2,data.height/2,text = "Sit 'em",
                                            font = "Times 30",fill = "Red")
    #finds the correct defense based on the position that was entered
    if data.recPos == "QB":
        canvas.create_text(data.width/3,data.height/5+data.radius*4,
                    text = data.qbMatchups[0],font = "Times 23",fill = "Green")
        canvas.create_text(data.width*2/3,data.height/5+data.radius*4,
                    text = data.qbMatchups[1],font = "Times 23",fill = "Green")
        canvas.create_text(data.width/3,data.height/2+data.radius*4,
                    text = data.qbMatchups[2],font = "Times 23",fill = "Red")
        canvas.create_text(data.width*2/3,data.height/2+data.radius*4,
                    text = data.qbMatchups[3],font = "Times 23",fill = "Red")
    if data.recPos == "RB":
        canvas.create_text(data.width/3,data.height/5+data.radius*4,
                    text = data.rbMatchups[0],font = "Times 23",fill = "Green")
        canvas.create_text(data.width*2/3,data.height/5+data.radius*4,
                    text = data.rbMatchups[1],font = "Times 23",fill = "Green")
        canvas.create_text(data.width/3,data.height/2+data.radius*4,
                    text = data.rbMatchups[2],font = "Times 23",fill = "Red")
        canvas.create_text(data.width*2/3,data.height/2+data.radius*4,
                    text = data.rbMatchups[3],font = "Times 23",fill = "Red")
    if data.recPos == "TE":
        canvas.create_text(data.width/3,data.height/5+data.radius*4,
                    text = data.teMatchups[0],font = "Times 23",fill = "Green")
        canvas.create_text(data.width*2/3,data.height/5+data.radius*4,
                    text = data.teMatchups[1],font = "Times 23",fill = "Green")
        canvas.create_text(data.width/3,data.height/2+data.radius*4,
                    text = data.teMatchups[2],font = "Times 23",fill = "Red")
        canvas.create_text(data.width*2/3,data.height/2+data.radius*4,
                    text = data.teMatchups[3],font = "Times 23",fill = "Red")
    if data.recPos == "WR":
        canvas.create_text(data.width/3,data.height/5+data.radius*4,
                    text = data.wrMatchups[0],font = "Times 23",fill = "Green")
        canvas.create_text(data.width*2/3,data.height/5+data.radius*4,
                    text = data.wrMatchups[1],font = "Times 23",fill = "Green")
        canvas.create_text(data.width/3,data.height/2+data.radius*4,
                    text = data.wrMatchups[2],font = "Times 23",fill = "Red")
        canvas.create_text(data.width*2/3,data.height/2+data.radius*4,
                    text = data.wrMatchups[3],font = "Times 23",fill = "Red")
        

####################################
# instruction screen
####################################
def instructionMousePressed(event, data):
    if event.x <= data.bX + data.radius and event.x >= data.bX-data.radius:
        if event.y <= data.bY + data.radius and event.y >= data.bY-data.radius:
            data.mode = "homeScreen"


def instructionKeyPressed(event, data):
    pass
    

def instructionTimerFired(data):
    pass

def instructionRedrawAll(canvas, data):
    canvas.create_rectangle(data.bX-data.radius,data.bY-data.radius,
                                        data.bX+data.radius,data.bY+data.radius)
    canvas.create_text(data.bX,data.bY,text="B",font="Times 30")
    canvas.create_text(data.width/2,data.height/10,text="Scoring Rules",
                                                                font="Times 40")
    canvas.create_text(data.width/2,data.height/2,
    text = "TD: 6 Pts\nRec: 1 Pt\nRush YD: 0.1 Pts\nRec YD: 0.1 Pts\nPass YD:"+ 
    "0.04 Pts\nFum: -2 Pts\nInt: -2 Pts", font = "Times 25")
    
    
####################################
#create lienup screen
####################################
def createLineupMousePressed(event, data):
    if event.x <= data.bX + data.radius and event.x >= data.bX-data.radius:
        if event.y <= data.bY + data.radius and event.y >= data.bY-data.radius:
            data.mode = "homeScreen"
    #fixes bug crashes on first click
    if len(data.createBox) != 0:
        for i in range(len(data.posList)):
            tupe = data.createBox[i]
            cX = tupe[0]
            cY = tupe[1]
            if event.x <= cX + data.radius and event.x >= cX-data.radius:
                if event.y <= cY + data.radius and event.y >= cY-data.radius:
                    #if you click on a position gives option to enter player
                    #https://www.python-course.eu/tkinter_entry_widgets.php
                    master = Tk()
                    Label(master, text="First Name").grid(row=0)
                    Label(master, text="Last Name").grid(row=1)
                    e1 = Entry(master)
                    e2 = Entry(master)
                    e1.grid(row=0, column=1)
                    e2.grid(row=1, column=1)
                    Button(master, text='Enter', 
                    command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
                    mainloop()
                    first = e1.get()
                    last = e2.get()
                    position = data.posList[i]
                    tmpPosition = getPosition(last,first)
                    #makes sure the player is in nfl and at that position
                    if position == tmpPosition:
                        bye = getBye(last,first)
                        data.players[i] = (last,first,cY,bye)
                    else:
                        print("Wrong Position")
    if event.x <= data.width/2 + 2*data.radius and event.x >= data.width/2-\
                                                                2*data.radius:
        if event.y <= data.height and event.y >= data.height-2*data.margin:
            #finds chemistry between all positions
            createFile(data.players)
            chemistry = 1
            for i in range(len(data.players)):
                for j in range(len(data.players)):
                    if data.players[i] != 0 and data.players[j] != 0:
                        last1 = data.players[i][0]
                        last2 = data.players[j][0]
                        first1 = data.players[i][1]
                        first2 = data.players[j][1]
                        #fixes bug that takes chemistry of same player
                        if last1 != last2: 
                            chem = getChemistry(last1,first1,last2,first2)
                            chemistry += chem
            data.chem = round(chemistry,2)
            createFileChem(str(data.chem))
    

def createLineupKeyPressed(event, data):
    pass

def createLineupTimerFired(data):
    pass

def createLineupRedrawAll(canvas, data):
    canvas.create_text(data.width/2,data.height/10,text="Create Lineup",
                                                                font="Times 40")
    space = 60
    for i in range(len(data.posList)):
        #creates the position boxes 
        cX = data.margin + data.radius
        cY = data.margin + data.radius +(space*i) +data.height/5
        canvas.create_rectangle(cX-data.radius,cY-data.radius,
                                                cX+data.radius,cY+data.radius)
        canvas.create_text(cX,cY,text=data.posList[i],font = "Times 20")
        data.createBox.append((cX,cY))
    canvas.create_rectangle(data.bX-data.radius,data.bY-data.radius,
                                        data.bX+data.radius,data.bY+data.radius)
    canvas.create_text(data.bX,data.bY,text="B",font="Times 30")
    for i in range(len(data.players)):
        #adds all legit players to the screen along with their 
        #fantasy points for that week
        if data.players[i] != 0:
            tupe = data.players[i]
            canvas.create_text(data.width/2,tupe[2],text= tupe[1] +" "+tupe[0],
                                                            font = "Times 20") 
            if data.posList[i] == "QB":
                if tupe[3] < data.week:
                    lst = getWeekStats(tupe[0],tupe[1],data.week-1)
                elif tupe[3] >= data.week:
                    lst = getWeekStats(tupe[0],tupe[1],data.week)
                if len(lst[0][1]) > 2:
                    points = 0
                else:
                    points = getQBPoints(cleanQBStats(lst))
                    data.totalScore[i] = points
                canvas.create_text(data.cX,tupe[2],text = str(points),
                                                            font = "Times 20")
            if data.posList[i] == "RB":
                if tupe[3] < data.week:
                    lst = getWeekStats(tupe[0],tupe[1],data.week-1)
                elif tupe[3] >= data.week:
                    lst = getWeekStats(tupe[0],tupe[1],data.week)
                
                if len(lst[0][1]) > 2:
                    points = 0
                else:
                    points = getRBPoints(cleanRBStats(lst))
                    data.totalScore[i] = points
                canvas.create_text(data.cX,tupe[2],text = str(points),
                                                            font = "Times 20")
            if data.posList[i] == "WR" or data.posList[i] == "TE":
                if tupe[3] < data.week:
                    lst = getWeekStats(tupe[0],tupe[1],data.week-1)
                elif tupe[3] >= data.week:
                    lst = getWeekStats(tupe[0],tupe[1],data.week)
                if len(lst[0][1]) > 2:
                    points = 0
                else:
                    points = getWRTEPoints(cleanWRTEStats(lst))
                    data.totalScore[i] = points
                canvas.create_text(data.cX,tupe[2],text = str(points),
                                                            font = "Times 20")
                                                            
            
    canvas.create_text(data.cX,data.cY+data.radius+data.margin,
                                                text = "PTS",font = "Times 20")
                                                
    canvas.create_text(data.cX,data.height-data.radius-data.margin,
                                text=str(round(sum(data.totalScore)*data.chem
                                    ,1)),font="Times 20")
    canvas.create_text(data.cX,data.height-data.radius,
                                    text=str(data.chem),font="Times 20")
    canvas.create_text(data.bX+data.margin,data.height-data.radius,
                                    text="Chemistry",font="Times 20")
    canvas.create_rectangle(data.width/2-(2*data.radius),
                       data.height-(2*data.margin),data.width/2+(2*data.radius),
                                                    data.height)
    canvas.create_text(data.width/2,data.height-data.radius,text="Save",
                                                                font="Times 25")

####################################
#past palyer stats
####################################    
def pastMousePressed(event, data):
    if event.x <= data.bX + data.radius and event.x >= data.bX-data.radius:
        if event.y <= data.bY + data.radius and event.y >= data.bY-data.radius:
            data.mode = "homeScreen"
    #finds player stats for a given week based on input
    if event.x <= data.width/2 + data.radius and event.x >= data.width/2-\
                                                                    data.radius:
        if event.y <= data.height*9/10 + data.radius and event.y >= data.height\
                                                            *9/10-data.radius:
            #https://www.python-course.eu/tkinter_entry_widgets.php
            master = Tk()
            Label(master, text="First Name").grid(row=0)
            Label(master, text="Last Name").grid(row=1)
            Label(master, text="Week").grid(row=2)
            e1 = Entry(master)
            e2 = Entry(master)
            e3 = Entry(master)
            e1.grid(row=0, column=1)
            e2.grid(row=1, column=1)
            e3.grid(row=2, column=1)
            Button(master, text='Enter', command=master.quit).grid(row=3, 
                                                    column=0, sticky=W, pady=4)
            mainloop()
            first = e1.get()
            last = e2.get()
            data.pastWeek= int(e3.get())
            position  = str(getPosition(last,first))
            bye = int(getBye(last,first))
            data.pastPos = position
            if data.pastWeek == bye:
                print("Sorry the player didnt play that week.")
            else:
                #calls correct stats formatting based on player position
                if position == "QB":
                    if bye < data.pastWeek:
                        stats = getWeekStats(last,first,data.pastWeek-1)
                    elif bye >= data.pastWeek:
                        stats = getWeekStats(last,first,data.pastWeek)
                    stats = cleanQBStats(stats)
                    data.pastPlayerStats = stats
                elif position == "RB":
                    if bye < data.pastWeek:
                        stats = getWeekStats(last,first,data.pastWeek-1)
                    elif bye >= data.pastWeek:
                        stats = getWeekStats(last,first,data.pastWeek)
                    stats = cleanRBStats(stats)
                    data.pastPlayerStats = stats
                elif position == "WR" or position == "TE":
                    if bye < data.pastWeek:
                        stats = getWeekStats(last,first,data.pastWeek-1)
                    elif bye >= data.pastWeek:
                        stats = getWeekStats(last,first,data.pastWeek)
                    stats = cleanWRTEStats(stats)
                    data.pastPlayerStats = stats
                else:
                    print("No Player Found")
    

def pastKeyPressed(event,data):
    pass
        
def pastTimerFired(data):
    pass

def pastRedrawAll(canvas, data):
    canvas.create_rectangle(data.bX-data.radius,data.bY-data.radius,
                                        data.bX+data.radius,data.bY+data.radius)
    canvas.create_text(data.bX,data.bY,text="B",font="Times 30")
    canvas.create_rectangle(data.width/2-data.radius,
                        data.height*9/10-data.radius,data.width/2+data.radius,
                                                data.height*9/10 +data.radius)
    canvas.create_text(data.width/2,data.height*9/10,text="P",font="Times 30")
    
    if data.pastWeek != 0:
        #prints player formated stats based on position
        canvas.create_text(data.width/2,data.height/10,
                            text = "Week"+str(data.pastWeek),font = "Times 30")
        if data.pastPos == "QB":
            points = getQBPoints(data.pastPlayerStats)
            canvas.create_text(data.width/2,data.height/5,
                                    text=str(points)+" PTS",font = "Times 25")
        if data.pastPos == "RB":
            points = getRBPoints(data.pastPlayerStats)
            canvas.create_text(data.width/2,data.height/5,
                                    text=str(points)+" PTS",font = "Times 25")
        if data.pastPos == "WR" or data.pastPos == "TE":
            points = getWRTEPoints(data.pastPlayerStats)
            canvas.create_text(data.width/2,data.height/5,
                                    text=str(points)+" PTS",font = "Times 25")
    space = 50
    if data.pastPlayerStats != []:
        for i in range(len(data.pastPlayerStats)):
            canvas.create_text(data.width/3,200 + space*i,
                            text = data.pastPlayerStats[i][0],font = "Times 20")
            canvas.create_text(2*data.width/3,200 + space*i,
                            text = data.pastPlayerStats[i][1],font = "Times 20")

####################################
#past lineups
####################################        
def pastLineupMousePressed(event, data):
    if event.x <= data.bX + data.radius and event.x >= data.bX-data.radius:
        if event.y <= data.bY + data.radius and event.y >= data.bY-data.radius:
            data.mode = "homeScreen"
    if event.x <= data.width/2 + data.radius and event.x >= data.width/2-\
                                                                    data.radius:
        if event.y <= data.bY + data.radius and event.y >= data.bY-data.radius:
            #https://www.python-course.eu/tkinter_entry_widgets.php
            master = Tk()
            Label(master, text="Week").grid(row=0)
            e1 = Entry(master)
            e1.grid(row=0, column=1)
            Button(master, text='Enter', command=master.quit).grid(row=2, 
                                                    column=0, sticky=W, pady=4)
            mainloop()
            data.pastLineupWeek = int(e1.get())
            #searches to see if lineup exists
            try:
                data.pastLineupPlayers =list(readFile(str(data.pastLineupWeek)+\
                                                                        ".txt"))
                data.pastLineupChem = float(readFileChem(
                                        str(data.pastLineupWeek)+"chem.txt"))
            except:
                print("There was no Lineup found for that week!")


def pastLineupKeyPressed(event, data):
    pass
        
def pastLineupTimerFired(data):
    pass

def pastLineupRedrawAll(canvas, data):
    canvas.create_rectangle(data.bX-data.radius,data.bY-data.radius,
                                        data.bX+data.radius,data.bY+data.radius)
    canvas.create_rectangle(data.width/2-data.radius,data.bY-data.radius,
                                   data.width/2+data.radius,data.bY+data.radius)
    canvas.create_text(data.bX,data.bY,text="B",font="Times 30")
    canvas.create_text(data.width/2,data.bY,text="W",font="Times 30")
    space = 60
    if len(data.pastLineupPlayers) != 0:
        for i in range(len(data.posList)):
            #creates the position boxes 
            cX = data.margin + data.radius
            cY = data.margin + data.radius +(space*i) +data.height/5
            canvas.create_rectangle(cX-data.radius,
                                cY-data.radius,cX+data.radius,cY+data.radius)
            canvas.create_text(cX,cY,text=data.posList[i],font = "Times 20")
            data.createBox.append((cX,cY))
        for i in range(len(data.pastLineupPlayers)):
            if data.pastLineupPlayers[i] != 0:
                tupe = data.pastLineupPlayers[i]
                canvas.create_text(data.width/2,tupe[2],
                                text= tupe[1] +" "+tupe[0],font = "Times 20") 
                #draws the correcr lineup at their correct psotion boxes
                if data.posList[i] == "QB":
                    if tupe[3] < data.pastLineupWeek:
                        lst = getWeekStats(tupe[0],tupe[1],
                                                        data.pastLineupWeek-1)
                    elif tupe[3] >= data.pastLineupWeek:
                        lst = getWeekStats(tupe[0],tupe[1],data.pastLineupWeek)
                    if len(lst[0][1]) > 2:
                        points = 0
                    else:
                        points = getQBPoints(cleanQBStats(lst))
                        data.pastTotalScore[i] = points
                    canvas.create_text(data.cX,tupe[2],text = str(points),
                                                            font = "Times 20")
                if data.posList[i] == "RB":
                    if tupe[3] < data.pastLineupWeek:
                        lst = getWeekStats(tupe[0],tupe[1],
                                                        data.pastLineupWeek-1)
                    elif tupe[3] >= data.pastLineupWeek:
                        lst = getWeekStats(tupe[0],tupe[1],data.pastLineupWeek)
                    
                    if len(lst[0][1]) > 2:
                        points = 0
                    else:
                        points = getRBPoints(cleanRBStats(lst))
                        data.pastTotalScore[i] = points
                    canvas.create_text(data.cX,tupe[2],text = str(points),
                                                            font = "Times 20")
                if data.posList[i] == "WR" or data.posList[i] == "TE":
                    if tupe[3] < data.pastLineupWeek:
                        lst = getWeekStats(tupe[0],tupe[1],
                                                        data.pastLineupWeek-1)
                    elif tupe[3] >= data.pastLineupWeek:
                        lst = getWeekStats(tupe[0],tupe[1],data.pastLineupWeek)
                    if len(lst[0][1]) > 2:
                        points = 0
                    else:
                        points = getWRTEPoints(cleanWRTEStats(lst))
                        data.pastTotalScore[i] = points
                    canvas.create_text(data.cX,tupe[2],text = str(points),
                                                            font = "Times 20")
                                                            
            
    canvas.create_text(data.cX,data.cY+data.radius+data.margin,
                                                text = "PTS",font = "Times 20")
                                                
    canvas.create_text(data.cX,data.height-data.radius-data.margin,
                    text=str(round(sum(data.pastTotalScore)*data.pastLineupChem
                                    ,1)),font="Times 20")
    canvas.create_text(data.cX,data.height-data.radius,
                                text=str(data.pastLineupChem),font="Times 20")
    canvas.create_text(data.bX+data.margin,data.height-data.radius,
                                    text="Chemistry",font="Times 20")
    

####################################
# use the run function as-is
####################################

#https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Create root before calling init (so we can create images in init)
    root = Tk()
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600,600)