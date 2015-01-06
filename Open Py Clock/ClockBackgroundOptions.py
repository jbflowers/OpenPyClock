import Tkinter as tk
import tkMessageBox
import tkColorChooser
from Tkinter import StringVar, IntVar
from tkFileDialog import askopenfilename

class ClockBackgroundOptions(tk.Frame):
    def __init__(self, master, parent):
        tk.Frame.__init__(self, master)
        self.clock = master.clock
        self.grid()
        
        self.backgroundColour = "#ffffff"
        self.backgroundImageX = StringVar()
        self.backgroundImageY = StringVar()
        self.backgroundImageScaleX = StringVar()
        self.backgroundImageScaleY = StringVar()
        self.constrain = IntVar()
        self.tilesBackground = IntVar()
        self.imageLocation = ""
        
        self.getDefaults()
        self.createWidgets()
        
    # Gets and sets default values for widgets
    def getDefaults(self):
        defaults = self.clock.getBackgroundInformation()
        self.backgroundColour = defaults[0]
        self.imageLocation = defaults[1]
        self.backgroundImageX.set(defaults[2])
        self.backgroundImageY.set(defaults[3])
        self.backgroundImageScaleX.set(defaults[4])
        self.backgroundImageScaleY.set(defaults[5])
        self.tilesBackground.set(defaults[6])   
        
    def createWidgets(self):
        colourButton = tk.Button(self, text = "Set background colour",
                                 command = self.getColour)
        colourButton.grid(row = 0, column = 0, sticky = "NW", pady = 10)
        
        imageButton = tk.Button(self, text = "Set image as background",
                                command = self.setBackgroundImgae)
        imageButton.grid(row = 1, column = 0, sticky = "NW", pady = 5)
        
        maxX = self.winfo_screenwidth()
        maxY = self.winfo_screenheight()
        
        xlabel = tk.Label(self, text = "Background Image X Coordinate")
        xlabel.grid(row = 2, column = 0, sticky = "NW", pady = 5)
        self.valX = tk.Spinbox(self, from_ =0, to=maxX,
                               textvariable = self.backgroundImageX)
        self.valX.grid(row = 2, column = 1)
        
        ylabel = tk.Label(self, text = "Background Image Y Coordinate")
        ylabel.grid(row = 3, column = 0, sticky = "NW", pady = 5)
        self.valY = tk.Spinbox(self, from_=0, to=maxY,
                               textvariable = self.backgroundImageY)
        self.valY.grid(row = 3, column = 1)
        
        xlabel = tk.Label(self, text = "Background Image X Scale %")
        xlabel.grid(row = 4, column = 0, sticky = "NW", pady = 5 )
        self.valScaleX = tk.Spinbox(self, from_=0, to=10000, 
                                    textvariable=self.backgroundImageScaleX)
        self.valScaleX.grid(row = 4, column = 1)
        
        ylabel = tk.Label(self, text = "Background Image Y Scale %")
        ylabel.grid(row = 5, column = 0, sticky = "NW")
        self.valScaleY = tk.Spinbox(self, from_=0, to=10000, 
                                    textvariable = self.backgroundImageScaleY)
        self.valScaleY.grid(row = 5, column = 1)
        
        self.constrainScaling = tk.Checkbutton(self, text = "Equal scaling",
                                              variable = self.constrain,
                                              command = self.constrainHandler)
        self.constrainScaling.grid(row = 4, column = 2, sticky = "NW")
        
        self.valTiles = tk.Checkbutton(self, text="Tile",
                       variable = self.tilesBackground,
                       command = self.tileBackground)
        
        self.valTiles.grid(row = 6, column = 0, sticky = "NW", pady = 5 )    
        
        self.clearImage = tk.Button(self, text= "Clear background image",
                                    command = self.clearBgImage)
        self.clearImage.grid(row = 7, column = 0, sticky = "NW", pady = 5 )
        
        self.applyButton = tk.Button(self, text= "Apply", command = self.apply)
        self.applyButton.grid(row = 8, column = 0, sticky = "NW", pady = 5 )
        
        if (self.imageLocation == ""):
            self.valX.config(state="disabled")
            self.valY.config(state="disabled")
            self.valScaleX.config(state="disabled")
            self.valScaleY.config(state="disabled")
            self.valTiles.config(state="disabled")
            self.clearImage.config(state= "disabled")
            self.applyButton.config(state="disabled")
            self.constrainScaling.config(state="disabled")
        
        if self.backgroundImageScaleX.get() == self.backgroundImageScaleY.get():
            self.constrain.set(1)
            self.valScaleY.config(state = "disabled")
    
    
    # Handler for clear background button
    def clearBgImage(self):
        self.clock.setBackgroundImage(self.backgroundImageX.get(), 
                              self.backgroundImageY.get(),
                              self.backgroundImageScaleX.get(),
                              self.backgroundImageScaleY.get(), 
                              "none")
        self.valX.config(state="disabled")
        self.valY.config(state="disabled")
        self.valScaleX.config(state="disabled")
        self.valScaleY.config(state="disabled")
        self.valTiles.config(state="disabled")
        self.clearImage.config(state= "disabled")
        self.applyButton.config(state="disabled")
        self.constrainScaling.config(state="disabled")
        self.clock.saveClockOptions()
    
    # Handler for tiling checkbutton
    def tileBackground(self):
        self.clock.setBackgroundTiling(self.tilesBackground.get())
    
    # Handler for set image background button
    def setBackgroundImgae(self):
        types = (("Joint Photographic Experts Group", "*.jpeg"),
                 ("Joint Photographic Experts Group", "*.jpg"),
                 ("Portable Networks Graphics", "*.png"),
                 ("Graphics Interchange Format", "*.gif"),
                 ("Bitmap", "*.bmp") );
        
        location = askopenfilename(parent=self,
                                   filetypes = types )
        
        if location != () and location != "":
            self.valX.config(state="normal")
            self.valY.config(state="normal")
            self.valScaleX.config(state="normal")
            self.valTiles.config(state="normal")
            self.clearImage.config(state="normal")
            self.applyButton.config(state="normal")
            self.constrainScaling.config(state = "normal")
            self.imageLocation = location
            self.clock.setBackgroundImage(self.backgroundImageX.get(), 
                                          self.backgroundImageY.get(),
                                          self.backgroundImageScaleX.get(),
                                          self.backgroundImageScaleY.get(), 
                                          location)
            self.clock.saveClockOptions()

    # Handler for apply button
    def apply(self):
        try:
            int(self.valX.get())
            int(self.valY.get())
            int(self.valScaleX.get())
            int(self.valScaleY.get())
            if self.constrain.get() == 1:
                self.backgroundImageScaleY.set(self.backgroundImageScaleX.get())
                
            self.clock.setBackgroundImage(self.valX.get(), 
                              self.valY.get(),
                              self.backgroundImageScaleX.get(),
                              self.backgroundImageScaleY.get(), 
                              "same")
            self.clock.saveClockOptions()
        except ValueError:
            tkMessageBox.showerror("Invalid input", "A value entered was not valid",
                       parent = self)
        except IOError:
            tkMessageBox.showerror("Background Image Not Found", "The background image supplied was not found.",
                       parent = self)
    
    # Handler for select background colour button 
    def getColour(self):
        colours = tkColorChooser.askcolor(parent = self, color = self.backgroundColour)
        if colours[1] != None:
            self.clock.setBackgroundColour(colours[1])
            self.backgroundColour = colours[1]
            self.clock.saveClockOptions()
    
    # Handler for made x y scaling equal checkbutton
    def constrainHandler(self):
        if self.constrain.get() == 1 :
            self.valScaleY.config(state="disabled")
        else:
            self.valScaleY.config(state="normal")
