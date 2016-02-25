#!/usr/bin/python
# A Python Script
#
# BugMe - Learn to Program with a bug object
#
import PyBugger.bots as pbg

# Initialize the Global Game Object
pbg.BugGame = pbg.Game()

def main():
    
    # Create the Game Object
    myGame = pbg.BugGame
    # Setup the Game and Screen
    myGame.setup()
    
    # Create the Bug Object
    bug = pbg.BugObject(x = 3, y = 3)
    # Wait for initial press of <ENTER> key to start action
    bug.pause()
    
    # Start the Game Actions
    bug.move()
    bug.turn()
    bug.move()
    bug.move()

    # End the Game
    bug.die()
    myGame.end()

# kick it off! - run the "main()" function
main()
