#!/usr/bin/env python
# coding: utf-8

# In[6]:

import time


class Node:
    def __init__(self, chips, turnp, children=[]):
        self.chips = chips
        self.turnp = turnp
        self.children = children
        self.mmv = None


class Player:
    def __init__(self, value):
        self.value = value


class Agent(Player):
    def __init__(self, value, depth=False):
        self.rootn = False  # root node for storing tree
        self.depth = depth
        self.value = value

    def makemove(self, nchips, depth=-1):
        # calc tree on player's first turn
        re = Node(nchips, self.value)
        # print(re.chips)
        # depth-limited search
        if depth > 0:
            re = self.gentreebydepth(re, self.value, depth)
            # print("Children of ", re.chips, ": ")
            # i=0
            # for c in re.children[:20]:
            #       #print(i, c.chips, c.mmv)
            #      i+=1
            re = self.calcbestmove(re)
        # complete tree search
        else:
            if not self.rootn:
                # create entire game tree from agent's first turn
                self.rootn = self.gentree(re, self.value)
                # print("Children of ", self.rootn.chips, ": ")
                # i=0
                # for c in self.rootn.children[:20]:
                #   #print(i, c.chips, c.mmv)
                #  i+=1
                re = self.calcbestmove(self.rootn)
            else:
                currnode = self.searchnextlvl(self.rootn, nchips)
                # print("Children of ", currnode.chips, ": ")
                # i=0
                # for c in currnode.children[:20]:
                #   #print(i, c.chips, c.mmv)
                #  i+=1
                re = self.calcbestmove(currnode)

        self.rootn = re
        return re

    def searchnextlvl(self, rootn, qry):
        res = False
        for ch in rootn.children:
            # print(qry,"?=" , ch)
            if qry == ch.chips:
                res = ch
                break
        return res

    def calc_moves(self, nchips):
        moveset = []

        if nchips < 1:
            return

        for i in (1, 2, 3):
            if nchips-i >= 0:
                moveset.append(nchips-i)
        # print(moveset)
        return moveset

    def calcbestmove(self, node):
        # print("calculating best move - parents chips: ", node.chips)
        bestmove = node.children[0]
        # for c in node.children:
        # print(c.chips,c.mmv)
        if len(node.children) > 1:  # calcbestmove if more than 1 possible move
            remainc = node.children[1:]
            if node.turnp == 'p1':
                # check minimax value of children nodes to determine best move
                for c in remainc:
                    if c.mmv > bestmove.mmv:
                        bestmove = c
                        # print(bestmove.chips)
            elif node.turnp == 'p2':
                for c in remainc:
                    if c.mmv < bestmove.mmv:
                        bestmove = c
                        # print(bestmove.chips)
        # print("Returning best move: ", bestmove.chips)
        return bestmove

    def calc_minimax(self, node):
        ef = 0
        c = node.chips

        if c == 0:
            if node.turnp == 'p1':
                ef = -10
            elif node.turnp == 'p2':
                ef = 10

        elif c < 4:
            if node.turnp == 'p1':
                ef = 9
            elif node.turnp == 'p2':
                ef = -9

        elif c == 4:
            if node.turnp == 'p1':
                ef = -8
            elif node.turnp == 'p2':
                ef = 8

        # determine if 5,6,7...11,12,13... etc
        else:
            i = 0
            c -= 5
            while c > 2:
                c -= 3
                i += 1

            # if 5,6,7...11,12,13...17,18,19,
            if i % 2 == 1:
                if node.turnp == 'p1':
                    ef = 3
                elif node.turnp == 'p2':
                    ef = -3

            # if 8,9,10...14,15,16...20,21,22,
            else:
                if node.turnp == 'p1':
                    ef = -1
                elif node.turnp == 'p2':
                    ef = 1
        return ef

    def gentree(self, root, turnplayer):
        currnode = Node(root.chips, turnplayer)
        children = []
        mmv = currnode.mmv
        # if leaf node calc minimax value
        if currnode.chips < 1:
            mmv = self.calc_minimax(currnode)
        else:
            childl = self.calc_moves(currnode.chips)  # calculates children
            if childl:
                for m in childl:
                    childnode = Node(m, nextturn(turnplayer))
                    children.append(childnode)
                # calc children for each child
                for chn in range(len(children)):
                    children[chn] = self.gentree(
                        children[chn], nextturn(turnplayer))
                    tempchn = children[chn]
                    # calc mmv of currnode using mmv of chn
                    if turnplayer == 'p1':
                        if mmv is None:
                            mmv = tempchn.mmv
                        elif mmv < tempchn.mmv:
                            mmv = tempchn.mmv
                    if turnplayer == 'p2':
                        if mmv is None:
                            mmv = tempchn.mmv
                        elif mmv > tempchn.mmv:
                            mmv = tempchn.mmv
                    # print(currnode.mmv)
                currnode.children = children
            else:
                mmv = self.calc_minimax(currnode)

        currnode.mmv = mmv
        return currnode

    def gentreebydepth(self, root, turnplayer, depth):
        currnode = Node(root.chips, turnplayer)
        children = []
        mmv = currnode.mmv
        # if leaf node calc minimax value
        if currnode.chips < 1 or depth < 1:
            mmv = self.calc_minimax(currnode)
        else:
            childl = self.calc_moves(currnode.chips)  # calculates children
            # print("Children of ", currnode.chips ,childl)
            if childl:
                for m in childl:
                    # print("child: ", m)
                    childnode = Node(m, nextturn(turnplayer))
                    children.append(childnode)
                    # TODO: alpha-beta pruning
                # calc next depth
                for chn in range(len(children)):
                    children[chn] = self.gentreebydepth(children[chn],
                                                        nextturn(turnplayer),
                                                        depth-1)
                    tempchn = children[chn]
                    # calc mmv of currnode using mmv of chn
                    if turnplayer == 'p1':
                        if mmv is None:
                            mmv = tempchn.mmv
                        elif mmv < tempchn.mmv:
                            mmv = tempchn.mmv
                    elif turnplayer == 'p2':
                        if mmv is None:
                            mmv = tempchn.mmv
                        elif mmv > tempchn.mmv:
                            mmv = tempchn.mmv
                    # print("Added MMV for ", turnplayer,
                    # currnode.chips, ' MMV:', mmv)
                currnode.children = children
            else:
                mmv = self.calc_minimax(currnode)

        currnode.mmv = mmv
        return currnode


def nextturn(turnplayer):
    nextturn = None
    if turnplayer == 'p1':
        nextturn = 'p2'
    if turnplayer == 'p2':
        nextturn = 'p1'
    return nextturn


def playgame(player1, player2, nchips):
    # new game state
    turnp = player1
    chipstate = Node(nchips, turnp.value)
    turn = 0
    winner = None
    print("*****Play Game*****")

    # turn loop
    while chipstate.chips > 0:
        start = time.perf_counter()
        newstate = Node(chipstate.chips, turnp.value)
        print(newstate.chips, " chips left.")
        # agent moves
        if isinstance(turnp, Agent):
            print(turnp.value, "'s turn: ")
            print(turnp.value, " is making it's move...")
            if turnp.value == player1.value:
                if not turnp.depth:
                    newstate = player1.makemove(chipstate.chips)
                elif turnp.depth:
                    newstate = player1.makemove(chipstate.chips, turnp.depth)
                if newstate.chips < 1:
                    winner = turnp
                    break
                finish = time.perf_counter()
                print(turnp.value,
                      f"'s turn took {finish - start:0.4f} seconds")
                turnp = player2  # swap turn

            elif turnp.value == player2.value:
                if not turnp.depth:
                    newstate = player2.makemove(chipstate.chips)
                elif turnp.depth:
                    newstate = player2.makemove(chipstate.chips, turnp.depth)
                if newstate.chips < 1:
                    winner = turnp
                    break
                finish = time.perf_counter()
                print(turnp.value,
                      f"'s turn took {finish - start:0.4f} seconds")
                turnp = player1  # swap turn
            turn += 1

        # human's turn
        else:
            if turnp.value == player1.value:
                movemade = False
                while not movemade:
                    print("Make your move and remove a number of chips by entering a number from 1-3.")
                    move = input(">>> ")
                    move = int(move)
                    if move in (1, 2, 3):
                        newstate.chips -= move
                        movemade = True
                        print("You removed ", move, " chips.")
                    else:
                        print("Try again...")

                print(newstate.chips, " chips left.")
                if newstate.chips < 1:
                    winner = turnp
                    break
                finish = time.perf_counter()
                print(turnp.value,
                      f"'s turn took {finish - start:0.4f} seconds")
                turnp = player2  # swap turn
            elif turnp.value == player2.value:
                movemade = False
                while not movemade:
                    print(newstate.chips, " chips left.")
                    print("Make your move and remove a number of chips by entering a number from 1-3.")
                    move = input(">>> ")
                    move = int(move)
                    if move in (1, 2, 3):
                        newstate.chips -= move
                        movemade = True
                        print("You removed ", move, " chips.")
                    else:
                        print("Try again...")

                print(newstate.chips, " chips left.")
                if newstate.chips < 1:
                    winner = turnp
                    break
                finish = time.perf_counter()
                print(turnp.value,
                      f"'s turn took {finish - start:0.4f} seconds")
                turnp = player1  # swap turn
            turn += 1
        chipstate = newstate
    print(winner.value, " wins!")


def newgame():
    while True:
        player1 = Player('p1')
        player2 = Player('p2')

        print("*****Game Settings*****")
        print("Enter the number of chips you wish to play with: ")
        nchips = input(">>> ")
        nchips = int(nchips)

        print("Turn on Depth-Limited Search? type on/off and press Enter: ")
        dls = input(">>> ")
        dls = dls.lower()
        depth = None
        if dls == "on":
            print("Type a number and press Enter to set depth: ")
            depth = input(">>> ")
            while not depth.isnumeric:
                print("Please type a NUMBER and press Enter to set depth: ")
                depth = input(">>> ")
            depth = int(depth)
            print("Do you wish to make the first move? type yes/no and press Enter: ")
            fm = input(">>> ")
            fm = fm.lower()
            if fm == "yes":
                player2 = Agent("p2", depth)
                playgame(player1, player2, nchips)
                break  # remove for game to reset after finish
            elif fm == "no":
                player1 = Agent("p1", depth)
                playgame(player1, player2, nchips)
                break  # remove for game to reset after finish
            else:
                ("Please try again...")
        elif dls == "off":
            print("Do you wish to make the first move? type yes/no and press Enter: ")
            fm = input(">>> ")
            fm = fm.lower()
            if fm == "yes":
                player2 = Agent("p2")
                playgame(player1, player2, nchips)
                break  # remove for game to reset after finish
            elif fm == "no":
                player1 = Agent("p1")
                playgame(player1, player2, nchips)
                break  # remove for game to reset after finish
        else:
            print("Please try again...")

# In[8]:
# start timer
# start = time.perf_counter()


# setup game
# bobai = Agent('p1')
# steveai = Agent('p2')
# start game
# playgame(bobai, steveai, 28)

# test calc_minimax
# for i in range(9):
#     print('Minimax evalfunc: ', bobai.calc_minimax(Node([i],[])))
# bobai.gentree(bobai.root, 'o')
# bobai.gentreebydepth(bobai.root, 'x', 2)
# finish = time.perf_counter()
# print(f"Finished game in {finish - start:0.4f} seconds")
# print(f"Total processing time : {finish - start:0.4f} seconds")


newgame()
