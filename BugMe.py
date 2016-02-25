#!/usr/bin/python
# A Python Script
#
# BugMe - Learn to Program with a bug object
#
import PyBugger.bots as pbg

class FlyBug(pbg.BugObject):
    
    def __init__(self, x, y):
        super(FlyBug, self).__init__(x = x, y = y)
        self.timer = 0
        self.step = 0

    def update(self):
        super(FlyBug, self).update() # Call inherited class Update method
        if self.timer % 15 == 0:
            if self.step == 0 or self.step == 1:
                self.move()
            if self.step == 3:
                self.turn()
            self.step += 1
            if self.step > 3:
                self.step = 0
        self.timer += 1
        if self.timer > 1000:
            self.timer = 0

# Initialize the Global Game Object
pbg.BugGame = pbg.Game()

def main():

    # Set up the Game - click to add fences
    g = pbg.BugGame
    g.setup()
    
    #Set up the Game Objects
    bug = pbg.BugObject(x = 3, y = 3)
    bug.name = "Bob"
    #bug.TRAIL = True
    
    # Add a Chip to the grid (set the number of chips with 'cnt')
    g.put_chip(x = 4, y = 4, cnt = 3)
    
    # Start the Game
    g.pause()
    
    bug.turn()
    bug.move()

    bug.move()

    bug.turn()
    g.broadcast("NIGHT")
    bug.move() # Should be over Chip
    
    #Bug will pick up a chip and move with it
    bug.pick_chip()
    bug.turn()
    bug.move()
    
    #Bug will drop a chip them move on
    bug.drop_chip()
    bug.turn()
    bug.move()

    #End the Game
    bug.die()
    g.end()

# kick it off! - run the "main()" function
main()
