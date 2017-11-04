#Game Of life Made By Husam Dababneh
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import tkinter
from math import sin

WIDTH, HEIGHT = (500 + (500 //50)) , (500 + (500 //50))

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

class MainFrame(ttk.Frame):
	def __init__(self, Master = None):
		super().__init__(Master)
		self.pack(expand=True, fill='both')
		self.Label1 = MLabel(self, text="Game of life", justify="center")
		self.testCanvas = Canvas(self, width=WIDTH, height=HEIGHT, bg="#FFFFFF")
		self.testCanvas.pack()
		self.img = PhotoImage(width=WIDTH, height=HEIGHT)
		self.testCanvas.create_image((WIDTH/2, HEIGHT/2), image=self.img, state="normal")
		self.Pixels = []
		self.x = 0
		self.y = 0
		self.CreateGrid()
		#self.FillPixel(10 ,10)

	def CreateGrid(self):
		for x in range(WIDTH//50):
			for y in range(HEIGHT//50):
				self.img.put("#000000", (x , y+10))

	def FillPixel(self, inX , inY):
		for x in range(WIDTH//50):
			for y in range(HEIGHT//50):
				self.img.put("#000000", (inX+ x, inY +y))

class GameFrame(ttk.Frame):
	def __init__(self, Master = None):
		super().__init__(Master)
	def move():
		pass #TODO : 


root = Root(None,"Game Of Life" , "650x650+75+75")
MainFrame1 = MainFrame(root)

root.mainloop()
