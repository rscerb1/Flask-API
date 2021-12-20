from flask import Flask, request
from flask_restful import reqparse, Api, Resource
from waitress import serve
from checkBoard import Board
import sqlFunctions, datetime, os.path


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('player0')
parser.add_argument('player1')
parser.add_argument('board')
parser.add_argument('turn')
parser.add_argument('username')
parser.add_argument('password')


# error logger
def log(message):
  with open(str(os.path.dirname(os.path.abspath(__file__))) + '/log.txt', 'a+') as logFile:
        logFile.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\tAPI:\t{message}\n")

#
# USER
#


class Players(Resource):
    # return specified user
    def get(self):
        try:
            args = request.args.to_dict()
            if(len(args) == 0):
                # return all users
                log('REQUEST: Get all players')
                return sqlFunctions.getUsers()
            if(len(args) == 1):
                # return a specified user
                log('REQUEST: Get player ' + args['username'])
                return sqlFunctions.getUser(args['username'])
            else:
                log('REQUEST: Invalid argument(s) in get player(s)')
                return "Invalid argument(s)"
        except:
            log('REQUEST: Get player(s) failed')
        
    # add new user
    def post(self):
        try:
            args = parser.parse_args()
            log('REQUEST: Create player ' + args['username'])
            return sqlFunctions.postUser(parser.parse_args()['username'],parser.parse_args()['password']), 201
        except:
            log('REQUEST: Create player failed')
    
    # delete a specified user
    def delete(self):
        try:
            return sqlFunctions.deleteUser(parser.parse_args()['user']), 204
        except:
            log('REQUEST: Delete player failed')
    
#
# GAME
#

class Game(Resource):
    def get(self):
        try:
            args = request.args.to_dict()
            if(len(args) == 0):
                # return all games
                log('REQUEST: Get all games')
                return sqlFunctions.getGames()
            if(len(args) == 1):
                # return all games of specified user
                log('REQUEST: Get games from player ' + args['username'])
                return sqlFunctions.getUserGames(str(args['username']))
            if(len(args) == 2):
                # return a game between 2 specified players
                log('REQUEST: Get games from players ' + args['player0'] + 'and ' + args['player1'])
                return sqlFunctions.getGame(str(args['player0']), str(args['player1']))
            else:
                return "Invalid argument(s)"
        except:
            log('REQUEST: Failed to get game(s)')
    
    # create new game between 2 users
    def post(self):
        try:
            args = parser.parse_args()
            log('REQUEST: Create game between ' + args['player0'] + 'and ' + args['player1'])
            return sqlFunctions.postGame(args['player0'], args['player1']), 201
        except:
            log('REQUEST: Failed to create game')
    
    # update a game between 2 users
    def put(self):
        try:
            args = parser.parse_args()
            board = Board(args['board'])
            return sqlFunctions.putGame(args['player0'], args['player1'], args['board'], args['turn'], board.getStatus()), 201
        except:
            log('Error updating player')
    
    # delete a game between 2 users
    def delete(self):
        try:
            args = parser.parse_args()
            return sqlFunctions.deleteGame(args['player0'], args['player1']), 204
        except:
            log('Error deleting game')
    
# addresses
api.add_resource(Players, '/players')
api.add_resource(Game, '/games')


if __name__ == '__main__':
    log("INFO: API Started")
    serve(app, host='10.0.5.152', port=5000, threads=1)
    #app.run(host='10.0.5.152', port=5000, debug=True)