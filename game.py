# import pygame zero to get GUI
import pygame
import pgzrun
import sys
# import randint for rolling dice
from random import randint

# sets screen size
WIDTH = 1350
HEIGHT = 1000

# this part is commented out b/c no sprites yet & causes errors when trying to test if game works
# sets default location of sprites
p1 = Actor("player1")
p1.pos = 925, 925
p2 = Actor("player2")
p2.pos = 900, 950
p3 = Actor("player3")
p3.pos = 900, 1000
p4 = Actor("player4")
p4.pos = 900, 1050

# this variable checks if user in main menu or not; default is True to allow user to launch into the menu
main_menu = True

# this variable checks if a player's turn is ongoing
roll = False

# sets the location of some special places on the board
util = [12, 28]
jail = 30
luxtax = 38
inctax = 4
chance = [7, 22, 36]
community = [2, 17, 33]

# tracks turns left until out of jail
jailTurn = {1:0, 2:0, 3:0, 4:0}

# tracks the location of each player on the board
playerLoc = {1: 0, 2: 0, 3: 0, 4:0}

# tracks owner of properties; default is 0 b/c no one owns them
posOwn = {1:0, 3:0, 5:0, 6:0, 8:0, 9:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 18:0, 19:0, 21:0, 23:0, 24:0, 25:0, 26:0, 27:0,
          28:0, 29:0, 31:0, 32:0, 34:0, 35:0, 37:0, 39:0}

# static price of all properties
pricePos = {1:60, 3:60, 5:200, 6:100, 8:100, 9:120, 11:140, 12:150, 13:140, 14:160, 15:200, 16:180, 18:180, 19:200,
            21:220, 23:220, 24:240, 25:200, 26:260, 27:260, 28: 150, 29:280, 31:300, 32:300, 34:320, 35:200, 37:250,
            39:400}

# static name of all properties
posName = {1:"Mediterranean Avenue", 3:"Baltic Avenue", 5:"Reading Railroad", 6:"Vermont Avenue", 8:"Oriental Avenue",
            9:"Connecticut Avenue", 11:"St. Charles Place", 12:"Electric", 13:"States Avenue", 14:"Virginia Avenue ",
            15:"Pennsylvania Railroad", 16:"St. James Place", 18:"Tennessee Avenue", 19:"New York Avenue",
            21:"Kentucky Avenue ", 23:"Indiana Avenue", 24:"Illinois Avenue", 25:"B. & O. Railroad",
            26:"Atlantic Avenue", 27:"Ventnor Avenue", 28:"Water", 29:"Marvin Gardens", 31:"Pacific Avenue",
            32:"North Carolina Avenue", 34:"Pennsylvania Avenue", 35:"Short Line", 37:"Park Place ", 39:"Boardwalk"}

# dynamic price of rent on all properties (dependent on houses, hotels, etc.)
posRent = {1:2, 3:4, 5:25, 6:6, 8:6, 9:8, 11:10, 13:10, 14:12, 15:25, 16:14, 18:14, 19:16, 21:18, 23:18, 24:20, 25:25,
           26:22, 27:22, 29:24, 31:26, 32:26, 34:28, 35:25, 37:35, 39:50}

# tracks the amount of money each player has
money = {1: 1500, 2: 1500, 3: 1500, 4: 1500}

# tracks which player's turn it is; default is player 1
turn = 1

# tracks value of the dice roll
rollVal = int()

# tracks whether player can buy location or not; default is True because player should be able to buy all locations
buyStat = True

# tracks whether player can change a property's property; default is False because player cannot edit when they buy property
editPerm = False

# tracks whether player on income tax box or not; default False b/c player doesn't spawn on income tax box
income = False

# tracks community & chance cards; default False b/c don't have card yet
card = str()
getChance = False
getCommunity = False
chanceStuff = [50, -15, 150]
chanceVal = int()
communityStuff = [200, -50, 50, 100, 20, 100, -100, -50, 25, 10, 100]
communityVal = int()

# track if land on jail square or on free parking; default False b/c will be doing something sometime
nothing = False

# rolls dice with this function & updates location of each player
def diceRoll(usr):
    # rolls the dice
    global playerLoc, money
    roll1 = randint(1, 7)
    roll2 = randint(1, 7)
    # updates location of player
    playerLoc[usr] += roll1 + roll2
    if playerLoc[usr] > 39:
        playerLoc[usr] -= 40
        money[usr] += 200
    return roll1 + roll2

# creates the screen and allows user to play the game
def draw():
    global main_menu, roll
    # if the user is in the main menu
    if main_menu:
        # makes the background black and puts the title & message
        screen.fill("black")
        screen.draw.text("MONOPOLY", center=(625, 430), fontsize=70)
        box = Rect((450, 575), (350, 50))
        screen.draw.filled_rect(box, (255, 0, 0))
        screen.draw.text("Click here to begin", center=(625, 600), fontsize=50)
    # otherwise, draws the game board and the pieces
    else:
        screen.blit("board.jpg", (0, 0))
        p1.draw()
        p2.draw()
        p3.draw()
        p4.draw()
        screen.draw.text("Player 1: ${}".format(str(money[1])), center=(1150, 200), fontsize=50)
        screen.draw.text("Player 2: ${}".format(str(money[2])), center=(1150, 400), fontsize=50)
        screen.draw.text("Player 3: ${}".format(str(money[3])), center=(1150, 600), fontsize=50)
        screen.draw.text("Player 4: ${}".format(str(money[4])), center=(1150, 800), fontsize=50)
        # checks whether player needs to roll or not; if so, lets player roll dice
        if roll:
            if turn == 1:
                # creates two rectangles (the background & the button box)
                box = Rect((200,300), (600, 400))
                screen.draw.filled_rect(box, (0,150,0))
                button = Rect((400, 500), (200, 100))
                screen.draw.filled_rect(button, (0,0,0))
                # writes whose turn it is and the button to roll
                screen.draw.text("Player 1's turn to roll the dice", center=(500, 350), fontsize=50)
                screen.draw.text("ROLL", center=(500, 550), fontsize=45)
            elif turn == 2:
                box = Rect((200,300), (600, 400))
                screen.draw.filled_rect(box, (0,150,0))
                button = Rect((400, 500), (200, 100))
                screen.draw.filled_rect(button, (0,0,0))
                screen.draw.text("Player 2's turn to roll the dice", center=(500, 350), fontsize=50)
                screen.draw.text("ROLL", center=(500, 550), fontsize=45)
            elif turn == 3:
                box = Rect((200,300), (600, 400))
                screen.draw.filled_rect(box, (0,150,0))
                button = Rect((400, 500), (200, 100))
                screen.draw.filled_rect(button, (0,0,0))
                screen.draw.text("Player 3's turn to roll the dice", center=(500, 350), fontsize=50)
                screen.draw.text("ROLL", center=(500, 550), fontsize=45)
            elif turn == 4:
                box = Rect((200,300), (600, 400))
                screen.draw.filled_rect(box, (0,150,0))
                button = Rect((400, 500), (200, 100))
                screen.draw.filled_rect(button, (0,0,0))
                screen.draw.text("Player 4's turn to roll the dice", center=(500, 350), fontsize=50)
                screen.draw.text("ROLL", center=(500, 550), fontsize=45)
        # otherwise, player needs to do something -> pay rent, buy property, etc.
        else:
            box = Rect((100, 300), (800, 400))
            screen.draw.filled_rect(box, (200, 0, 0))
            if income:
                screen.draw.text("INCOME TAX: Choose from below", center=(500, 350),
                                 fontsize=50)
                percent = Rect((275, 500), (200, 100))
                screen.draw.filled_rect(percent, (0, 0, 0))
                hard = Rect((525, 500), (200, 100))
                screen.draw.filled_rect(hard, (0, 0, 0))
                screen.draw.text("10%", center=(375, 550), fontsize=45)
                screen.draw.text("200", center=(625, 550), fontsize=45)
            elif getChance or getCommunity:
                screen.draw.text("{}".format(card), center=(500, 350), fontsize=50)
                button = Rect((400, 500), (200, 100))
                screen.draw.filled_rect(button, (0, 0, 0))
                screen.draw.text("DO IT", center=(500, 550), fontsize=45)
            elif nothing:
                screen.draw.text("You don't have to do anything", center=(500, 350), fontsize=50)
                button = Rect((400, 500), (200, 100))
                screen.draw.filled_rect(button, (0, 0, 0))
                screen.draw.text("PASS", center=(500, 550), fontsize=45)
            elif buyStat:
                screen.draw.text("Would you like to buy {}?".format(posName[playerLoc[turn]]), center=(500, 350),
                                 fontsize=50)
                buy = Rect((275, 500), (200, 100))
                screen.draw.filled_rect(buy, (0, 0, 0))
                no = Rect((525, 500), (200, 100))
                screen.draw.filled_rect(no, (0, 0, 0))
                screen.draw.text("BUY", center=(375, 550), fontsize=45)
                screen.draw.text("NO", center=(625, 550), fontsize=45)
            elif not buyStat and editPerm:
                house = Rect((275, 500), (200, 100))
                screen.draw.filled_rect(house, (0, 0, 0))
                no = Rect((525, 500), (200, 100))
                screen.draw.filled_rect(no, (0, 0, 0))
                screen.draw.text("What would you like to do to {}?".format(posName[playerLoc[turn]]), center=(500, 350),
                                 fontsize=50)
                screen.draw.text("HOUSE", center=(375, 550), fontsize=45)
                screen.draw.text("NOTHING", center=(625, 550), fontsize=45)
            elif not buyStat and not editPerm:
                screen.draw.text("You need to pay Player {} ${}".format(str(posOwn[playerLoc[turn]]),
                                                                           str(posRent[playerLoc[turn]])),
                                 center=(500, 350),fontsize=50)
                button = Rect((400, 500), (200, 100))
                screen.draw.filled_rect(button, (0, 0, 0))
                screen.draw.text("PAY RENT", center=(500, 550), fontsize=45)

# code to check whether new position is owned or not & checks if player can change the location's propertiess
def checkOwn(usr):
    global buyStat, editPerm, jailTurn, playerLoc, income, card, getChance, getCommunity, nothing, chanceVal, \
        communityVal
    pos = playerLoc[usr]
    if playerLoc[usr] in util:
        roll = randint(1, 7) + randint(1, 7)
        if not posOwn[pos]:
            buyStat = True
            editPerm = False
        elif posOwn[pos] == turn:
            buyStat = False
            editPerm = False
        elif posOwn[12] == posOwn[28] and posOwn[12] != 0:
            buyStat = False
            editPerm = False
            posRent[pos] = roll * 10
        elif posOwn[12] != posOwn[28]:
            buyStat = False
            editPerm = False
            posRent[pos] = roll * 7
    elif playerLoc[usr] == jail:
        playerLoc[usr] = 10
        jailTurn[usr] = 3
    elif playerLoc[usr] == luxtax:
        money[usr] -= 100
    elif playerLoc[usr] == inctax:
        income = True
    elif playerLoc[usr] in chance:
        file = open("chance.txt")
        x = file.readlines()
        def removelast(txt):
            return txt[:-1]
        cards = list(map(removelast, x))
        k = randint(0, len(cards) - 1)
        card = cards[k]
        getChance = True
        chanceVal = k
    elif playerLoc[usr] in community:
        file = open("community.txt")
        x = file.readlines()
        def removelast(txt):
            return txt[:-1]
        cards = list(map(removelast, x))
        k = randint(0, len(cards) - 1)
        card = cards[k]
        communityVal = k
        getCommunity = True
    elif pos == 10 or pos == 20:
        nothing = True
    elif not posOwn[pos]:
        if pricePos[pos] <= money[usr]:
            buyStat = True
            editPerm = False
        else:
            buyStat = False
            editPerm = False
    elif posOwn[pos] == usr:
        buyStat = False
        editPerm = True
    else:
        buyStat = False
        editPerm = False

# checks when mouse is clicked
def on_mouse_down(pos):
    global main_menu, roll, rollVal, turn, posOwn, posRent, getChance, getCommunity, buyStat, editPerm, nothing, income
    # checks where the player clicks to launch the game when in main menu
    if main_menu:
        if 550 <= pos[0] <= 700:
            if 500 <= pos[1] <= 700:
                main_menu = False
                roll = True
    # otherwise, needs to check a bunch of stuff to know what each click does
    else:
        # if a player hasn't rolled their dice yet, let them roll dice
        if roll:
            # turn signifies which player's turn it is
            if turn == 1:
                if 400 <= pos[0] <= 600:
                    if 500 <= pos[1] <= 600:
                        rollVal = diceRoll(1)
                        checkOwn(1)
                        roll = False
            elif turn == 2:
                if 400 <= pos[0] <= 600:
                    if 500 <= pos[1] <= 600:
                        rollVal = diceRoll(2)
                        checkOwn(2)
                        roll = False
            elif turn == 3:
                if 400 <= pos[0] <= 600:
                    if 500 <= pos[1] <= 600:
                        rollVal = diceRoll(3)
                        checkOwn(3)
                        roll = False
            elif turn == 4:
                if 400 <= pos[0] <= 600:
                    if 500 <= pos[1] <= 600:
                        rollVal = diceRoll(4)
                        checkOwn(4)
                        roll = False
        # if player needs to do some action, let them do it
        else:
            if income:
                if 275 <= pos[0] <= 475:
                    if 500 <= pos[1] <= 600:
                        k = money[turn]/10
                        k = int(k)
                        money[turn] -= k
                        if turn + 1 > 4:
                            turn = 1
                        else:
                            turn += 1
                        roll = True
                        income = False
                elif 525 <= pos[0] <= 725:
                    if 500 <= pos[1] <= 600:
                        money[turn] -= 200
                        if turn + 1 > 4:
                            turn = 1
                        else:
                            turn += 1
                        roll = True
                        income = False
            elif getChance:
                if 400 <= pos[0] <= 600:
                    if 500 <= pos[1] <= 600:
                        money[turn] += chanceStuff[chanceVal]
                        if turn + 1 > 4:
                            turn = 1
                        else:
                            turn += 1
                        roll = True
                        getChance = False
            elif getCommunity:
                if 400 <= pos[0] <= 600:
                    if 500 <= pos[1] <= 600:
                        money[turn] += communityStuff[communityVal]
                        if turn + 1 > 4:
                            turn = 1
                        else:
                            turn += 1
                        roll = True
                        getCommunity = False
            elif nothing:
                if 400 <= pos[0] <= 600:
                    if 500 <= pos[1] <= 600:
                        if turn + 1 > 4:
                            turn = 1
                        else:
                            turn += 1
                        roll = True
                        nothing = False
            elif buyStat:
                if 275 <= pos[0] <= 475:
                    if 500 <= pos[1] <= 600:
                        money[turn] -= pricePos[playerLoc[turn]]
                        posOwn[playerLoc[turn]] = turn
                        if turn + 1 > 4:
                            turn = 1
                        else:
                            turn += 1
                        roll = True
                        buyStat = False
                elif 525 <= pos[0] <= 725:
                    if 500 <= pos[1] <= 600:
                        if turn + 1 > 4:
                            turn = 1
                        else:
                            turn += 1
                        roll = True
                        buyStat = False
            elif not buyStat and editPerm:
                if 275 <= pos[0] <= 475:
                    if 500 <= pos[1] <= 600:
                        money[turn] -= 100
                        posRent[playerLoc[turn]] += 50
                        if turn + 1 > 4:
                            turn = 1
                        else:
                            turn += 1
                        roll = True
                        buyStat = False
                        editPerm = False
                elif 525 <= pos[0] <= 725:
                    if 500 <= pos[1] <= 600:
                        if turn + 1 > 4:
                            turn = 1
                        else:
                            turn += 1
                        roll = True
                        buyStat = False
                        editPerm = False
            elif not buyStat and not editPerm:
                if 400 <= pos[0] <= 600:
                    if 500 <= pos[1] <= 600:
                        money[turn] -= posRent[playerLoc[turn]]
                        money[posOwn[playerLoc[turn]]] += posRent[playerLoc[turn]]
                        if turn + 1 > 4:
                            turn = 1
                        else:
                            turn += 1
                        roll = True
                        buyStat = False
                        editPerm = False

# runs the game
pgzrun.go()