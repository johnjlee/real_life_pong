import PlayerListener
import ObserverListener
import StarterListener
import time
import random
from Constants import *

class GameServer:
    def __init__(self):
        # To better extend this to more players, just make an array of them
        # rather than separate vars..
        self.player1 = PlayerListener.PlayerListener(10001, 1, self)
        self.player2 = PlayerListener.PlayerListener(10002, 2, self)
        self.observer = ObserverListener.ObserverListener(10009, self)
        self.starter = StarterListener.StarterListener(10008, self)
        self.position1 = 0.5
        self.position2 = 0.5
        self.ballX = 0.5
        self.ballY = 0.5
        self.score1 = 0
        self.score2 = 0
        self.ballDX = 0
        self.ballDY = 0
        self.game_started = False
        self.paddle_halfwidth = ServerConstants.PADDLE_WIDTH/2.0
        self.ResetBallPosition()
        
    # A callback, which PlayerListener uses, to report a new position
    # for one of the players.
    def SetPosition(self, player, position):
        if (player == 1):
            self.position1 = position
        else:
            self.position2 = position

    # A callback, which ObserverListener uses, to request the state
    # of the game as a 6-dimensional list:
    # [player 1 position, player2 position, ball X, ball Y, score1, score2]
    def GetGameState(self):
        "Returns a comma delimited string describing the game state"
        lst = [self.position1, self.position2, self.ballX,
               self.ballY, self.score1, self.score2 ]
        return str(lst).strip('[]')
        

    def StartGame(self):
        self.game_started = True

    def IsGameStarted(self):
        return self.game_started
    
    ### Game logic ###

    # Changes the velocity of the ball depending on where the collision
    # happens (top, left, bottom, or right)
    def OnCollision(self, direction):
        if (direction == ServerConstants.DIRECTION_TOP or
            direction == ServerConstants.DIRECTION_BOTTOM):
            self.ballDY = -self.ballDY
        if (direction == ServerConstants.DIRECTION_LEFT or
            direction == ServerConstants.DIRECTION_RIGHT):
            self.ballDX = -self.ballDX

    # Advance the position of the ball, and then check to see if
    # the ball bounced off of something, or whether someone has
    # scored a point.
    def AdvanceBallPosition(self):
        self.ballX += self.ballDX
        self.ballY += self.ballDY
        self.CheckCollisions()
        self.CheckScore()

    # Checks to see if a collision has happened and changes the direction
    # of the ball as needed.
    def CheckCollisions(self):
        if (self.ballY < 0):
            self.OnCollision(ServerConstants.DIRECTION_BOTTOM)
        elif (self.ballY > 1):
            self.OnCollision(ServerConstants.DIRECTION_TOP)
        
        if (self.ballX < 0):
            # Is the player's paddle blocking it?
            if (self.ballY >= self.position1 - (self.paddle_halfwidth) and
                self.ballY <= self.position1 + (self.paddle_halfwidth)):
                self.OnCollision(ServerConstants.DIRECTION_LEFT)

        elif (self.ballX > 1):
            # Is the player's paddle blocking it?
            if (self.ballY >= self.position2 - (self.paddle_halfwidth) and
                self.ballY <= self.position2 + (self.paddle_halfwidth)):
                self.OnCollision(ServerConstants.DIRECTION_RIGHT)
                
    # Checks to see if someone has scored.
    def CheckScore(self):
        if (self.ballX < 0):
            # Is the player's paddle blocking it?
            if (self.ballY < self.position1 - (self.paddle_halfwidth) or
                self.ballY > self.position1 + (self.paddle_halfwidth)):
                self.score2 += 1
                self.ResetBallPosition()

        elif (self.ballX > 1):
            # Is the player's paddle blocking it?
            if (self.ballY < self.position2 - (self.paddle_halfwidth) or
                self.ballY > self.position2 + (self.paddle_halfwidth)):
                self.score1 += 1
                self.ResetBallPosition()
                
    def ResetBallPosition(self):
        self.ballX = 0.5
        self.ballY = 0.5
        rand1 = random.choice((-1,1))
        rand2 = random.choice((-1,1))
        self.ballDX = rand1 * ((random.random() * ServerConstants.MAX_SPEED) + ServerConstants.MIN_SPEED)
        self.ballDY = rand2 * ((random.random() * ServerConstants.MAX_SPEED) + ServerConstants.MIN_SPEED)
        
        
    def stop(self):
        self.player1.stop()
        self.player2.stop()
        self.observer.stop()
        self.starter.stop()
        
    def run(self):
        self.player1.start()
        self.player2.start()
        self.observer.start()
        self.starter.start()
        
        while True:
            time.sleep(ServerConstants.TIME_STEP_SIZE)
            if self.game_started == True:
                self.AdvanceBallPosition()


try:
    gameserver = GameServer()
    gameserver.run()
except (KeyboardInterrupt):
    gameserver.stop()
    raise
