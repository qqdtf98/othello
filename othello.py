
from bangtal import *
from enum import Enum

setGameOption(GameOption.ROOM_TITLE, False)
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)

scene = Scene("Othello", "Images/background.png")


class State(Enum):
  BLANK = 0
  POSSIBLE = 1
  BLACK = 2
  WHITE = 3


class Turn(Enum):
  BLACK = 1
  WHITE = 2


turn = Turn.BLACK


def setState(x, y, s):
  object = board[y][x]
  object.state = s 
  if s == State.BLANK:
    object.setImage("Images/blank.png")
  elif s == State.BLACK:
    object.setImage("Images/black.png")
  elif s == State.WHITE:
    object.setImage("Images/white.png")
  elif turn == Turn.BLACK:
    object.setImage("Images/black possible.png")
  else:
    object.setImage("Images/white possible.png")

black_Tens = Object("Images/blank.png")
black_Tens.locate(scene,750,270)
black_Tens.show()

black_Units = Object("Images/blank.png")
black_Units.locate(scene,820,270)
black_Units.show()

white_Tens = Object("Images/blank.png")
white_Tens.locate(scene,1080,270)
white_Tens.show()

white_Units = Object("Images/blank.png")
white_Units.locate(scene,1150,270)
white_Units.show()

def countStone():
  black = 0
  white = 0
  for y in range(8):
    for x in range(8):
      if(board[y][x].state == State.BLACK): black += 1
      elif(board[y][x].state == State.WHITE): white += 1

  if int(black / 10) == 0: black_Tens.setImage("Images/blank.png")
  else: black_Tens.setImage(f"Images/L{int(black / 10)}.png")
  black_Units.setImage(f"Images/L{black % 10}.png")

  if int(white / 10) == 0: white_Tens.setImage("Images/blank.png")
  else: white_Tens.setImage(f"Images/L{int(white / 10)}.png")
  white_Units.setImage(f"Images/L{white % 10}.png")

def count_xy_dir(x,y,dx,dy):
  count = 0
  if turn == Turn.BLACK:
    mine = State.BLACK
    other = State.WHITE
  else:
    mine = State.WHITE
    other = State.BLACK

  possible = False
  while True:
    x = x+dx
    y = y+dy 

    if x<0 or x>7: return
    if y<0 or y>7: return

    object = board[y][x]
    if object.state == other:
      possible = True
    elif object.state == mine:
      if possible:
        while True:
          x = x - dx
          y = y - dy
          object = board[y][x]
          if object.state == other:
            count+=1
          else: return count
    else: return


def count_xy(x,y):
  totalCount = 0
  for i in range(-1,2):
    for j in range(-1,2):
      count = count_xy_dir(x,y,i,j)
      if (i != 0 or j != 0) and count != None:
        totalCount += count
  return totalCount


def setWhiteByComputer():
  global turn

  max = -1
  maxi = -1
  maxj = -1

  for y in range(8):
    for x in range(8):
      if(board[y][x].state == State.POSSIBLE):
        count = count_xy(x,y)
        if(count != None):
          if max < count:
            max = count
            maxi = x
            maxj = y

  object = board[maxj][maxi]
  if object.state == State.POSSIBLE:
    setState(maxi, maxj, State.WHITE)
    reverse_xy(maxi,maxj)
    turn = Turn.BLACK

    if not setPossible():
      turn = Turn.BLACK

      if not setPossible(): 
        showMessage("게임이 종료되었습니다.")

  countStone()



def stone_onMouseAction(x, y):
  global turn

  object = board[y][x]
  if object.state == State.POSSIBLE:
    setState(x, y, State.BLACK)
    reverse_xy(x,y)
    turn = Turn.WHITE
      
    if not setPossible():
      turn = Turn.WHITE

      if not setPossible(): 
        showMessage("게임이 종료되었습니다.")

  countStone()
  setWhiteByComputer()


def reverse_xy_dir(x,y,dx,dy):
  if turn == Turn.BLACK:
    mine = State.BLACK
    other = State.WHITE
  else:
    mine = State.WHITE
    other = State.BLACK

  possible = False
  while True:
    x = x+dx
    y = y+dy 

    if x<0 or x>7: return
    if y<0 or y>7: return

    object = board[y][x]
    if object.state == other:
      possible = True
    elif object.state == mine:
      if possible:
        while True:
          x = x - dx
          y = y - dy
          object = board[y][x]
          if object.state == other:
            setState(x,y,mine)
          else: return
    else: return


def reverse_xy(x,y):
  for i in range(-1,2):
    for j in range(-1,2):
      if(i != 0 or j != 0): reverse_xy_dir(x,y,i,j)

def setPossible_xy_dir(x,y,dx,dy):
  if turn == Turn.BLACK:
    mine = State.BLACK
    other = State.WHITE
  else:
    mine = State.WHITE
    other = State.BLACK

  possible = False
  while True:
    x = x+dx
    y = y+dy 

    if x<0 or x>7: return False
    if y<0 or y>7: return False

    object = board[y][x]
    if object.state == other:
      possible = True
    elif object.state == mine:
      return possible
    else:
      return False


def setPossible_xy(x,y):
  object = board[y][x]
  if object.state == State.BLACK: return False
  if object.state == State.WHITE: return False
  setState(x,y,State.BLANK)
   
  for i in range(-1,2):
    for j in range(-1,2):
      if i != 0 or j != 0:
        if setPossible_xy_dir(x,y,i,j): return True
  return False

     
def setPossible():
  possible = False
  for y in range(8):
    for x in range(8):
      if setPossible_xy(x,y):
        setState(x,y,State.POSSIBLE)
        possible = True

  return possible

board = []
for y in range(8):
  board.append([])
  for x in range(8):
    object = Object("Images/blank.png")
    object.locate(scene, 40+x*80, 40+y*80)
    object.show()
    object.onMouseAction = lambda mx, my, action, ix = x, iy = y: stone_onMouseAction(ix, iy)
    object.state = State.BLANK

    board[y].append(object)

setState(3,3,State.BLACK)
setState(4,4,State.BLACK)
setState(3,4,State.WHITE)
setState(4,3,State.WHITE)

setPossible()
countStone()

startGame(scene)