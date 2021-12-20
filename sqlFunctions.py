import mysql.connector, time, checkBoard, datetime


# error logger
def log(message):
    with open('log.txt', 'a+') as logFile:
        logFile.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\t'DBFs:'\t{message}\n")


try:
  database = mysql.connector.connect(
    host="localhost",
    user="python",
    password="12qwaszx",
    database="androidProject"
  )
except:
  log("ERROR: Could not connect to the DB")

# test username input
def checkUsername(username):
  if(username.isalnum() and len(username)<=10):
    return True
  else:
    return False

# select a list from the database and return it formated for flask
def selectListQuery(sql):
  cursor = database.cursor()
  cursor.execute(sql)
  row_headers=[x[0] for x in cursor.description]
  rv = cursor.fetchall()
  json_data=[]
  for result in rv:
      json_data.append(dict(zip(row_headers,result)))
  return json_data

#
# USER table queries
#

# query for selecting all users
def getUsers():
  sql = "SELECT * FROM USERS ORDER BY WINS LIMIT 50"
  return selectListQuery(sql)

# query for selecting a specified user
def getUser(user):
  if(checkUsername(user)):
    cursor = database.cursor()
    cursor.execute(f"SELECT * FROM androidProject.USERS WHERE username = '{user}';")
    row_headers=[x[0] for x in cursor.description]
    return dict(zip(row_headers,cursor.fetchone()))

# query for creating a new user
def postUser(username, password):
  try:
    if(checkUsername(username) and checkUsername(password)):
      accountSql = f"INSERT INTO ACCOUNT_INFO (username, password) VALUES ('{username}', '{password}');"
      userSql = f"INSERT INTO USERS (username) VALUES ('{username}');"
      cursor = database.cursor()
      cursor.execute(accountSql)
      cursor.execute(userSql)
      database.commit()
      return "1000"
  except:
    return "1003"
    
# query for deleting a specified user
def deleteUser(user):
  try:
    if(checkUsername(user)):
      sql = f"DELETE FROM USERS WHERE username = '{user}';"
      cursor = database.cursor()
      cursor.execute(sql)
      database.commit()
      return f"User '{user}' has been deleted"
  except:
    return 'ERROR: User was not found or has existing games'
    
#
# GAME table queries
#

# query for selecting all games
def getGames():
  sql = "SELECT * FROM GAMES;"
  return selectListQuery(sql)

# query for selecting all user games from a specified user
def getUserGames(user):
  if(checkUsername(user)):
    sql = f"SELECT * FROM GAMES WHERE player0 = '{user}' OR player1 = '{user}';"
    return selectListQuery(sql)
  
# query for selecting a game between two specified users
def getGame(user, user1):
  if(checkUsername(user) and checkUsername(user1)):
    sql = f"SELECT * FROM GAMES WHERE (player0 = '{user}' AND player1 = '{user1}') OR (player0 = '{user1}' AND player1 = '{user}');"
    cursor = database.cursor()
    cursor.execute(sql)
    row_headers=[x[0] for x in cursor.description]
    return dict(zip(row_headers,cursor.fetchone()))
  
# query for creating a new game
def postGame(user, user1):
  try:
    if(checkUsername(user) and checkUsername(user1)):
      if(user == user1):
        return "ERROR: Cannot create a game between the same user"
      rand = int(time.time()) % 2
      cursor = database.cursor()
      cursor.execute(f"INSERT INTO GAMES (player0, player1, turn, status) VALUES ('{user}', '{user1}', '{rand}', 1);")
      database.commit()
      return f"Game created between '{user}' and '{user1}'"
  except:
    return "ERROR: Game could not be created"
    
# query for deleting all games
def deleteGames():
  cursor = database.cursor()
  cursor.execute(f"TRUNCATE TABLE GAMES;")
  database.commit()
    
# query for deleting a game between specified users
def deleteGame(user, user1):
  try:
    if(checkUsername(user) and checkUsername(user1)):
      cursor = database.cursor()
      cursor.execute(f"DELETE FROM GAMES WHERE (player0 = '{user}' AND player1 = '{user1}') OR (player0 = '{user1}' AND player1 = '{user}');")
      database.commit()
      return f"Game between '{user}' and '{user1}' has been deleted"
  except:
    return "ERROR: Game could not be deleted"

# query for updating a game between specified users
def putGame(user, user1, board, turn, status):
  gameTurn = turn
  try:
    if(checkUsername(user) and checkUsername(user1) and (checkBoard(board))):
      if(turn == '1'):
        gameTurn = '0'
      else:
        gameTurn = '1'
      sql = f"""
      UPDATE GAMES 
      SET board = {board}, turn = {gameTurn}, status = {status} 
      WHERE (player0 = '{user}' and player1 = '{user1}') OR (player0 = '{user1}' and player1 = '{user}');"""
      cursor = database.cursor()
      cursor.execute(sql)
      database.commit()
      return "Game updated"
  except:
    return "ERROR: Game could not be updated"
