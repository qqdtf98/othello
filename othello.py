
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

  print(black)
  print(white)


def stone_onMouseAction(x, y):
  global turn

  object = board[y][x]
  if object.state == State.POSSIBLE: 
    if turn == Turn.BLACK:
      setState(x, y, State.BLACK)
      reverse_xy(x,y)
      turn = Turn.WHITE
    else:
      setState(x, y, State.WHITE)
      reverse_xy(x,y)
      turn = Turn.BLACK
      
    if not setPossible():
      if turn == Turn.BLACK: turn = Turn.WHITE
      else: turn = Turn.BLACK

      if not setPossible(): 
        showMessage("게임이 종료되었습니다.")

  countStone()


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
  reverse_xy_dir(x,y,0,1)   
  reverse_xy_dir(x,y,1,1)   
  reverse_xy_dir(x,y,1,0)   
  reverse_xy_dir(x,y,1,-1)   
  reverse_xy_dir(x,y,0,-1)   
  reverse_xy_dir(x,y,-1,-1)   
  reverse_xy_dir(x,y,-1,0)   
  reverse_xy_dir(x,y,-1,1)

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
   
  if (setPossible_xy_dir(x,y,0,1)): return True
  if (setPossible_xy_dir(x,y,1,1)): return True
  if (setPossible_xy_dir(x,y,1,0)): return True
  if (setPossible_xy_dir(x,y,1,-1)): return True
  if (setPossible_xy_dir(x,y,0,-1)): return True
  if (setPossible_xy_dir(x,y,-1,-1)): return True
  if (setPossible_xy_dir(x,y,-1,0)): return True
  if (setPossible_xy_dir(x,y,-1,1)): return True
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