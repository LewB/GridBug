#!/usr/bin/python

import PyBugger.bots as bw

class LabRat(bw.BugObject):
    
    def __init__(self, name, x, y):
        rat_img = bw.games.load_image("PyBugger/images/RatImage.gif")
        super(LabRat, self).__init__(
                                 image = rat_img,
                                 x = x, y = y)
        # BugObject adds itself to the game screen
        self.name = name
        self.home = (x, y)
        self.hungry = True
        
    def run(self):
        # Run the LabRat on its own
        if not self.can_move():
            # Try going Right
            self.turn()
            if not self.can_move():
                # Try going Left
                self.turn()
                self.turn()
                if not self.can_move():
                    # Try going Back
                    self.turn()
                    self.turn()
                    self.turn()
                    if not self.can_move():
                        # Nowhere left to go
                        self.say("Help I'm trapped!")
        else:
            self.move()

class Food(bw.ChipObject):
    
    def __init__(self, x, y):
        food_img = bw.games.load_image("PyBugger/images/Cheese.bmp",
                                       transparent=True)
        super(Food, self).__init__(image = food_img,
                                x = x, y = y, show_cnt = False)
        bw.games.gscreen.add(self)

# Initialize the Global Game Object
bw.BugGame = bw.Game()

def main():
    # Initialize the Game Object
    Maze = bw.BugGame
    Maze.setup()
    
    #Set up the Game Objects
    cheese = Food(x = 7, y = 7)
    rat = LabRat(name = "Rat", x = 3, y = 3)
    rat.pause() # Set up maze while paused
    
    # Run the Rat
    while Maze.running == True:
        rat.run()
        rat.say("LOC: " + str(rat.location))
        rat.pause()
        # If rat does not have a chip and rat is hungry
        # pick up a chip if there is one there
        if not rat.CHIP and rat.hungry:
            for obj in rat.overlapping_sprites:
                if obj != rat.CHIP and obj.TYPE == "CH":
                    # Get the Loose Cheese
                    rat.pick_chip()
                    if rat.CHIP:
                        # Got the Cheese
                        rat.say("Got the Cheese!")
                        rat.hungry = False
                        rat.pause()
        
        if rat.CHIP and rat.location == rat.home:
            # Drop the Cheese
            rat.say("Dropped the Cheese at Home!")
            rat.drop_chip()
            rat.pause()
    
    # End the Game
    Maze.end()
    
# Run Maze
main()
