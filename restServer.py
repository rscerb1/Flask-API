from flask import Flask, request
from flask_restful import reqparse, Api, Resource
from waitress import serve
from checkBoard import Board
import sqlFunctions

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('player0')
parser.add_argument('player1')
parser.add_argument('board')
parser.add_argument('turn')
parser.add_argument('username')
parser.add_argument('password')


#
# USER
#

class Players(Resource):
    # return specified user
    def get(self):
        args = request.args.to_dict()
        if(len(args) == 0):
            # return all users
            return sqlFunctions.getUsers()
        if(len(args) == 1):
            # return a specified user
            return sqlFunctions.getUser(args['username'])
        else:
            return "Invalid argument(s)"
        
    # add new user
    def post(self):
        args = parser.parse_args()
        return sqlFunctions.postUser(parser.parse_args()['username'],parser.parse_args()['password']), 201
    
    # delete a specified user
    def delete(self):
        return sqlFunctions.deleteUser(parser.parse_args()['user']), 204
    
#
# GAME
#

class Game(Resource):
    def get(self):
        args = request.args.to_dict()
        if(len(args) == 0):
            # return all games
            return sqlFunctions.getGames()
        if(len(args) == 1):
            # return all games of specified user
            return sqlFunctions.getUserGames(str(args['username']))
        if(len(args) == 2):
            # return a game between 2 specified players
            return sqlFunctions.getGame(str(args['player0']), str(args['player1']))
        else:
            return "Invalid argument(s)"
    
    # create new game between 2 users
    def post(self):
        args = parser.parse_args()
        return sqlFunctions.postGame(args['player0'], args['player1']), 201
    
    # update a game between 2 users
    def put(self):
        args = parser.parse_args()
        board = Board(args['board'])
        return sqlFunctions.putGame(args['player0'], args['player1'], args['board'], args['turn'], board.getStatus()), 201
    
    # delete a game between 2 users
    def delete(self):
        args = parser.parse_args()
        return sqlFunctions.deleteGame(args['player0'], args['player1']), 204
    
# addresses
api.add_resource(Players, '/players')
api.add_resource(Game, '/games')


if __name__ == '__main__':
    serve(app, host='10.0.5.152', port=5000, threads=1)
    #app.run(host='10.0.5.152', port=5000, debug=True)