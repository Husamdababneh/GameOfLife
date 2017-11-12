#Game Of life Made By Husam Dababneh
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

from classes import GridWindow

from  common import *

class Root(tkinter.Tk):
	def __init__(self, Master = None, Title = "Untitled", Size= "100x100", 
					Resizeable = False):
		super().__init__(Master)
		self.title(Title)
		self.geometry(Size)
		if (Resizeable == False):
			self.resizable(0,0)
			
class MainFrame(ttk.Frame):
	def __init__(self, Master = None):
		super().__init__(Master)
		self.pack(expand=True, fill='both')
		#self.Label1 = MLabel(self, text="Game of life", justify="center")
		
		self.SimulationWindow = GridWindow(self, width=WIDTH , height=HEIGHT, bg="#7E7E7E")
		self.button = Button(self,text="Test" , command=self.SimulationWindow.pr)
		self.button.pack()



root = Root(None,"Game Of Life" , "690x690+75+75", True)
Game = MainFrame(root)

root.mainloop()
