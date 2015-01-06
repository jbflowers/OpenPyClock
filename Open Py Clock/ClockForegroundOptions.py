import Tkinter as tk
import tkMessageBox
import ttk
import tkFont as tkFont
import tkColorChooser
from Tkinter import StringVar, IntVar

class ClockForegroundOptions(tk.Frame):
    def __init__(self, master, parent):
        tk.Frame.__init__(self, master)
        self.parent = parent
        self.grid()
        self.clock = master.clock
        clock = self.clock

        self.valXLabel = StringVar()
        self.valYLabel = StringVar()
        self.valFontLabel = StringVar()
        self.valFontSizeLabel = StringVar()
        self.valFontColourLabel = StringVar()

        self.xVar = StringVar()
        self.yVar = StringVar()
        self.fontVar = StringVar()
        self.fontSizeVar = StringVar()

        self._12HourFormatVar = IntVar()
        self.hourLeadingZeroesVar = IntVar()
        self.longMonthVar = IntVar()
        self.onVar = IntVar()
        
        self.symbolVar = StringVar()
        
        self.lastSymbolId = 0
        
        self.setSwitch = {"Hour": clock.setHour,
                          "Minute": clock.setMinute,
                          "Second": clock.setSecond,
                          "Year": clock.setYear,
                          "Month": clock.setMonth,
                          "Day Number": clock.setDayNumber,
                          "Day of Week": clock.setDayOfWeek,
                          "AM/PM": clock.setAMPM,
                          "Symbols": clock.setSymbol}
        self.getSwitch = {"Hour": clock.getHour,
                          "Minute": clock.getMinute,
                          "Second": clock.getSecond,
                          "Year": clock.getYear,
                          "Month": clock.getMonth,
                          "Day Number": clock.getDayNumber,
                          "Day of Week": clock.getDayOfWeek,
                          "AM/PM" : clock.getAMPM,
                          "Symbols" : clock.getSymbols}

        self.createWidgets()
        self.getDefaults("Hour")

    # Gets defaults for widgets based on label given and sets labels as necessary
    def getDefaults(self, label):
        defaults = self.getSwitch[label]()
        self.setDefaults(defaults, label)

    def setDefaults(self, defaults, label):
        
        if label == "Symbols":
            self.symbols = defaults
            self.symbolTextbox.delete('1.0', 'end')   
        else:
            self.xVar.set(defaults[0])
            self.yVar.set(defaults[1])
            self.fontVar.set(defaults[2])
            self.valFont.select_clear(0, "end")
            
            i = 0
            while (i < self.valFont.size()):
                if self.valFont.get(i).strip() == self.fontVar.get().strip():
                    t = self.valFont.get(i)
                    self.valFont.delete(i)
                    self.valFont.insert(0, t)
                    self.valFont.select_set(0)
                    i = 10000
                i+=1
    
            self.fontSizeVar.set(defaults[3])
            self.fontColourDefault = defaults[4]
            self.onVar.set(defaults[5])
    
            if (label == "Hour"):
                self._12HourFormatVar.set(defaults[5])
                self.hourLeadingZeroesVar.set(defaults[6])
                self.onVar.set(defaults[7])
            elif (label == "Month"):
                self.longMonthVar.set(defaults[5])
                self.onVar.set(defaults[6])
        
        self.setAllLabels(label)

    def setAllLabels(self, label):
        self.valXLabel.set(label + " X Coordinate")
        self.valYLabel.set(label + " Y Coordinate")
        self.valFontLabel.set(label + " Font")
        self.valFontSizeLabel.set(label + " Font Size")
        self.valFontColourLabel.set(label + " Font Colour")
        
        # Handle edge case items
        if (label != "Hour"):
            self.hourCheckButton.grid_forget()
            self.hourLeadingZeroes.grid_forget()
        else:
            self.hourCheckButton.grid(row = 0, column = 1, pady = 10, sticky = "NW")
            self.hourLeadingZeroes.grid(row = 0, column = 2, pady = 10, sticky = "NW")

        if (label != "Month"):
            self.monthCheckButton.grid_forget()
        else:
            self.monthCheckButton.grid(row = 0, column = 1, pady = 10, sticky = "NW")
        
        if (label != "Symbols"):
            self.symbolSelect.grid_forget()
            self.onCheckButton.grid(row = 1, column = 1, pady= 10, sticky="nw")
            try:
                self.symbolLabel.grid_forget()
                self.symbolTextbox.grid_forget()
                self.symbolDeleteButton.grid_forget()
            except:
                print("issues forgetting")
        else:
            symbols = list()
            for item in self.symbols:
                curSym = ("Symbol " + str(self.symbols[item]["idNum"]) + ' : "' 
                          + self.symbols[item]["sym"] + '"')
                symbols.append(curSym)
            symbols.append("New Symbol")
            

            self.symbolSelect.config(values = symbols)
            
            self.symbolVar.set(symbols[self.lastSymbolId])
                
            self.lastSymbolId = 0
            
            self.selectSymbol(None)
            
            self.onCheckButton.grid_forget()
            self.symbolSelect.grid(row = 0, column = 1, pady = 10, sticky = "NW")
        
        # Fix apply to all
        if (label == "Month" or label == "Year" or label == "Day of Week" or label == "Day Number"):
            self.applyToAll.config(text="Apply font, font size, and\ncolour to all date options",
                       command = self.applyToAllDate)
        elif (label == "Symbols"):
            self.applyToAll.config(text="Apply font, font size, and\ncolour to all symbols",
                       command = self.applyToAllSymbols)
        else:
            self.applyToAll.config(text="Apply font, font size, and\ncolour to all time options",
                       command = self.applyToAllTime)

    def createWidgets(self):

        fonts = tkFont.families(self.master)
        fonts = set(fonts)
        fonts = sorted(fonts)
        
        options = ["Hour", "Minute", "Second", "AM/PM", 
                   "Day of Week", "Month", "Day Number", "Year",
                   "Symbols"]

        self.currentOption = tk.Listbox(self, selectmode="SINGLE", exportselection=False)
        for option in options:
            self.currentOption.insert("end", option)
        self.currentOption.select_set(0)
        self.currentOption.bind("<ButtonRelease-1>", self.showOptions)
        self.currentOption.grid(row = 0, column = 0, rowspan = 10, pady = 10, sticky = "NW")
        

        # Hour checkbuttons
        self.hourCheckButton = tk.Checkbutton(self, text = "12 hour clock", variable = self._12HourFormatVar)
        self.hourCheckButton.grid(row = 0, column = 1, pady= 10, sticky = "NW")

        self.hourLeadingZeroes = tk.Checkbutton(self, text = "Leading zeroes", variable = self.hourLeadingZeroesVar)
        self.hourLeadingZeroes.grid(row = 0, column = 2, pady = 10, sticky = "NW")
        
        # Month checkbutton
        self.monthCheckButton = tk.Checkbutton(self, text = "Long month form",
                                              variable = self.longMonthVar)

        # Symbol stuff
        self.symbolSelect = ttk.Combobox(self, textvariable=self.symbolVar,
                                         state = "readonly")
        self.symbolSelect.bind("<<ComboboxSelected>>", self.selectSymbol)
        self.symbolLabel = tk.Label(self, text="Symbol: ")
        self.symbolTextbox = tk.Text(self, width = 24, height=1)
        self.symbolDeleteButton = tk.Button(self, text="Delete Symbol",
                                            command = self.removeSymbol)
        
        # On checkbutton
        self.onCheckButton = tk.Checkbutton(self, text = "Visible", variable = self.onVar)
        self.onCheckButton.grid(row = 1, column = 1, pady= 10, sticky = "NW")
        
        # val X
        tk.Label(self, text="Hour X", textvariable = self.valXLabel).grid(row=2, column = 1, pady = 5, sticky = "NW")
        maxX = self.master.winfo_screenwidth()
        maxY = self.master.winfo_screenheight()
        self.valX = tk.Spinbox(self, from_=0, to=maxX, textvariable = self.xVar)
        self.valX.grid(row=2, column = 2)

        # val Y
        tk.Label(self, textvariable = self.valYLabel).grid(row=3, column = 1, pady = 5, sticky = "NW")
        self.valY = tk.Spinbox(self, from_=0, to=maxY, textvariable = self.yVar)
        self.valY.grid(row=3, column = 2)

        # val font listbox
        scrollbar = tk.Scrollbar(self)
        tk.Label(self, textvariable = self.valFontLabel).grid(row=4, column = 1, pady = 5, sticky = "NW")
        self.valFont = tk.Listbox(self, selectmode = "SINGLE", exportselection = False, yscrollcommand = scrollbar.set)
        scrollbar.config(command = self.valFont.yview)
        scrollbar.grid(row=4, column = 2)
        self.valFont.grid(row=4, column = 2, pady = 5)
        for font in fonts:
            self.valFont.insert("end", font)

        # val font size
        tk.Label(self, textvariable = self.valFontSizeLabel).grid(row=5, column = 1, pady = 5, sticky = "NW")
        self.valFontSize = tk.Spinbox(self, from_=0, to=1000, textvariable = self.fontSizeVar)
        self.valFontSize.grid(row = 5, column = 2)

        # val font colour
        tk.Button(self, textvariable = self.valFontColourLabel, command = self.showColourPicker).grid(row = 6, column = 1, sticky = "NW")

        # Buttons
        tk.Button(self, text="Apply", command=self.apply).grid(row = 8, column = 2, sticky = "NE", pady=30)
        self.applyToAll = tk.Button(self, text="Apply font, font size, and\ncolour to all time options",
                       command = self.applyToAllTime)
        self.applyToAll.grid(row = 8, column = 1, stick = "NW", pady=30)
        tk.Button(self, text="Drag and drop mode", command=self.beginDragMode).grid(row=8, column=0, sticky="NW", pady=30)

    # Applys current options
    def apply(self):
        f = self.valFont.get(self.valFont.curselection())
        o = self.currentOption.get(self.currentOption.curselection())

        try:
            int(self.valX.get())
            int(self.valY.get())
            int(self.valFontSize.get())
            if (o.strip() == "Month"):
                self.setSwitch[o](self.valX.get(), self.valY.get(), f,
                                  self.valFontSize.get(), self.fontColourDefault,
                                  self.longMonthVar.get(), self.onVar.get())
    
            elif o.strip() == "Hour":
                self.setSwitch[o](self.valX.get(), self.valY.get(), f,
                                  self.valFontSize.get(), self.fontColourDefault,
                                  self._12HourFormatVar.get(),
                                  self.hourLeadingZeroesVar.get(),
                                  self.onVar.get())
    
            elif o.strip() == "Symbols":
                if self.symbolSelect.get() == "New Symbol":
                    idNum = len(self.symbols)
                    sym = self.symbolTextbox.get('1.0', 'end')
                    sym = sym[:-1]
                    if len(sym.strip()) == 0:
                        raise Exception
                else:
                    t = self.symbolSelect.get()
                    idNum = int(t.split(" ")[1])
                    sym = self.symbols[idNum]["sym"]
                self.setSwitch[o](self.valX.get(), self.valY.get(), f,
                                  self.valFontSize.get(), self.fontColourDefault,
                                  idNum, sym, self.onVar.get())
                self.lastSymbolId = idNum
                
            else :
                self.setSwitch[o](self.valX.get(), self.valY.get(), f,
                                  self.valFontSize.get(), self.fontColourDefault, self.onVar.get())
            self.clock.saveClockOptions()
        
        except:
            tkMessageBox.showerror("Invalid input", "A value entered was not valid",
                                   parent = self)
        
        self.getDefaults(o.strip())

    # Applies current settings to all time options
    def applyToAllTime(self):
        f = self.valFont.get(self.valFont.curselection())
        
        self.clock.setHour(self.clock.hourX, self.clock.hourY, f,
                  self.valFontSize.get(), self.fontColourDefault,
                  self._12HourFormatVar.get(), self.hourLeadingZeroesVar.get(), 
                  self.onVar.get())
        self.clock.setMinute(self.clock.minuteX, self.clock.minuteY, f,
                             self.valFontSize.get(), self.fontColourDefault,
                             self.onVar.get())
        self.clock.setSecond(self.clock.secondX, self.clock.secondY, f,
                             self.valFontSize.get(), self.fontColourDefault,
                             self.onVar.get())
        
        self.clock.setAMPM(self.clock.ampmX, self.clock.ampmY, f,
                           self.valFontSize.get(), self.fontColourDefault,
                           self.onVar.get())
        
        self.clock.saveClockOptions()
            
    # Applies current settings to all date options
    def applyToAllDate(self):
        f = self.valFont.get(self.valFont.curselection())
        
        self.clock.setYear(self.clock.yearX, self.clock.yearY, f,
                  self.valFontSize.get(), self.fontColourDefault, self.onVar.get())
        
        self.clock.setMonth(self.clock.monthX, self.clock.monthY, f,
                  self.valFontSize.get(), self.fontColourDefault,
                  self.longMonthVar.get(), self.onVar.get())
        
        self.clock.setDayNumber(self.clock.dayNumberX, self.clock.dayNumberY, f,
                  self.valFontSize.get(), self.fontColourDefault, self.onVar.get())

        self.clock.setDayOfWeek(self.clock.dayOfWeekX, self.clock.dayOfWeekY, f,
                  self.valFontSize.get(), self.fontColourDefault, self.onVar.get())
        
        self.clock.saveClockOptions()
    
    # Applies current settings to all symbols
    def applyToAllSymbols(self):
        f = self.valFont.get(self.valFont.curselection())
        for item in self.symbols:
            cur = self.symbols[item]
            self.setSwitch["Symbols"](cur['x'], cur['y'], f,
                  self.valFontSize.get(), self.fontColourDefault,
                  cur["idNum"], cur["sym"], 1)
    
    # Handler for drag and drop placement mode button
    def beginDragMode(self):
        self.parent.beginDragMode()

    # Handler to close windwo
    def close(self):
        self.parent.close()

    # Event handler for click on select list of time options
    def showOptions(self, position):
        o = self.currentOption.get(self.currentOption.curselection())
        self.getDefaults(o)

    # Event handler for click on select list of all symbols
    def selectSymbol(self, event):
        s = self.symbolSelect.get()
        if (s == "New Symbol"):
            self.prepareForNewSymbol()
            return
        try:
            self.symbolLabel.grid_forget()
            self.symbolTextbox.grid_forget()
        except:
            None
        self.clock.saveClockOptions()
        self.symbolDeleteButton.grid(row = 0, column = 2)
        idNum = s.split(" ")
        idNum = int(idNum[1])
        
        curSym = self.symbols[idNum]

        self.xVar.set(curSym["x"])
        self.yVar.set(curSym["y"])
        self.fontVar.set(curSym["font"])
        self.fontSizeVar.set(curSym["size"])
        self.fontColourDefault = curSym["colour"]
        self.onVar.set(curSym["on"])
        
        self.valFont.select_clear(0, "end")
        i = 0
        while (i < self.valFont.size()):
            if self.valFont.get(i).strip() == self.fontVar.get().strip():
                t = self.valFont.get(i)
                self.valFont.delete(i)
                self.valFont.insert(0, t)
                self.valFont.select_set(0)
                i = 10000
            i+=1

    # Prepares window to show options for new symbol
    def prepareForNewSymbol(self):
        self.xVar.set(0)
        self.yVar.set(0)
        self.fontVar.set("")
        self.fontSizeVar.set(12)
        self.fontColourDefault = "#000000"
        self.onVar.set(1)
        
        self.valFont.select_clear(0, "end")
        self.valFont.select_set(0)
        
        
        self.symbolLabel.grid(row=1, column =1, sticky = "nw")
        
        self.symbolTextbox.grid(row = 1, column = 2, sticky="nw")
        
        print("Grid forget at 388")
        self.symbolDeleteButton.grid_forget()
        
    # Handler for delete symbol button
    def removeSymbol(self):
        idNum = int(self.symbolSelect.get().split(" ")[1])
        self.clock.removeSymbol(idNum)
        self.clock.saveClockOptions()
        self.getDefaults("Symbols")
        
    # Handler for font colour button    
    def showColourPicker(self):
        colours = tkColorChooser.askcolor(parent = self, color = self.fontColourDefault)
        if colours[1] != None:
            self.fontColourDefault = colours[1]
