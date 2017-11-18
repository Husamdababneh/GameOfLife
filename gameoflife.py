#Game Of life Made By Husam Dababneh
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

from classes import GridWindow

from  common import *

class Root(tkinter.Tk):
	def __init__(self, Master = None, Title = "Untitled", Size= "100x100", 
					Resizeable = False, **kw):
		super().__init__(Master, **kw)
		self.title(Title)
		self.geometry(Size)
		if (Resizeable == False):
			self.resizable(0,0)
			
class MainFrame(tkinter.Frame):
	def __init__(self, Master = None, **kw):
		super().__init__(Master, **kw)
		self.pack(expand = True, fill= "both")
		#self.Label1 = MLabel(self, text="Game of life", justify="center")
		
		self.SimulationWindow = GridWindow(self, width=WIDTH +1 , height=HEIGHT+1,
						highlightbackground ="#999999" , bg="#7E7E7E", bd=-2)#highlightbackground ="#999999"
		#self.button = Button(self,text="Test" , command=self.SimulationWindow.pr)
		#self.button.pack()



root = Root(None,"Game Of Life" , "690x690+75+75", False)
Game = MainFrame(root, bg="#D3D3D3")

root.mainloop()
