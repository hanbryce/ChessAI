#!/usr/bin/env python
# coding: utf-8

# In[1]:


#pieces

class Piece:
    
    def __init__(self):
        self.color = None
        self.code = '-'
        self.moveset = []

    def __str__(self):
        return str(self.color)+" "+str(self.__class__.__name__)
        
class Pawn(Piece):
    def __init__(self):
        super().__init__()
        self.code = 'P'
        
    def new(color):
        s = __class__()
        s.color=color
        return s
    
    def mobility(self,game,pos):
        ix,iy = pos
        self.moveset=[]
        if game.turn%2==1:
            if iy+1<8:
                if ix+1<8:
                    if game.board[iy+1][ix+1].color=='White': self.moveset.append((1,1))
                if ix-1>=0:
                    if game.board[iy+1][ix-1].color=='White': self.moveset.append((-1,1))
            if game.board[iy+1][ix].color==None: self.moveset.append((0,1))
            if iy==1 and game.board[3][ix].color==None: self.moveset.append((0,2))
        else:
            if iy-1>=0:
                if ix+1<8:
                    if game.board[iy+1][ix+1].color=='Black': self.moveset.append((1,-1))
                if ix-1>=0:
                    if game.board[iy+1][ix-1].color=='Black': self.moveset.append((-1,-1))
                if game.board[iy-1][ix].color==None: self.moveset.append((0,-1))
                if iy==6 and game.board[4][ix].color==None: self.moveset.append((0,-2))
        return self.moveset
    
class Rook(Piece):
    def __init__(self):
        super().__init__()
        self.code = 'R'

    def new(color):
        s = Rook()
        s.color=color
        return s
    
    def mobility(self,game,pos):
        ix,iy = pos
        return straightCheck(game,pos)

class Bishop(Piece):
    def __init__(self):
        super().__init__()
        self.code = 'B'
    
    def new(color):
        s = __class__()
        s.color=color
        return s
    
    def mobility(self,game,pos):
        ix,iy = pos
        return diagonalCheck(game,pos)

class Knight(Piece):
    def __init__(self):
        super().__init__()
        self.code = 'N'
        
    def new(color):
        s = __class__()
        s.color=color
        return s

    def mobility(self,game,pos):
        ix,iy = pos
        self.moveset = [(-2,-1),(-1,2),(-2,1),(2,1),(2,-1),(1,2),(-1,-2),(1,-2)]
        return pointCheck(game,pos,self.moveset)

class Queen(Piece):
    def __init__(self):
        super().__init__()
        self.code = 'Q'
        
    def new(color):
        s = __class__()
        s.color=color
        return s
        
    def mobility(self,game,pos):
        ix,iy = pos
        return straightCheck(game,pos)+diagonalCheck(game,pos)

class King(Piece):
    def __init__(self):
        super().__init__()
        self.code = 'K'
        
    def new(color):
        s = __class__()
        s.color=color
        return s
    
    def mobility(self,game,pos):
        ix,iy = pos
        self.moveset = [(-1,-1),(-1,0),(-1,1),(0,1),(0,-1),(1,1),(1,0),(1,-1)]
        return pointCheck(game,pos,self.moveset)

class Empty(Piece) :
    def __init__(self):
        super().__init__()
        
    def new():
        s = __class__()
        return s
    
def straightCheck(game,pos):
    ix,iy = pos
    moveset = []
    #left side(-x)
    for i in range(1,ix+1):
        if game.board[iy][ix-i].color!=None:
            if game.board[iy][ix-i].color==game.opposite: moveset.append((-i,0))
            break
        moveset.append((-i,0))
    #right side(+x)
    for i in range(1,8-ix):
        if game.board[iy][ix+i].color!=None:
            if game.board[iy][ix+i].color==game.opposite: moveset.append((i,0))
            break
        moveset.append((i,0))
    #down side(-y)
    for i in range(1,iy+1):
        if game.board[iy-i][ix].color!=None:
            if game.board[iy-i][ix].color==game.opposite: moveset.append((0,-i))
            break
        moveset.append((0,-i))
    #up side(+y)
    for i in range(1,8-iy):
        if game.board[iy+i][ix].color!=None:
            if game.board[iy+i][ix].color==game.opposite: moveset.append((0,i))
            break
        moveset.append((0,i))
    return moveset

def diagonalCheck(game,pos):
    ix,iy = pos
    moveset = []
    #1st Quadrant(+x,+y)
    for i in range(1,min(8-ix,8-iy)):
        if game.board[iy+i][ix+i].color!=None:
            if game.board[iy+i][ix+i].color==game.opposite: moveset.append((i,i))
            break
        moveset.append((i,i)) 
    #2nd Quadrant(-x,+y)
    for i in range(1,min(ix+1,8-iy)):
        if game.board[iy+i][ix-i].color!=None:
            if game.board[iy+i][ix-i].color==game.opposite: moveset.append((-i,i))
            break
        moveset.append((-i,i)) 
    #3rd Quadrant(-x,-y)
    for i in range(1,min(ix+1,iy+1)):
        if game.board[iy-i][ix-i].color!=None:
            if game.board[iy-i][ix-i].color==game.opposite: moveset.append((-i,-i))
            break
        moveset.append((-i,-i))    
    #4th Quadrant(+x,-y)
    for i in range(1,min(8-ix,iy+1)):
        if game.board[iy-i][ix+i].color!=None:
            if game.board[iy-i][ix+i].color==game.opposite: moveset.append((i,-i))
            break
        moveset.append((i,-i))
    return moveset

def pointCheck(game,pos,moveset):
    ix,iy = pos
    newset = []
    for vector in moveset:
        x,y = vector
        if (not 0<=ix+x<8) or (not 0<=iy+y<8):
            continue
        if game.board[iy+y][ix+x].color==game.current:
            continue
        newset.append(vector)
    return newset


# In[2]:


#board

class Game:
    
    def __init__(self):
        self.board = []
        self.turn = 1
        self.current = 'Black'
        self.opposite = 'White'
        self.counter = 0
        
    def moveCheck(self,move):
        ix,iy,fx,fy = move
        pos = (ix,iy)
        initpos = self.board[iy][ix]
        finpos = self.board[fy][fx]
        vector = (fx-ix,fy-iy)
        if initpos.color==None or (initpos.color==self.opposite): return False
        if vector not in initpos.mobility(self,pos): return False
        return True

    def movePiece(self,move,show=True):
        ix,iy,fx,fy = move
        self.board[iy][ix],self.board[fy][fx]=self.board[fy][fx],self.board[iy][ix]
        if show: print('\nmoving',self.board[fy][fx],'\n...')
        if self.board[iy][ix].color!=None: 
            if show: print('\nremoved',self.board[iy][ix])
            self.board[iy][ix]=Empty.new()
        
def initBoard():
    
    line1 = [Rook.new('Black'),Knight.new('Black'),Bishop.new('Black'),Queen.new('Black'),King.new('Black'),Bishop.new('Black'),Knight.new('Black'),Rook.new('Black')]
    line2 = [Pawn.new('Black') for i in range(8)]
    linei = [[Empty.new() for j in range(8)] for i in range(4)]
    line7 = [Pawn.new('White') for i in range(8)]
    line8 = [Rook.new('White'),Knight.new('White'),Bishop.new('White'),Queen.new('White'),King.new('White'),Bishop.new('White'),Knight.new('White'),Rook.new('White')]
    board = [line1, line2, *linei, line7, line8]
    return board

def afterMove(game):
    game.turn+=1
    game.current,game.opposite=game.opposite,game.current


# In[3]:


import copy
import random

#ai 

class AInode(Game):
    
    def __init__(self,ref):
        super().__init__()
        self.__dict__=ref.__dict__.copy()
        self.board=copy.deepcopy(ref.board)
        self.pastmove = None
        self.parent=[]
        self.child=[]
        self.score=0
        
    def getChild(self,move):
        child = AInode(self)
        child.parent=[self]
        child.pastmove = move
        child.movePiece(move,False)
        afterMove(child)
        self.child.append(child)

def ai(game):
    base = AInode(game)
    createTree(base)
    game.movePiece(random.choice(base.child).pastmove)
    afterMove(game)

def createTree(node):
    for i in range(1):
        generateChilds(node)

def generateChilds(node):
    for i in range(8):
        for j in range(8):
            if node.board[j][i].color==node.current: 
                for move in node.board[j][i].mobility(node,(i,j)):
                    x,y = move
                    node.getChild((i,j,i+x,j+y))


# In[4]:


#main

from colorama import Fore, Style

def showBoard(game):
    print('\n')
    for i,line in reversed(list(enumerate(game.board))):
        for pos in line:
            if pos.color!='White': print(f'{pos.code:>3s}',end="")
            else: print(f'{Fore.YELLOW}{pos.code:>3s}{Style.RESET_ALL}', end="")
        print(f'{i+1:>6d}')
    print('\n\n  a  b  c  d  e  f  g  h\n')

def getInput():
    frominput = input("\nmove piece on: ")
    toinput = input("to: ")
    if(ord('a')<=ord(frominput[0])<=ord('h') and ord('a')<=ord(toinput[0])<=ord('h') and ord('0')<ord(frominput[1])<ord('9') and ord('0')<ord(toinput[1])<ord('9') and frominput != toinput):
        move = (ord(frominput[0])-ord('a'),int(frominput[1])-1,ord(toinput[0])-ord('a'),int(toinput[1])-1)
    else: 
        print("\nWrong input, type again")
        move = getInput()
    return move
                
def userMove(game):
    print("\n\n\nPlayer's Turn,")
    move=getInput()
    while not game.moveCheck(move):
        print("\nImpossible move, type again")
        move=getInput()
    game.movePiece(move)
    afterMove(game)
    
def aiMove(game):
    print("\n\n\nGuillaumeGo's turn...")
    ai(game)
    
def playTurn(game):
    if game.turn%2==1:
        userMove(game)   
    else:
        aiMove(game)
    
def runGame():
    print("Chess start! Match with GuillaumeGo!")
    game = Game()
    game.board = initBoard()
    
    while True:
        showBoard(game)
        playTurn(game)
    
runGame()

