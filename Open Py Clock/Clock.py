import Tkinter as tk
import tkFont
import datetime
import os
from PIL import Image, ImageTk
import tkMessageBox
  
class Clock(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.parent = master
        
        self.usesBackgroundImage = 0
        self.backgroundHasChanged = True
        self.backgroundImageLocation = ""
        self.backgroundImageX = 0
        self.backgroundImageY = 0
        self.backgroundImageScaleX = 100
        self.backgroundImageScaleY = 100
        self.top = self.winfo_toplevel()
        self.shouldDrawClock = 1
        self.symbols = dict()
        
        self.getClockOptions()
        
        self.createWidgets()
    
    # A bunch of setters and getters
    # All booleans should be specified with 1 or 0, not True or False
    
    # x is x coord
    # y is y coord
    # font is the exact font name to use from the system list of fonts
    # size is the font size to use
    # colour is a hex value for said colour
    # on is whether the option should be visible (1 for visible, 0 for hidden)

    # uses12HourFormat = 1: show hour in 1-12, am pm format (otherwise 24 hour format)
    # leadingZeroes = 1: show leading zeroes for hour (otherwise no leading zeroes)
    def setHour(self, x, y, font, size, colour, uses12HourTime, leadingZeroes, on):
        self.hourX = int(x)
        self.hourY = int(y) 
        self.hourFont = font
        self.hourSize = int(size)
        self.hourFontColour = colour
        self.uses12HourTime = int(uses12HourTime)
        self.hourOn = on
        self.hourLeadingZeroes = leadingZeroes
    
    def getHour(self):
        x = [str(self.hourX),
             str(self.hourY), 
             self.hourFont,
             str(self.hourSize),
             self.hourFontColour,
             self.uses12HourTime,
             self.hourLeadingZeroes,
             self.hourOn]
        return x
        
    def setMinute(self, x, y, font, size, colour, on):
        self.minuteX = int(x)
        self.minuteY = int(y)
        self.minuteFont = font
        self.minuteSize = int(size)
        self.minuteFontColour = colour
        self.minuteOn = on
        
    def getMinute(self):
        x = [self.minuteX,
             self.minuteY, 
             self.minuteFont,
             self.minuteSize,
             self.minuteFontColour,
             self.minuteOn]
        return x
        
    def setSecond(self, x, y, font, size, colour, on):
        self.secondX = int(x)
        self.secondY = int(y)
        self.secondFont = font
        self.secondSize = int(size)
        self.secondFontColour = colour
        self.secondOn = on
        
    def getSecond(self):
        x = [self.secondX,
             self.secondY, 
             self.secondFont,
             self.secondSize,
             self.secondFontColour,
             self.secondOn]
        return x
    
    # longMonth = 1: Month is show in English written form (otherwise uses 1-12)
    def setMonth(self, x, y, font, size, colour, longMonth, on):
        self.monthX = int(x)
        self.monthY = int(y)
        self.monthFont = font
        self.monthSize = int(size) 
        self.monthFontColour = colour
        if longMonth:
            self.longMonth = 1
        else:
            self.longMonth = 0
        self.monthOn = on
    
    def getMonth(self):
        x = [self.monthX,
             self.monthY, 
             self.monthFont,
             self.monthSize,
             self.monthFontColour,
             self.longMonth,
             self.monthOn]
        return x
    
    def setDayNumber(self, x, y, font, size, colour, on):
        self.dayNumberX = int(x)
        self.dayNumberY = int(y)
        self.dayNumberFont = font
        self.dayNumberSize = int(size)
        self.dayNumberFontColour = colour
        self.dayNumberOn = on
    
    def getDayNumber(self):
        x = [self.dayNumberX,
             self.dayNumberY, 
             self.dayNumberFont,
             self.dayNumberSize,
             self.dayNumberFontColour,
             self.dayNumberOn]
        return x
    
    def setDayOfWeek(self, x, y, font, size, colour, on):
        self.dayOfWeekX = int(x)
        self.dayOfWeekY = int(y)
        self.dayOfWeekFont = font
        self.dayOfWeekSize = int(size)  
        self.dayOfWeekFontColour = colour
        self.dayOfWeekOn = on
    
    def getDayOfWeek(self):
        x = [self.dayOfWeekX,
             self.dayOfWeekY, 
             self.dayOfWeekFont,
             self.dayOfWeekSize,
             self.dayOfWeekFontColour, 
             self.dayOfWeekOn]
        return x
    
    def setYear(self, x, y, font, size, colour, on):
        self.yearX = int(x)
        self.yearY = int(y)
        self.yearFont = font
        self.yearSize = int(size)
        self.yearFontColour = colour
        self.yearOn = on
    
    def getYear(self):
        x = [self.yearX,
             self.yearY, 
             self.yearFont,
             self.yearSize,
             self.yearFontColour,
             self.yearOn]
        return x
     
    def setAMPM(self, x, y, font, size, colour, on):
        self.ampmX = int(x)
        self.ampmY = int(y)
        self.ampmFont = font
        self.ampmSize = int(size)
        self.ampmFontColour = colour
        self.ampmOn = on
    
    def getAMPM(self):
        x = [self.ampmX,
             self.ampmY, 
             self.ampmFont,
             self.ampmSize,
             self.ampmFontColour,
             self.ampmOn]
        return x
    
    # Adds a symbol if its idNum doesnt exist, otherwise sets the existing one
    # sym is the string to be saved
    # idNum is the id of the symbol (use len(symbols) to get id for new entry)
    def setSymbol(self, x, y, font, size, colour, idNum, sym, on):
        if idNum in self.symbols:
            cur = self.symbols[idNum]
        else:
            cur = dict()
            cur['idNum'] = idNum
            
        cur['x'] = x
        cur['y'] = y
        cur['font'] = font
        cur['size'] = size
        cur['colour'] = colour
        cur['on'] = on
        cur['sym'] = sym
        self.symbols[idNum] = cur
    
    def getSymbols(self):
        return self.symbols
    
    def removeSymbol(self, idNum):
        del self.symbols[idNum]

    # Sets the background image given arguments
    # scaleX and scaleY are percentages to scale
    # For 'location' can take a valid path, 'same' for same as current,
    # or 'none' to clear
    def setBackgroundImage(self, x, y, scaleX, scaleY, location):
        # If location is the same as current perform operations on current
        if location == "same":
            self.backgroundImageX = int(x)
            self.backgroundImageY = int(y)
            self.backgroundImageScaleX = int(scaleX)
            self.backgroundImageScaleY = int(scaleY)
            image = Image.open(self.backgroundImageLocation)
            size = image.size
            scaleX = long(scaleX)
            scaleY = long(scaleY)
            finalX = long(size[0] * scaleX/100)
            finalY = long(size[1] * scaleY/100)
            image = image.resize( (finalX, finalY ),
                                  Image.ANTIALIAS)
            self.image = image
            self.backgroundImage = ImageTk.PhotoImage(image)
        # If location is none reset background image information
        elif location == "none":
            self.usesBackgroundImage = 0
            self.backgroundImage = ""
            self.image = None
            self.backgroundImageScaleX = 100
            self.backgroundImageScaleY = 100
            self.backgroundImageX = 0
            self.backgroundImageY = 0
            self.backgroundImageLocation = ""
        # Otherwise attempt to load the new image
        else:
            try:
                # Get image and handle resizing
                image = Image.open(location)
                
                size = image.size
                scaleX = long(scaleX)
                scaleY = long(scaleY)
                finalX = long(size[0] * scaleX/100)
                finalY = long(size[1] * scaleY/100)
                image = image.resize( (finalX, finalY ),
                                      Image.ANTIALIAS)
                
                # Set new data
                self.image = image
                self.backgroundImage = ImageTk.PhotoImage(image)
                self.backgroundImageX = int(x)
                self.backgroundImageY = int(y)
                self.backgroundImageScaleX = int(scaleX)
                self.backgroundImageScaleY = int(scaleY)
                self.backgroundImageLocation = location
                self.usesBackgroundImage = 1
            except IOError:
                # If you get an error, stop the clock and reset image data
                self.shouldDrawClock = 0
                tkMessageBox.showerror("No image found",
                                       "Could not find an image at " + self.backgroundImageLocation
                                       + ".")
                self.setBackgroundImage(0, 0, 0, 0, "none")
                self.shouldDrawClock = 1
        self.backgroundHasChanged = True

    def setBackgroundColour(self, colour):
        self.backgroundColour = colour
        self.backgroundHasChanged = True
        
    def setBackgroundTiling(self, b):
        self.tilesBackground = b
        self.backgroundHasChanged = True
    
    def getBackgroundInformation(self):
        x = [self.backgroundColour,
             self.backgroundImageLocation,
             self.backgroundImageX,
             self.backgroundImageY,
             self.backgroundImageScaleX,
             self.backgroundImageScaleY,
             self.tilesBackground]
        return x
    
    # Set defaults (in case of no prefs file)
    def setDefaults(self):
        # Get default font
        fonts = tkFont.families(self)
        fonts = set(fonts)
        defaultFont = "Courier"
        for font in fonts:
            if ("COURIER" in font.upper()):
                defaultFont = font
                break
        
        # Set default values
        self.setHour(30, 10, defaultFont, 13, "#000000", 1, 1, 1)
        self.setMinute(60, 10, defaultFont, 13, "#000000", 1)
        self.setSecond(90, 10, defaultFont, 13, "#000000", 1)
        self.setAMPM(100, 10, defaultFont, 13, "#000000", 1)
        self.setDayOfWeek(10, 100, defaultFont, 13, "#000000", 1)
        self.setMonth(10, 130, defaultFont, 13, "#000000", 1, 1)
        self.setDayNumber(10, 160, defaultFont, 13, "#000000", 1)
        self.setYear(10, 190, defaultFont, 13, "#000000", 1)
        self.setBackgroundColour("#ffffff")
        self.setBackgroundTiling(0)
    
    # Adds widgets to screen
    def createWidgets(self):
        
        # Add canvas for clock
        self.canvas = tk.Canvas(self, highlightthickness = 0)
        self.canvas.pack(fill="both", expand="yes")
        
        # Begin clock
        self.drawClock()
    
    # Resizes canvas to match window
    def onResize(self, event):
        self.top.withdraw
        print(event.height, event.width)
        self.canvas.config(height = event.height, width = event.width)
        self.backgroundHasChanged = True
        self.top.iconify

    # Starts the cycle for updateClock
    def drawClock(self):
        if self.shouldDrawClock:
            self.updateClock()
            self.after(1000, self.drawClock)

    # Actually handles refreshing the clock on screen
    def updateClock(self): 
        try:
            # Clear canvas and draw background if its been changed
            if self.backgroundHasChanged:
                self.canvas.delete("all")
                
                if (self.usesBackgroundImage):
                    if (self.tilesBackground):
                        self.tileBackground()
                    
                    else:
                        self.canvas.create_image(int(self.backgroundImageX),
                                                   int(self.backgroundImageY),
                                                   image=self.backgroundImage,
                                      anchor="nw")
    
                self.canvas.config(background=self.backgroundColour)
                self.backgroundHasChanged = False
            else:
                self.canvas.delete("fitem")
            
            current = datetime.datetime.today()
            
            # Draw hour
            if self.hourOn:
                hour = current.hour
                
                if (self.uses12HourTime):
                    if hour == 0:
                        hour = 12
                    elif hour > 12:
                        hour = hour - 12
                
                hour = str(hour)
                if self.hourLeadingZeroes:
                    if int(hour) < 10:
                        hour = "0" + hour
                         
                hour = self.canvas.create_text(self.hourX, self.hourY, text=hour,
                                          font=(self.hourFont, self.hourSize),
                                          fill=self.hourFontColour, tag="fitem",
                                          anchor="ne")
                self.hourbbox = self.canvas.bbox(hour)
            
            # Draw minute
            if self.minuteOn:
                minute = current.minute
                minute = str(minute)
                minute = str(minute).zfill(2)
                minute = self.canvas.create_text(self.minuteX, self.minuteY, text=minute,
                                          font=(self.minuteFont, self.minuteSize),
                                          fill=self.minuteFontColour, tag="fitem",
                                          anchor="ne")
                self.minutebbox = self.canvas.bbox(minute)
            
            # Draw second
            if self.secondOn:
                second = current.second
                second = str(second)
                second = str(second).zfill(2)
                second = self.canvas.create_text(self.secondX, self.secondY, text=second,
                                          font=(self.secondFont, self.secondSize),
                                          fill=self.secondFontColour, tag="fitem",
                                          anchor="ne")
                self.secondbbox = self.canvas.bbox(second)
            
            # Draw month
            if self.monthOn:
                month = current.month
                if self.longMonth:
                    month = current.strftime("%B")
                else:
                    month = str(month)
                month = self.canvas.create_text(self.monthX, self.monthY, text=month,
                                          font=(self.monthFont, self.monthSize),
                                          fill=self.monthFontColour, tag="fitem",
                                          anchor="nw")
                self.monthbbox = self.canvas.bbox(month)
            
            # Draw day of week
            if self.dayOfWeekOn: 
                dayOfWeek = current.weekday()
                
                if dayOfWeek == 0:
                    dayOfWeek = "Monday"
                elif dayOfWeek == 1:
                    dayOfWeek = "Tuesday"
                elif dayOfWeek == 2:
                    dayOfWeek = "Wednesday"
                elif dayOfWeek == 3:
                    dayOfWeek = "Thursday"
                elif dayOfWeek == 4:
                    dayOfWeek = "Friday"
                elif dayOfWeek == 5:
                    dayOfWeek = "Saturday"
                elif dayOfWeek == 6:
                    dayOfWeek = "Sunday"
                
                dayOfWeek = self.canvas.create_text(self.dayOfWeekX, self.dayOfWeekY,
                                          text=dayOfWeek,
                                          font=(self.dayOfWeekFont, self.dayOfWeekSize),
                                          fill=self.dayOfWeekFontColour, tag="fitem",
                                          anchor="nw")
                self.dayOfWeekbbox = self.canvas.bbox(dayOfWeek)
            
            # Draw day number
            if self.dayNumberOn:
                dayNumber = current.day
                dayNumber = str(dayNumber)
                dayNumber = self.canvas.create_text(self.dayNumberX, self.dayNumberY,
                                          text=dayNumber,
                                          font=(self.dayNumberFont, self.dayNumberSize),
                                          fill=self.dayNumberFontColour, tag="fitem",
                                          anchor="nw")
                self.dayNumberbbox = self.canvas.bbox(dayNumber)  
            
            # Draw year
            if self.yearOn:
                year = current.year
                year = str(year)
                year = self.canvas.create_text(self.yearX, self.yearY, text=year,
                                          font=(self.yearFont, self.yearSize),
                                          fill=self.yearFontColour, tag="fitem",
                                          anchor="nw")
                self.yearbbox = self.canvas.bbox(year)
            
            # Draw AM/PM
            if self.ampmOn:                          
                ampm = "AM"
                hour = current.hour
                if hour >= 12 :
                    ampm = "PM"
                ampm = self.canvas.create_text(self.ampmX, self.ampmY, text=ampm,
                                          font=(self.ampmFont, self.ampmSize),
                                          fill=self.ampmFontColour, tag="fitem",
                                          anchor="nw")
                self.ampmbbox = self.canvas.bbox(ampm)
            self.symbolbboxes = list()
            
            # Draw symbols
            for item in self.symbols:
                cur = self.symbols[item]
                symbol = self.canvas.create_text(cur['x'], cur['y'], text=cur['sym'],
                                          font=(cur['font'], cur['size']),
                                          fill=cur['colour'], tag="fitem",
                                          anchor="nw")
                self.symbolbboxes.append(self.canvas.bbox(symbol))
                
                
        except:
            self.shouldDrawClock = 0
            tkMessageBox.showerror("Problems drawing clock",
                                   "The clock could not be drawn with current settings. " + 
                                   "This could because of a corrupt preferences file or " + 
                                   "an internal error. Try deleting the 'prefs' folder " + 
                                   "and try again.")
            self.quit()
            
    # Tiles the background image for updateClock
    def tileBackground(self):
        x = int(self.backgroundImageX)
        y = int(self.backgroundImageY)
        
        size = self.image.size
        
        screenX = self.winfo_screenwidth()
        screenY = self.winfo_screenheight()
        
        # Perform tiling
        while x < screenX:
            self.canvas.create_image(x, y, image = self.backgroundImage,
                                  anchor = "nw")
            
            while y < screenY:
                self.canvas.create_image(x, y, image = self.backgroundImage,
                                  anchor = "nw")
                y += size[1]
            y = 0
            x += size[0]
        
        
    # Saves current clock options to local prefs file
    def saveClockOptions(self):
        
        if not os.path.exists("prefs"):
            os.makedirs("prefs")
        
        f = open('prefs/clock_prefs.dat', 'w+')
        
        # Write background information
        f.write(str(self.backgroundColour) + "\n")
        f.write(str(self.usesBackgroundImage) + "\n")
        f.write(str(self.backgroundImageLocation) + "\n")
        f.write(str(self.backgroundImageX) + "\n")
        f.write(str(self.backgroundImageY) + "\n")
        f.write(str(self.backgroundImageScaleX) + "\n")
        f.write(str(self.backgroundImageScaleY) + "\n")
        f.write(str(self.tilesBackground) + "\n")
        
        # Write hour information
        f.write(str(self.hourX) + "\n")
        f.write(str(self.hourY) + "\n")
        f.write(str(self.hourFont) + "\n")
        f.write(str(self.hourSize) + "\n")
        f.write(str(self.hourFontColour) + "\n")
        f.write(str(self.uses12HourTime) + "\n")
        f.write(str(self.hourLeadingZeroes) + "\n")
        f.write(str(self.hourOn) + "\n")
        
        # Write minute information
        f.write(str(self.minuteX) + "\n")
        f.write(str(self.minuteY) + "\n")
        f.write(str(self.minuteFont) + "\n")
        f.write(str(self.minuteSize) + "\n")
        f.write(str(self.minuteFontColour) + "\n")
        f.write(str(self.minuteOn) + "\n")
        
        # Write second information
        f.write(str(self.secondX) + "\n")
        f.write(str(self.secondY) + "\n")
        f.write(str(self.secondFont) + "\n")
        f.write(str(self.secondSize) + "\n")
        f.write(str(self.secondFontColour) + "\n")
        f.write(str(self.secondOn) + "\n")
        
        # Write year information
        f.write(str(self.yearX) + "\n")
        f.write(str(self.yearY) + "\n")
        f.write(str(self.yearFont) + "\n")
        f.write(str(self.yearSize) + "\n")
        f.write(str(self.yearFontColour) + "\n")
        f.write(str(self.yearOn) + "\n")
        
        # Write month information
        f.write(str(self.monthX) + "\n")
        f.write(str(self.monthY) + "\n")
        f.write(str(self.monthFont) + "\n")
        f.write(str(self.monthSize) + "\n")
        f.write(str(self.monthFontColour) + "\n")
        f.write(str(self.longMonth) + "\n")
        f.write(str(self.monthOn) + "\n")
        
        # Write day number information
        f.write(str(self.dayNumberX) + "\n")
        f.write(str(self.dayNumberY) + "\n")
        f.write(str(self.dayNumberFont) + "\n")
        f.write(str(self.dayNumberSize) + "\n")
        f.write(str(self.dayNumberFontColour) + "\n")
        f.write(str(self.dayNumberOn) + "\n")
        
        # Write day of week information
        f.write(str(self.dayOfWeekX) + "\n")
        f.write(str(self.dayOfWeekY) + "\n")
        f.write(str(self.dayOfWeekFont) + "\n")
        f.write(str(self.dayOfWeekSize) + "\n")
        f.write(str(self.dayOfWeekFontColour) + "\n")
        f.write(str(self.dayOfWeekOn) + "\n")
        
        # Write AM/PM information
        f.write(str(self.ampmX) + "\n")
        f.write(str(self.ampmY) + "\n")
        f.write(str(self.ampmFont) + "\n")
        f.write(str(self.ampmSize) + "\n")
        f.write(str(self.ampmFontColour) + "\n")
        f.write(str(self.ampmOn) + "\n")
        
        # Write symbol information
        
        for item in self.symbols:
            f.write(str(self.symbols[item]["x"]) + "\n")
            f.write(str(self.symbols[item]["y"]) + "\n")
            f.write(str(self.symbols[item]["font"]) + "\n")
            f.write(str(self.symbols[item]["size"]) + "\n")
            f.write(str(self.symbols[item]["colour"]) + "\n")
            f.write(str(self.symbols[item]["idNum"]) + "\n")
            f.write(str(self.symbols[item]["sym"]) + "\n")
            f.write(str(self.symbols[item]["on"]) + "\n")
        
    # Gets clock options from local prefs file
    def getClockOptions(self):
        if os.path.exists("prefs/clock_prefs.dat"):
            f = open('prefs/clock_prefs.dat', 'r')
          
            # Get background information
            self.backgroundColour = f.readline().strip()
            self.usesBackgroundImage = int(f.readline().strip())
            self.backgroundImageLocation = f.readline().strip()
            self.backgroundImageX = int(f.readline().strip())
            self.backgroundImageY = int(f.readline().strip())
            self.backgroundImageScaleX = int(f.readline().strip())
            self.backgroundImageScaleY = int(f.readline().strip())
            self.tilesBackground = int(f.readline().strip())
            
            # Set background image if its been used
            if (self.usesBackgroundImage):
                self.setBackgroundImage(self.backgroundImageX, 
                                        self.backgroundImageY,
                                        self.backgroundImageScaleX,
                                        self.backgroundImageScaleY, 
                                        self.backgroundImageLocation)
            
            # Get hour information
            self.hourX = int(f.readline())
            self.hourY = int(f.readline())
            self.hourFont = f.readline().strip()
            self.hourSize = int(f.readline())
            self.hourFontColour = f.readline().strip()
            self.uses12HourTime = int(f.readline().strip())
            self.hourLeadingZeroes = int(f.readline().strip())
            self.hourOn = int(f.readline().strip())
            
            # Get minute information
            self.minuteX = int(f.readline())
            self.minuteY = int(f.readline())
            self.minuteFont = f.readline().strip()
            self.minuteSize = int(f.readline())
            self.minuteFontColour = f.readline().strip()
            self.minuteOn = int(f.readline().strip())
            
            # Get second information
            self.secondX = int(f.readline())
            self.secondY = int(f.readline())
            self.secondFont = f.readline().strip()
            self.secondSize = int(f.readline())
            self.secondFontColour = f.readline().strip()
            self.secondOn = int(f.readline().strip())
            
            # Get year information
            self.yearX = int(f.readline())
            self.yearY = int(f.readline())
            self.yearFont = f.readline().strip()
            self.yearSize = int(f.readline())
            self.yearFontColour = f.readline().strip()
            self.yearOn = int(f.readline().strip())
        
            # Get month information
            self.monthX = int(f.readline())
            self.monthY = int(f.readline())
            self.monthFont = f.readline().strip()
            self.monthSize = int(f.readline())
            self.monthFontColour = f.readline().strip()
            self.longMonth = int(f.readline().strip())
            self.monthOn = int(f.readline().strip())
            
            # Get day number information
            self.dayNumberX = int(f.readline())
            self.dayNumberY = int(f.readline())
            self.dayNumberFont = f.readline().strip()
            self.dayNumberSize = int(f.readline())
            self.dayNumberFontColour = f.readline().strip()
            self.dayNumberOn = int(f.readline().strip())
            
            # Get day of week information
            self.dayOfWeekX = int(f.readline())
            self.dayOfWeekY = int(f.readline())
            self.dayOfWeekFont = f.readline().strip()
            self.dayOfWeekSize = int(f.readline())
            self.dayOfWeekFontColour = f.readline().strip()
            self.dayOfWeekOn = int(f.readline().strip())

            # Get AM/PM information
            self.ampmX = int(f.readline())
            self.ampmY = int(f.readline())
            self.ampmFont = f.readline().strip()
            self.ampmSize = int(f.readline())
            self.ampmFontColour = f.readline().strip()
            self.ampmOn = int(f.readline().strip())
            
            # Get symbol information
            flag = True
            while(flag):
                line = f.readline()
                if line:
                    cur = dict()
                    cur['x'] = int(line)
                    cur['y'] = int(f.readline().strip())
                    cur['font'] = f.readline().strip()
                    cur['size'] = int(f.readline().strip())
                    cur['colour'] = f.readline().strip()
                    cur["idNum"] = int(f.readline().strip())
                    cur['sym'] = f.readline().strip()
                    cur['on'] = int(f.readline().strip())
                    self.symbols[cur["idNum"]] = cur
                else:
                    flag = False
        else:
            self.setDefaults()
 
    # Begins drag and drop placement mode
    def beginDragMode(self):
        # Stop the clock
        self.shouldDrawClock = 0
        
        # Record original values
        self.originalHourX = self.hourX
        self.originalHourY = self.hourY
        self.originalMinuteX = self.minuteX
        self.originalMinuteY = self.minuteY
        self.originalSecondX = self.secondX
        self.originalSecondY = self.secondY
        self.originalYearX = self.yearX
        self.originalYearY = self.yearY
        self.originalMonthX = self.monthX
        self.originalMonthY = self.monthY
        self.originalDayNumberX = self.dayNumberX
        self.originalDayNumberY = self.dayNumberY
        self.originalDayOfWeekX = self.dayOfWeekX
        self.originalDayOfWeekY = self.dayOfWeekY
        self.originalAmpmX = self.ampmX
        self.originalAmpmY = self.ampmY
        symbolCoords = list()
        for item in self.symbols:
            item = self.symbols[item]
            curCoords = (item['x'], item['y'])
            print(curCoords)
            symbolCoords.append(curCoords)
            
        self.originalSymbolCoords = symbolCoords
        
        # Bind listeners for dragging
        self.canvas.bind("<Button-1>", self.checkIfClickedItem) 
        
        # Draw drag boxes for first time
        self.drawDragBoxes()
        
        # Let the user know what's going on
        tkMessageBox.showinfo("Entering Drag Mode", "To exit this mode, hit Escape")
        
        # Bring clock into focus
        self.focus()
    
     
    # Checks if an item was clicked and binds drag listener if so  
    def checkIfClickedItem(self, event):
        # Stop listening for drag input
        self.canvas.unbind("<B1-Motion>")
        
        # Reset indicators
        self.clickedFlags = [False,
                             False,
                             False,
                             False,
                             False,
                             False,
                             False,
                             False,
                             False]
        
        bounds = [self.findCentre(self.hourbbox),
          self.findCentre(self.minutebbox),
          self.findCentre(self.secondbbox),
          self.findCentre(self.ampmbbox),
          self.findCentre(self.yearbbox),
          self.findCentre(self.monthbbox),
          self.findCentre(self.dayNumberbbox),
          self.findCentre(self.dayOfWeekbbox)]
        
        for item in self.symbolbboxes:
            bounds.append(self.findCentre(item))
        
        # Find clicks
        i = 0
        for item in bounds:
            if (event.x in range(item[0] - 5, item[0] + 5) and
                        event.y in range (item[1] - 5, item[1] + 5)):
                if i < 8:
                    self.clickedFlags[i] = True
                else:
                    self.clickedFlags[8] = True
                    self.clickedSymbol = i - 8
                self.canvas.bind("<B1-Motion>", self.dragItem)
                return
            i+=1
        
        self.drawDragBoxes()
    
    # Handles dragging a selected item across the clock
    def dragItem(self, event):
        maxX = self.winfo_screenwidth()
        maxY = self.winfo_screenheight()
        
        bounds = (self.findCentre(self.hourbbox),
          self.findCentre(self.minutebbox),
          self.findCentre(self.secondbbox),
          self.findCentre(self.ampmbbox),
          self.findCentre(self.yearbbox),
          self.findCentre(self.monthbbox),
          self.findCentre(self.dayNumberbbox),
          self.findCentre(self.dayOfWeekbbox))
        
        
        # Check if out of range, otherwise drag selected item
        if (event.x < 0 or event.y < 0 
            or event.x > maxX or event.y > maxY ):
            return
        
        self.hourDragged = self.clickedFlags[0]
        self.minuteDragged = self.clickedFlags[1]
        self.secondDragged = self.clickedFlags[2]
        self.ampmDragged = self.clickedFlags[3]
        self.yearDragged = self.clickedFlags[4]
        self.monthDragged = self.clickedFlags[5]
        self.dayNumberDragged = self.clickedFlags[6]
        self.dayOfWeekDragged = self.clickedFlags[7]
        self.symbolDragged = self.clickedFlags[8]
        
        if self.hourDragged:
            difx = event.x - bounds[0][0]
            dify = event.y - bounds[0][1]
            self.hourX = self.hourX + difx
            self.hourY = self.hourY + dify
            
        elif self.minuteDragged:
            difx = event.x - bounds[1][0]
            dify = event.y - bounds[1][1]
            self.minuteX = self.minuteX + difx
            self.minuteY = self.minuteY + dify
            
        elif self.secondDragged:
            difx = event.x - bounds[2][0]
            dify = event.y - bounds[2][1]
            self.secondX = self.secondX + difx
            self.secondY = self.secondY + dify
        
        elif self.ampmDragged:
            difx = event.x - bounds[3][0]
            dify = event.y - bounds[3][1]
            self.ampmX = self.ampmX + difx
            self.ampmY = self.ampmY + dify
            
        elif self.yearDragged:
            difx = event.x - bounds[4][0]
            dify = event.y - bounds[4][1]
            self.yearX = self.yearX + difx
            self.yearY = self.yearY + dify
        
        elif self.monthDragged:
            difx = event.x - bounds[5][0]
            dify = event.y - bounds[5][1]
            self.monthX = self.monthX + difx
            self.monthY = self.monthY + dify
        
        elif self.dayNumberDragged:
            difx = event.x - bounds[6][0]
            dify = event.y - bounds[6][1]
            self.dayNumberX = self.dayNumberX + difx
            self.dayNumberY = self.dayNumberY + dify
            
        elif self.dayOfWeekDragged:
            difx = event.x - bounds[7][0]
            dify = event.y - bounds[7][1]
            self.dayOfWeekX = self.dayOfWeekX + difx
            self.dayOfWeekY = self.dayOfWeekY + dify
        
        elif self.symbolDragged:
            s = self.symbols[self.clickedSymbol]
            sb = self.symbolbboxes[self.clickedSymbol]
            
            difx = event.x - sb[0]
            dify = event.y - sb[1]
            s["x"] = int(s["x"]) + difx
            s["y"] = int(s["y"]) + dify
            
        self.updateClock()
        self.drawDragBoxes()
        
    # Draws a box over each draggable item
    def drawDragBoxes(self): 
        bounds = [self.findCentre(self.hourbbox),
                  self.findCentre(self.minutebbox),
                  self.findCentre(self.secondbbox),
                  self.findCentre(self.yearbbox),
                  self.findCentre(self.monthbbox),
                  self.findCentre(self.dayNumberbbox),
                  self.findCentre(self.dayOfWeekbbox),
                  self.findCentre(self.ampmbbox)]
        for item in self.symbolbboxes:
            bounds.append(self.findCentre(item))
        
        for item in bounds:
            self.canvas.create_rectangle(item[0] - 5,
                               item[1] - 5,
                               item[0] + 5,
                               item[1] + 5,
                               fill = "#FFFFFF", tag = "fitem",
                                outline = "#000000",
                                width = 2.0,
                                stipple="gray50")


    # Handles leaving drag mode   
    def endDragMode(self):
        # Unbind listeners
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        
        # Ask to save changes
        if not tkMessageBox.askyesno("Confirm", "Save changes?") :
            self.hourX = self.originalHourX
            self.hourY = self.originalHourY
            self.minuteX = self.originalMinuteX
            self.minuteY = self.originalMinuteY
            self.secondX = self.originalSecondX
            self.secondY = self.originalSecondY
            self.yearX = self.originalYearX
            self.yearY = self.originalYearY
            self.monthX = self.originalMonthX
            self.monthY = self.originalMonthY
            self.dayNumberX = self.originalDayNumberX
            self.dayNumberY = self.originalDayNumberY
            self.dayOfWeekX = self.originalDayOfWeekX
            self.dayOfWeekY = self.originalDayOfWeekY
            self.ampmX = self.originalAmpmX
            self.ampmY = self.originalAmpmY
            for item in self.symbols:
                self.symbols[item]['x'] = self.originalSymbolCoords[item][0]
                self.symbols[item]['y'] = self.originalSymbolCoords[item][1]
        
        # Restart clock
        self.shouldDrawClock = 1
        self.drawClock()
        self.lift()
        self.focus()
        self.saveClockOptions()
    
    # Given a bbox, returns the x,y coords in the very middle of it
    def findCentre(self, bbox):
        topx = bbox[0]
        topy = bbox[1]
        botx = bbox[2]
        boty = bbox[3]
        
        difx = botx - topx
        dify = boty - topy
        
        difx = difx/2
        dify = dify/2
        
        difx = topx + difx
        dify = topy + dify
        
        return (difx, dify)