import Tkinter as tk
import Clock
import Options
import platform
import tkMessageBox
import os

class Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack(fill = "both", expand = "yes")
        self.top = self.winfo_toplevel()
        self.optionsOpen = False
        self.windowOptionsOpen = False
        self.isFullscreen = False
        self.top.protocol("WM_DELETE_WINDOW", self.close)
        
        self.getWindowOptions()
        
        self.createWidgets()
        
        if self.fullscreenOnStart:
            self.goFullscreen()
        
        self.top.geometry(str(self.windowX) + "x" + str(self.windowY))
        self.update()
    
    # Setter for options open       
    def setOptions(self, b):
        self.optionsOpen = b
    
    def createWidgets(self):
        # Add clock
        self.clock = Clock.Clock(self)
        self.clock.pack(fill = "both", expand = "yes")
        
        # Declare popup menus
        self.menu1 = tk.Menu(self, tearoff=0)
        self.menu1.add_command(label = "Options", command = self.openOptions)
        self.menu1.add_command(label = "Fullscreen", command = self.goFullscreen)
        
        self.menu2 = tk.Menu(self, tearoff=0)
        self.menu2.add_command(label = "Options", command = self.openOptions)
        self.menu2.add_command(label = "Stop fullscreen", command = self.stopFullscreen)
        
        # Bind popup menu listeners
        self.top.bind("<FocusOut>", self.stopPopup)
        self.top.bind("<Button-1>", self.stopPopup)
        
        if platform.system() != "Linux" and platform.system() != "Windows":
            self.top.bind("<Button-2>", self.popup)
        else:
            self.top.bind("<Button-3>", self.popup)
        
        # Bind resizing listener
        self.bind("<Configure>", self.onResize)
    
    # Resize listener to update clock canvas size and send values to options window
    def onResize(self, event):
        self.top.withdraw
        self.clock.onResize(event)
        if self.windowOptionsOpen:
            self.optionsWindow.windowOptions.xVar.set(event.width)
            self.optionsWindow.windowOptions.yVar.set(event.height)
        self.top.iconify
    
    # Handler for opening the options window
    def openOptions(self):
        if not self.optionsOpen:
            self.optionsOpen = True
            self.optionsWindow = Options.Options(self)
        else:
            self.optionsWindow.top.focus()
            self.optionsWindow.top.lift()
            
    # Handler for opening popup menu
    def popup(self, event):
        if (self.isFullscreen):
            self.menu2.post(event.x_root, event.y_root)
        else:    
            self.menu1.post(event.x_root, event.y_root)
    
    # Handler for closing popup menu
    def stopPopup(self, event = None):
        self.menu1.unpost()
        self.menu2.unpost()
    
    # Handler for fullscreen option in popup
    def goFullscreen(self):
        self.top.withdraw
        self.top.attributes("-fullscreen", True)
        self.isFullscreen = True
        self.top.iconify
    
    # Handler for stop fullscreen option in popup
    def stopFullscreen(self):
        self.top.withdraw
        self.top.attributes("-fullscreen", False)
        self.isFullscreen = False
        self.top.iconify
    
    # Begins drag mode; unbinds popup listener, binds exit listeners,
    # tells clock to begin drag mode
    def beginDragMode(self):
        self.stopPopup()
        if platform.system() != "Linux" and platform.system() != "Windows":
            self.top.unbind("<Button-2>")
        else:
            self.top.unbind("<Button-3>")
        
        self.top.attributes("-topmost", 1)
        
        self.top.bind("<FocusOut>", self.checkIfDragModeDone)
        self.top.bind("<Escape>", self.checkIfDragModeDone)
        self.clock.beginDragMode()
        
    # Handler for focusout in drag and drop mode
    def checkIfDragModeDone(self, event=None):
        self.top.unbind("<FocusOut>")
        if (tkMessageBox.askyesno("Confirm", "End drag mode?")):
            self.endDragMode()
        else:
            self.top.bind("<FocusOut>", self.checkIfDragModeDone)
        
    # Ends drag mode; unbinds exit listeners, binds regular popup listener
    def endDragMode(self, event=None):
        self.clock.endDragMode()
        self.top.unbind("<FocusOut>")
        self.top.unbind("<Escape>")
        if platform.system() != "Linux" and platform.system() != "Windows":
            self.top.bind("<Button-2>", self.popup)
        else:
            self.top.bind("<Button-3>", self.popup)
        self.top.bind("<FocusOut>", self.stopPopup)
        self.top.attributes("-topmost", 0)
        self.optionsWindow.foregroundOptions.showOptions("Hour")
        self.optionsWindow.top.lift()
    
    # Handles closing to prevent lost changes
    def close(self):
        if self.optionsOpen:
            if (tkMessageBox.askyesno("Confirm", "The options menu is open. " +
                                      "Close Open Py Clock? Unsaved changes " +
                                      "will be lost.")):
                self.quit()
        else:
            self.quit()
    
    # Gets the current options saved for the window; if not there, makes a new one
    def getWindowOptions(self):
        if os.path.exists("prefs/window_prefs.dat"):
            f = open('prefs/window_prefs.dat', 'r')
        else:
            self.initializeWindowOptions()
            f = open('prefs/window_prefs.dat', 'r')
        
        self.windowX = int(f.readline())
        self.windowY = int(f.readline())
        self.fullscreenOnStart = int(f.readline())
        
    # Initializes window_prefs.dat if its not present
    def initializeWindowOptions(self):
        if not os.path.exists("prefs"):
                os.makedirs("prefs")
        f = open('prefs/window_prefs.dat', 'w+')
        
        f.write("378\n")
        f.write("265\n")
        f.write("0\n")
        f.close()