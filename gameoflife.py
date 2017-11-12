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

class Label(ttk.Label):
	def __init__(self, Master = None,**kw):
		super().__init__(Master, **kw)
		self.pack()

class MLabel(ttk.Label):
	def __init__(self, master=None, **kw):
		super().__init__(master, **kw)
		self.bind('<1>', self.save_mouse_location)
		self.bind("<B1-Motion>", self.move)
		self.xa , self.ya = 0, 0
		self.pack()


	def save_mouse_location(self,event):
		self.xa, self.ya = event.x ,event.y

	def move(self, event):
		x1, y1 = self.winfo_x() + event.x - self.xa , self.winfo_y() + event.y - self.ya
		self.place(x=x1 , y=y1 )
###########################################
# Pixels count = 100
# (HEIGHT * WIDTH) / 100 = (500 * 500)/ 100  = 250000/ 100 == 2500 pixles
# Pixels Width is 10
# Pixels Hight is 10
###########################################

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
