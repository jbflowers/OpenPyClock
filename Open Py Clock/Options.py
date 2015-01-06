import Tkinter as tk
from ttk import Notebook
import ClockForegroundOptions
import ClockBackgroundOptions
import WindowOptions
class Options:

    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.parent = parent
        self.top.grid()
        self.top.clock = parent.clock
        self.top.close = self.close
        
        self.top.wm_title("Options")
    
        self.top.protocol("WM_DELETE_WINDOW", self.close)
        
        self.createWidgets()    
    
    def createWidgets(self):
        n = Notebook(self.top)
        
        self.foregroundOptions = ClockForegroundOptions.ClockForegroundOptions(self.top, self)
        self.backgroundOptions = ClockBackgroundOptions.ClockBackgroundOptions(self.top, self)
        self.windowOptions = WindowOptions.WindowOptions(self.top, self)
        
        n.add(self.foregroundOptions, text = "Foreground")
        n.add(self.backgroundOptions, text = "Background")
        n.add(self.windowOptions, text = "Window")
        n.bind("<ButtonRelease-1>", self.handleOpenTabLogic)
        n.grid()
        
        self.notebook = n
    
    # Handles a new tab click; tells the main window what box is open and 
    # gets defaults for each panel
    def handleOpenTabLogic(self, event):
        curTab = self.notebook.tab(self.notebook.select())
        if curTab['text'] == "Window":
            self.parent.windowOptionsOpen = True
            self.windowOptions.getWindowOptions()
        else:
            self.parent.windowOptionsOpen = False
            self.backgroundOptions.getDefaults()
            self.foregroundOptions.showOptions(event)
    
    # Handler for close button
    def close(self):
        self.parent.setOptions(False)
        self.top.destroy()
    
    # Used by clock to start drag mode in main clock window
    def beginDragMode(self):
        self.parent.beginDragMode()
