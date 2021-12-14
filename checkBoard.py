class Board():
    
    def __init__(self, board):
        self.__status = 0
        self.__board = board
        self.__checkGameWon()
    
    # return the status of the game
    # 1 = game is won
    # 0 = game not won
    def getStatus(self):
        return self.__status  
        
    # return the board value at coordinate (X,Y,Z)
    def __getValue(self, X, Y, Z):
        position = X + Y*9 + Z*3
        return(self.__board[position])
    
    # check the an axis for 3 in a row
    def __checkGameWon(self):
        groupX = ''
        groupY = ''
        groupZ = ''
        groupDR = ''
        groupDL = ''
        zDiagonals = []
        for i in range(3):
            for j in range(3):
                if(self.__checkGroups([groupX, groupY, groupZ, groupDR, groupDL])):
                    return True
                groupX = ''
                groupY = ''
                groupZ = ''
                groupDR = ''
                groupDL = ''
                for k in range(3):
                    groupX += self.__getValue(k,i,j)
                    groupY += self.__getValue(j,k,i)
                    groupZ += self.__getValue(j,i,k)
                    groupDR += self.__getValue(k, j, k)
                    groupDL += self.__getValue((k+2)%3, j, (k+k)%3)
                iter = 3*i + j
                zDiagonals.append(self.__board[iter] + str(self.__board[13]) + self.__board[26-iter])
        if(self.__checkGroups([groupX, groupY, groupZ, groupDR, groupDL] + zDiagonals)):
            return True
        return False
        
    # check for 3 in a row
    def __checkGroups(self, groups):
        for group in groups:
            if(group == '111' or group == '222'):
                self.__status = 1
                return True
        return False