#!/usr/bin/python
# A Python Script
#
# bots - A game environment with a grid, fence, chip, and bug objects
#
import sys
import math
import games
import color

BugGame = None

games.init(screen_width = 640, screen_height = 640, fps = 50)

class BugObject(games.Sprite):
    ### A sprite that moves one space on the screen. ###
    TYPE = "BG"
    _bug_img = games.load_image("PyBugger/images/BoxBug.gif")
   
    def __init__(self, image = None, x = 0, y = 0):
        bx = (x * 64) + 32
        by = (y * 64) + 32
        if image:
            self._bug_img = image
        self.WAIT = games.K_RETURN
        self.WAITMSG = ""
        self.MSGRSP = {}
        self.CHIP = None
        self.TRAIL = False
        self.name = "Bug"
        # INIT games.Sprite PARENT CLASS
        super(BugObject, self).__init__(image = self._bug_img,
                        x = bx, y = by, interval = 300)
        games.gscreen.add(self)
        
    def update(self):
        # Called with every call to tick(), if tickable = True
        global BugGame
        if BugGame:
            if self.MSGRSP:
                for msg in BugGame.msg:
                    #print "***** BROADCAST MSG: " + str(msg) + "*****"
                    if msg in self.MSGRSP:
                        #print self.MSGRSP[msg]
                        if self.MSGRSP[msg] != "":
                            self.say(self.MSGRSP[msg])
                        if msg == self.WAITMSG:
                            self.WAITMSG = ""
    
    def say(self, what=""):
        #print self.name + " Says: " + what
        SayObject(what, self.get_x() + (self.get_width() / 2), self.top)
        
    def wait_message(self, msg):
        self.say("Waiting for message: " + msg + " ...")
        self.WAITMSG = msg
        self.MSGRSP[msg] = "Got Message: " + msg
        
    def move(self, pw = 0):
        if self.WAITMSG:
            return
        if self.can_move():
            cx = self.x
            cy = self.y
            angle = self.angle * math.pi /180
            self.x = self.x + (64 * math.sin(angle))
            self.y = self.y + (64 * -math.cos(angle))
            
            for chp in self.overlapping_sprites:
                if chp.TYPE:
                    if chp.TYPE == "CH" and chp != self.CHIP:
                        if chp._SHOW_CNT == True and chp._NUMBER:
                            chp._NUMBER.lower()
                            chp.lower()
            if self.TRAIL:
                games.pygame.draw.line(BugGame.fg, color.red, (cx, cy), (self.x, self.y), 5)
        else:
            #print "*****  BUG CAN'T GO THERE  *******"
            self.say("OUCH! can't go there...")
        self.pause(pw)

    def pause(self, timeout = 0):
        global BugGame
        if BugGame:
            BugGame.pause(self.WAIT, timeout)
        
    def turn(self, pw = 0):
        if self.WAITMSG:
            return
        self.angle += 90
        #if pw:
        self.pause(pw)
        
    def flash(self):
        if self.WAITMSG:
            return
    
    def pick_chip(self, pw = 0):
        if self.WAITMSG:
            return
        picked = False
        for chp in self.overlapping_sprites:
            if chp.TYPE == "CH" and chp != self.CHIP:
                # print "*** FOUND CHIP ****"
                if self.CHIP == None:
                    if chp.COUNT == 1:
                        self.CHIP = chp
                    else:
                        self.CHIP = ChipObject(
                                           image = None,
                                           x = self.x,
                                           y = self.y,
                                           show_cnt = True,
                                           pix=True,
                                           cnt = 1)
                        # ChipObject init sets COUNT to 1
                        chp.COUNT -= 1
                else:
                    chp.COUNT -= 1
                    self.CHIP.COUNT += 1
                picked = True
                self.CHIP.angle = self.angle
                self.CHIP.elevate()
                if self.CHIP._SHOW_CNT and self.CHIP._NUMBER:
                        self.CHIP._NUMBER.elevate()
                break
        if not picked:
            print "Nothing to pick up"
            self.say("Nothing to Pick Up!")
        else:
            #if pw:
            self.pause(pw)
    
    def drop_chip(self, pw = 0):
        if self.WAITMSG:
            return
        if self.CHIP:
            #print "Have a CHIP to Drop"
            dropped = False
            for chp in self.overlapping_sprites:
                if chp.TYPE == "CH" and chp != self.CHIP:
                    #print "Found a CHIP at Location"
                    chp.COUNT += 1
                    dropped = True
                    break
            if not dropped:
                #print "No CHIP at Location"
                if self.CHIP.COUNT > 1:
                    #print "Making CHIP at Location"
                    chp = ChipObject(
                                    image = None,
                                    x = self.x,
                                    y = self.y,
                                    pix = True,
                                    cnt = 1)
                    # ChipObject init sets COUNT to 1
                    chp.lower(self)
                    #print "Decreasing Self CHIP Count"
                    self.CHIP.COUNT -= 1
                else:
                    #print "Dropping Self CHIP at Location"
                    self.elevate()
                    self.CHIP.angle = 0
                    self.CHIP = None
            #if pw:
            self.pause(pw)
        else:
            print "No CHIP to Drop."
    
    def can_move(self):
        result = True
        angle = self.angle * math.pi /180
        for i in range(0,56,8):
            rx = self.x + (i * math.sin(angle))
            ry = self.y + (i * -math.cos(angle))
            if (rx+5 > games.gscreen.width or rx-5 < 0
                    or ry+5 > games.gscreen.height or ry-5 < 0):
                result = False
                break
            fobs = games.gscreen.overlapping_objects((rx-5, ry-5, 10, 10))
            for s in fobs:
                if s.TYPE:
                    if s.TYPE == "FV" or s.TYPE == "FH":
                        result = False
                        break
        return result
    
    def get_location(self):
        x = int(math.floor(self.x / 64))
        y = int(math.floor(self.y / 64))
        return ((x, y))
    location = property(get_location)

    def get_x(self):
        return super(BugObject, self).get_x()
    def set_x(self, new_x):
        super(BugObject, self).set_x(new_x)
        if self.CHIP:
            self.CHIP.x = self.x    
    x = property(get_x, set_x)
    
    def get_y(self):
        return super(BugObject, self).get_y()
    def set_y(self, new_y):
        super(BugObject, self).set_y(new_y)
        if self.CHIP:
            self.CHIP.y = self.y
    y = property(get_y, set_y)
    
    def get_angle(self):
        return super(BugObject, self).get_angle()
    def set_angle(self, new_angle):
        super(BugObject, self).set_angle(new_angle)
        if self.CHIP:
            self.CHIP.angle = self.angle
    angle = property(get_angle, set_angle)
    
    def die(self):
        ### Destroy Bug. ###
        if self.CHIP:
            self.CHIP.die()
        self.destroy()
        

class ChipObject(games.Sprite):
    ### A Chip that can be dropped, stacked and picked up in the Grid
    TYPE = "CH"
    _img = games.load_image("PyBugger/images/chip00.bmp")
    
    def __init__(self, image = None, x = 0, y = 0,
                 show_cnt = False, pix = False, cnt = 1):
        if not pix:
            bx = (x * 64) + 32
            by = (y * 64) + 32
        else:
            bx = x
            by = y
        self._NUMBER = None
        if image:
            self._img = image
        super(ChipObject, self).__init__(
                image = self._img,
                x = bx, y = by,
                dx = 0, dy = 0)
        games.gscreen.add(self)
        if cnt < 1: cnt = 1
        if cnt > 99: cnt = 99
        self._SHOW_CNT = show_cnt
        self._COUNT = cnt
        if self._SHOW_CNT:
            self.update()
        
    def update(self):
        #set image to new count number
        if self._SHOW_CNT:
            if self._NUMBER:
                self._NUMBER.set_value(self._COUNT)
            else:
                self._NUMBER = ChipText(value = str(self._COUNT),
                                      x = self.x, y = self.y,
                                      angle = self.angle)
                # INIT Adds ChipText to Screen!
    
    ### COUNT Property
    def get_count(self):
        return self._COUNT
    def set_count(self, new_cnt):
        self._COUNT = new_cnt
        if self._COUNT == 0:
                self.die()
    COUNT = property(get_count, set_count)
    
    def get_x(self):
        return super(ChipObject, self).get_x()
    def set_x(self, new_x):
        super(ChipObject, self).set_x(new_x)
        if self._NUMBER:
            self._NUMBER.x = self.x
    x = property(get_x, set_x)
    
    def get_y(self):
        return super(ChipObject, self).get_y()
    def set_y(self, new_y):
        super(ChipObject, self).set_y(new_y)
        if self._NUMBER:
            self._NUMBER.y = self.y
    y = property(get_y, set_y)
    
    def get_angle(self):
        return super(ChipObject, self).get_angle()
    def set_angle(self, new_angle):
        super(ChipObject, self).set_angle(new_angle)
        if self._NUMBER:
            self._NUMBER.angle = self.angle
    angle = property(get_angle, set_angle)
    
    def die(self):
        if self._NUMBER:
            self._NUMBER.destroy()
        self.destroy()

class SayObject(games.Sprite):
    # Speech Balloon
    TYPE = "SB"
    _say_img = games.load_image("PyBugger/images/Bubble.bmp")
    #_new_img = _say_img
    
    def __init__(self, value, x = 0, y = 0):
        
        self._text = SayText(value, 0, 0)
        txwidth = self._text.get_width()
        txheight = self._text.get_height()
        if txwidth % 10 == 0:
            txwidth += 1
        #print("Width: " + str(txwidth))
        self._new_img = games.pygame.transform.smoothscale(self._say_img, (txwidth+20, txheight+40))
        kcolor = self._new_img.get_at((0,0))
        self._new_img.set_colorkey((kcolor))
        
        cx = x + (txwidth / 2) - 10
        cy = y - 4
        super(SayObject, self).__init__(
                image = self._new_img,
                x = cx, y = cy,
                is_collideable=False)
        self._text.x = cx
        self._text.y = cy - 2
        self._tickable = 0
        
        games.gscreen.add(self)
        games.gscreen.add(self._text)
    
    
class SayText(games.Text):
    ### Text for Bug
    TYPE = "ST"
    def __init__(self, value, x, y):
        super(SayText, self).__init__(
                                    value = value,
                                    x = x, y = y,
                                    size = 20,
                                    color = color.black)


class ChipText(games.Text):
    ### Text for top of Chip
    TYPE = "CT"

    def __init__(self, value, x, y, size = 20,
                                    color = color.black,
                                    angle = 0):
        
        super(ChipText, self).__init__(
                                    value = value,
                                    x = x, y = y,
                                    size = size,
                                    color = color,
                                    dx = 0, dy = 0,
                                    angle = angle)
        games.gscreen.add(self)


class GridObject(games.Sprite):
    ### A non-moving grid sprite ###
    TYPE = "XX"
    _SV_image = games.load_image("PyBugger/images/sv_grid.bmp")
    _SH_image = games.load_image("PyBugger/images/sh_grid.bmp")
      
    def __init__(self, x, y, imgtype):
        ityp = imgtype
        if ityp == "FH":
            image = self._SH_image
        elif ityp == "FV":
            image = self._SV_image
        else:
            ityp = "XX"
            image = None
        if image:
            super(GridObject, self).__init__(
                                    image = image,
                                    x = x, y = y,
                                    dx = 0, dy = 0)
            games.gscreen.add(self)
        self.TYPE = ityp
        self.tickable = 0
        
    def die(self):
        self.destroy()


class Game(object):
    ### The game itself. ###
    
    def __init__(self):
        ### Initialize Game object. ###
        # load and set background
        
        #bg = games.gscreen.get_background()
        #bg.fill(color.yellow, None, 0)
        #bg.convert()
        bg = games.load_image("PyBugger/images/BackGrid.jpg", transparent=False)
        games.gscreen.background = bg
        self.disp = games.gscreen._display
        games.pygame.display.set_caption("Foxcroft Python Game Window")
        ht = games.gscreen.height
        wd = games.gscreen.width
        self.fg = games.pygame.Surface((ht,wd))
        surfcolor = self.fg.get_at((0,0))
        self.fg.set_colorkey(surfcolor)
        self.auto_run = False
        self.running = True
        self.tip = None
        self.msg = []
    

    def __set_fences(self):
        mx = games.mouse.get_x()
        my = games.mouse.get_y()
        #print "****** MOUSE AT: " + str(mx) + " , " + str(my)
        fence_not_found = True
        fobs = games.gscreen.overlapping_objects((mx - 5, my - 5, 10, 10))
        if fobs:
            for mObj in fobs:
                if mObj.TYPE == "FH" or mObj.TYPE == "FV":
                    games.gscreen.remove(mObj)
                    mObj.die()
                    fence_not_found = False
                    #print "****** Deleting Fence ******"
        if fence_not_found:
            #print "****** CHECKING GRID HIT ******"
            cx = abs(mx % 64)
            cy = abs(my % 64)
            #print "****** CLICKED MODULO: " + str(cx) + " , " + str(cy)
            if cy < 5 and cx > 5:
                cx = math.floor(mx / 64) * 64 + 32
                cy = math.floor(my / 64) * 64
                #print "******* ADD FH OBJECT AT: " + str(cx) + " , " + str(cy)
                GridObject(
                         x = cx,
                         y = cy,
                         imgtype = "FH")
                
            elif cx < 5 and cy > 5:
                cx = math.floor(mx / 64) * 64
                cy = math.floor(my / 64) * 64 + 32
                #print "******* ADD FV OBJECT AT: " + str(cx) + " , " + str(cy)
                GridObject(
                         x = cx,
                         y = cy,
                         imgtype = "FV")


    def setup(self):
        ### Setup the game. ###
        self.tip = games.Message(value="Press <Enter> key to Move, <End> Key to Quit.",
                            color=color.blue,
                            size=24, x=320, y=40,
                            interval=0, is_collideable = False)
        self.tip._tickable = False
        self.tip.TYPE = "TP"
        games.gscreen.add(self.tip)
        self.refresh()
        

    def put_chip(self, x = 0, y = 0, cnt = 1):
        px = (x * 64) + 32
        py = (y * 64) + 32
        chip = None
        fnd = False
        obs = games.gscreen.overlapping_objects((px - 5, py - 5, 10, 10))
        for chp in obs:
            if chp.TYPE == "CH":
                fnd = True
                chp.COUNT += 1
                chip = chp
                break
        if not fnd:
            chip = ChipObject(image = None, x = px, y = py, 
                                show_cnt = True, pix = True, cnt = cnt)
        #self.pause()
        return chip


    def refresh(self):
        
        # Draw The Trail Surface onto the Main Display Surface
        self.disp.blit(self.fg, (0, 0))
        # Draw All Objects to Show Changes
        for obj in games.gscreen.all_objects:
            #print "Drawing Obj: " + str(obj)
            obj._draw()
        ### Refresh the screen ###
        games.gscreen._update_display()
        games.gscreen._flip_display()
        # Clear the objects for next move
        for obj in games.gscreen.all_objects:
            obj._erase()
    
    def broadcast(self, message = ""):
        # Broadcast a message to the list
        if message != "":
            self.msg.append(message)

    def autoplay(self):
        ### Play the game. ###
        # start play
        #print "**** STARTING PLAY ******"
        games.gscreen.mainloop()

    def pause(self, key = games.K_RETURN, wait = 0):

        while games.keyboard.is_pressed(games.K_END) == True \
                      or games.keyboard.is_pressed(key) == True:
            games.gscreen._clear_events()
        ### Main Loop ###
        iwt = wait
        while games.keyboard.is_pressed(key) == False:
            if games.keyboard.is_pressed(games.K_END) == True:
                self.running = False
                break
            if wait > 0:
                iwt -= 1
                if iwt < 1:
                    break
            #games.gscreen._clear_events()
            
            games.gscreen._wait_frame()
            # Check for Mouse Click
            if games.mouse.is_pressed(0) == True:
                self.__set_fences()
                while games.mouse.is_pressed(0) == True:
                    games.gscreen._clear_events()
            #
            # Have all tickable objects update themselves
            for obj in games.gscreen.all_objects[:]: 
                if obj._tickable:
                    # Calls obj.update()
                    obj._tick()
            #
            #Draw all Objects and Update Screen
            self.refresh()
        
            # Clear Message List for this Cycle
            self.msg = []
            # Get a Keypress or Mouse Click
            games.gscreen.handle_events()
            if games.gscreen._exit:
                self.running = False
                break

        ### End Main Loop ###
        
        # Clear Balloon+Text objects before next move
        for obj in games.gscreen.all_objects:
            if obj.TYPE == "SB" or obj.TYPE == "ST":
                obj.destroy()
        # If NOT running then End Program
        if self.running == False:
            self.end()

    def end(self):
        ### End the game. ###
        games.gscreen._clear_events()
        games.gscreen.clear()
        # show 'Game Over' for 5 seconds
        end_message = games.Message(value = "Game Over",
                                    size = 80,
                                    color = color.red,
                                    x = games.gscreen.width/2,
                                    y = games.gscreen.height/2,
                                    # interval = 500 * games.gscreen.fps,
                                    # after_death = games.gscreen.quit,
                                    is_collideable = False)
        games.gscreen.add(end_message)
        self.refresh()
        for i in range(1,200,1):
            games.gscreen._wait_frame()
        games.pygame.quit()
        sys.exit(0)

#def main():
    

    #myGame = Game()
    #myGame.setup()
    # myGame.autoplay()
    
    
# kick it off!
#main()
