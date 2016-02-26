#GridBug
A GridWorld like CS learning environment implemented in Python

**NOTE: _THIS FILE IS STILL BEING EDITED_.**

##Requires:
1. Python 2.7.x
2. Requires [Pygame](http://www.pygame.org/download.shtml) to be installed

##Included:
1. Livewires (modified) Inside _game.py_ as a wrapper for the pygame graphics library to create game surfaces (display), interactive objects (sprites and text), and control the main game event loop.

##PyBugger.bots Object Classes:  

###Game(object)
 
    Game()  
    
 The Game object controls the program flow and objects in the game.

**METHODS:**

    setup()
 Sets up the game environment and displays the blue instructions.
 
    refresh()
 Draws/Redraws all objects and updates the display screen.

    pause(\<key\>, \<wait\>)  
    
 Where:  

key = (games.key) Defaults to games.K_RETURN  
wait = (integer) Defaults to 0  

Will pause execution and wait for key <key> to be pressed or to wait for <wait> tenths of seconds to expire.
Pressing the \<END\> or \<ESC\> keys, or clicking on the game window close box with the mouse while in the pause() function will call the end() Function to terminate the game.

    autoplay()
 Will start a constant event loop that will not pause for any key input or mouse actions other than pressing \<ESC\> or clicking on the game window close box.  (For advanced real time game usage)

    broadcast(<message>)
 Where: message = (string)
 Will place <message> in the broadcast message queue for one pause cycle for BugObjects to process it. Typically used by the BugObject.update method to display a text balloon above the BugObject.

    end()
 Removes all objects, displays “Game Over” and closes the window.

**PROPERTIES:**

    running (boolean)
 Can be set or changed anytime after the Game object is initialized where it is set to “True”.  If set to “False” will cause Game.end() to be called.

    tip (games.Message object)
 Can be set or changed using the “games.Message.value” property.

    msg (python list object)
 List item can be added with Game.msg.append(<string>). The list used by the Game.broadcast function and is typically processed in the BugObject's update() method..

###BugObject()
 Inherited From: _games.Sprite_  (See “games” module for Sprite class object)
 
     BugObject(<image>, <x>, <y>)
 
Where:

image = A Surface image object. (optional)  
x = vertical coordinate in grid scale (optional)  
y = horizontal coordinate in grid scale (optional)

The BugObject will be added to the screen (grid) upon initialization.

**METHODS:**

	update()
Update() is called during each call to the Game.pause() method.  It can be modified to make the BugObject perform customized actions in a subclass for example.
	move(<wait>) Where: wait = (integer)
Moves the BugObject one space in the 10x10 grid in the direction in which it is currently pointed.  If a “fence” object is activated in the 10x10 grid it will form a barrier and the BugObject will not move past it. Specifying a <wait> interval will cause the BugObject to pause for the interval (in hundredths of a second) or until the <ENTER> key is pressed.
		turn(<wait>) Where: wait = (integer)
Rotates the BugObject 90 degrees to the right.  It does not change its current location. Specifying a <wait> interval will cause the BugObject to pause for the interval (in hundredths of a second) or until the <ENTER> key is pressed.
		pause(<timeout>) Where: timeout = (integer)
Pauses the game action of the BugObject.  Causes all game objects to be updated and waits for the <ENTER> key to be pressed. If a <timeout> value is specified (in hundredths of a second), then the pause will wait for the <ENTER> key until the <timeout> interval is passed, then resume program execution.

		say(<what>) Where: what = (string)
			Will display the <what> string in a text balloon above the BugObject.
		flash() (not unimplemented yet)
		pick_chip(wait) Where: wait = (integer)
Picks up a chip at the current BugObject 10x10 grid location and decreases the COUNT of the picked chip stack if the stack contains more than one chip.  If there is only one chip at the location, the chip will be moved to the BugObject. Specifying a <wait> interval will cause the BugObject to pause for the interval (in hundredths of a second) or until the <ENTER> key is pressed.
drop_chip(wait) Where: wait = (integer)
Drops a chip at the current 10x10 BugObject location and decreases the COUNT of the chip stack on the BugObject. If there is only one chip on the BugObject, the chip object is removed from the BugObject. Specifying a <wait> interval will cause the BugObject to pause for the interval (in hundredths of a second) or until the <ENTER> key is pressed.
		can_move()
Checks to see if there are any fence barriers in the direction that the BugObject would move if a move() method were called.
		die()
			Removes the BugObject from the Game.

	PROPERTIES:
		name (string)
Can be set or changed anytime or used to verify which BugObject is being referenced.
	CHIP (ChipObject)
		Set automatically by pick_chip() and drop_chip() methods.
	TRAIL (boolean)
		If set to “TRUE”, BugObject will leave a “trail” on its path.
	MSGRSP{} (python dictionary object)
Will respond to bots.game.broadcast(<string>) using <string> as the key to the index in the MSGRSP{} dictionary.
Add a response with: MSGRSP[<key string>] = “String to Say”
When the <key string> is “broadcast” BugObject will scan the bots.game.msg list for the <key string>. If found it will pass the corresponding “String to Say” to the BugObject.say() method.
	location (“Get” only - there is no “Set” function)
Evaluates to 10x10 grid coordinate tuple (x,y).

 
ChipObject()
	Inherited From: games.Sprite
	Instantiated with:
ChipObject(<image>=None, <x>, <y>, <show_cnt>=false, <pix>=False,
<cnt>=1)
	Where:	image= (Surface), returned from games.load_image(<file>) to
				use a different image from the default grey circle image
x = integer, vertical coordinate in grid scale (grid square)
			y = integer, horizontal coordinate in grid scale
			show_cnt = boolean, True to show the count of stacked stacked
“ChipObjects” at the same location (default False)
		pix = boolean, True if using pixel coordinates (default False)
			cnt = integer, number of chips at location (default = 1)
	The ChipObject will be added to the screen (grid) upon initialization.
METHODS:
	update()
Updates the chip object’s count text image to reflect the number of chip objects at a single grid location as defined by the “COUNT” property.
	die()	Removes the ChipObject.

PROPERTIES:
	COUNT (integer)
Determines number to display on chip objects.  Updated automatically when a chip is picked or dropped by a BugObject.
	*NOTE: A ChipObject with a COUNT set to zero will destroy itself.
 
ADDITIONAL REFERENCES:

Sprite Object from PyBugger.bots.games (from “bots.games”)
	Class that is inherited by BugObject andChipObject:
	bots.games.Sprite(<image>, <angle>=0, <x>=0, <y>=0, <top>=None,
<bottom>=None, <left>=None, <right>=None, <dx>=0, <dy>=0, <interval>=1, <is_collideable>=True)
image = bots.games.load_image(“path/to/image.xxx”,<transparent>=True)
		(use transparent=False for background images, defaults to True)
*NOTE: This is a low level “livewires” Sprite object that has no concept of the “PyBugger” modules.  As such all the all the location coordinates are not mapped to the 10 x 10 grid screen that is defined and managed by the “PyBugger” module.
METHODS:
	start() (not used – sets “tickable” to True)
	stop() (not used – sets “tickable” to False)
	tick() (passed through)
		Called in main loop if “tickable is “True”
	update() (passed through)
	overlaps(<object>)
		<object> is usually another Sprite Object
	elevate(<above object>)
	lower(<below object>)
	destroy()
		Usually called in higher level “die()” method.
PROPERTIES:
	x (integer)
	y (integer)
	position (tuple) – tuple is defined as (x, y)
	dx (integer)
	dy (integer)
	velocity (integer)
	left (integer)
	right (integer)
	top (integer)
	bottom (integer)
	angle (integer) – 0-360
	image (integer)
	height (integer)
	width (integer)
	is_collideable (boolean)
	overlapping_sprites (Sprite Object List)
	interval (integer)
