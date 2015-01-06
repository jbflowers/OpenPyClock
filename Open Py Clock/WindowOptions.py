import Tkinter as tk
import os
from Tkinter import StringVar, IntVar
import ttk
import tkMessageBox

class WindowOptions(tk.Frame):
    def __init__(self, master, parent):
        tk.Frame.__init__(self, master)
        self.grid()
        
        self.xVar = StringVar()
        self.yVar = StringVar()
        self.fullscreenVar = IntVar()
        
        self.getWindowOptions()
        
        self.createWidgets()   
        
    def createWidgets(self):
        maxX = self.winfo_screenwidth()
        maxY = self.winfo_screenheight()
        
        textLabel = tk.Label(self, text="Resize the clock window to dynamically change values below.")
        
        textLabel.grid(row = 0, column = 0, sticky="NW", pady = 5)
        
        xlabel = tk.Label(self, text = "Default Window Width")
        xlabel.grid(row = 1, column = 0, sticky = "NW", pady = 5)
        self.valX = tk.Spinbox(self, from_ =0, to=maxX,
                               textvariable = self.xVar)
        self.valX.grid(row = 1, column = 1)
        
        ylabel = tk.Label(self, text = "Default Window Height")
        ylabel.grid(row = 2, column = 0, sticky = "NW", pady = 5)
        self.valY = tk.Spinbox(self, from_ =0, to=maxY,
                               textvariable = self.yVar)
        self.valY.grid(row = 2, column = 1)
        
        self.fullscreenCheckbutton = ttk.Checkbutton(self, text = "Fullscreen on start",
                                              variable = self.fullscreenVar)
        
        self.fullscreenCheckbutton.grid(row = 3, column = 0, sticky = "NW", pady = 5)
    
        tk.Button(self, text="Apply", command = self.apply).grid(row = 4, column = 0,
                                                           sticky = "NW", pady = 5)

    def apply(self):
        try:
            self.windowX = int(self.xVar.get())
            self.windowY = int(self.yVar.get())
            self.fullscreenOnStart = self.fullscreenVar.get()
            self.saveWindowOptions()
        except ValueError:
            tkMessageBox.showerror("Invalid input", "A value entered was not valid",
                       parent = self)

    def getWindowOptions(self):
        if os.path.exists("prefs/window_prefs.dat"):
            f = open('prefs/window_prefs.dat', 'r')
        else:
            return
        self.windowX = int(f.readline())
        self.windowY = int(f.readline())
        self.fullscreenOnStart = int(f.readline())
        
        self.xVar.set(self.windowX)
        self.yVar.set(self.windowY)
        self.fullscreenVar.set(self.fullscreenOnStart)
        
    def saveWindowOptions(self):
        
        f = open('prefs/window_prefs.dat', 'w+')
        
        f.write(str(self.windowX) + "\n")
        f.write(str(self.windowY) + "\n")
        f.write(str(self.fullscreenOnStart) + "\n")
        