#Game Of life Made By Husam Dababneh
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import tkinter
from math import sin

WIDTH, HEIGHT = 650 , 650

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
		#self.bind('<1>', self.save_mouse_location)
		#self.bind("<B1-Motion>", self.move)
		#self.xa , self.ya = 0, 0
		self.pack()


	def save_mouse_location(self,event):
		self.xa, self.ya = event.x ,event.y

	def move(self, event):
		x1, y1 = self.winfo_x() + event.x - self.xa , self.winfo_y() + event.y - self.ya
		self.place(x=x1 , y=y1 )
###########################################
# Pixels count = 100
# (HEIGHT * WIDTH) / 100 = (500 * 500)/ 100  = 250000/ 100 == 2500 pixles
###########################################
class GridWindow(Canvas):
	def __init__(self, Master=None, **kw):
		super().__init__(Master , kw)
		self.bind('<Configure>', self.CreateGrid)
		#self.bind("<MouseWheel>",self.zoomer)

		#self.bind("<ButtonPress-1>", self.move_start)
		#self.bind("<B1-Motion>", self.move_move)

	def CreateGrid(self,event=None):
		
		w = self.winfo_width()# Get current width of canvas
		h = self.winfo_height() # Get current height of canvas
		#c.delete('grid_line')# Will only remove the grid_line
		
		for i in range(0, w, 10):
			self.create_line([(i, 0), (i, h)], fill="#999999" , tag='grid_line')

		for i in range(0, h, 10):
			self.create_line([(0, i), (w, i)],fill="#999999" , tag='grid_line')

	def zoomer(self,event):
		if (event.delta > 0):
			self.scale("all", event.x, event.y, 1.1, 1.1)
		elif (event.delta < 0):
			self.scale("all", event.x, event.y, 0.9, 0.9)
		self.configure(scrollregion = self.bbox("all"))

	def move_start(self, event):
		self.scan_mark(event.x, event.y)

	def move_move(self, event):
		self.scan_dragto(event.x, event.y, gain=1)

class MainFrame(ttk.Frame):
	def __init__(self, Master = None):
		super().__init__(Master)
		self.pack(expand=True, fill='both')
		#self.Label1 = MLabel(self, text="Game of life", justify="center")

		self.testCanvas = GridWindow(self, width=WIDTH , height=HEIGHT, bg="#7E7E7E")
		self.testCanvas.pack()

		self.Pixels = []
		self.x = 0
		self.y = 0




class GameFrame(ttk.Frame):
	def __init__(self, Master = None):
		super().__init__(Master)
	def move():
		pass #TODO : 


root = Root(None,"Game Of Life" , "650x650+75+75")
MainFrame1 = MainFrame(root)

root.mainloop()