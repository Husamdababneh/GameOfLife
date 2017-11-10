#Game Of life Made By Husam Dababneh
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import tkinter
from math import sin

WIDTH, HEIGHT = 650 , 650
DevidedBy = 10
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
class GridWindow(Canvas):
	def __init__(self, Master=None, **kw):
		super().__init__(Master , kw)
		self.bind('<Configure>', self.CreateGrid )
		self.bind("<MouseWheel>",self.zoomer)
		#self.bind("<ButtonPress-1>", self.move_start)
		self.bind("<ButtonPress-1>", lambda event: self.SetPixelColour(event,("#FFFFFF")))
		self.bind("<ButtonPress-3>",  lambda event: self.SetPixelColour(event,("#00FFFF")))
		
	#	self.bind("<Motion>", self.out)
		self.Pixels = {}
		self.PixelsState = {}
		self.pack()
		self.label = MLabel(Master ,text="Game of life", justify="right")

	def out(self,event = None):
		x , y = event.x, event.y
		string = ("(%s,%s)" % (x,y))
		print(string)

	def CreateGrid(self,event=None):
		
		w = self.winfo_width()# Get current width of canvas
		h = self.winfo_height() # Get current height of canvas
		#self.delete('grid_line')# Will only remove the grid_line
		
		for i in range(0, w, 10):
			self.create_line([(i, 0), (i, h)], fill="#000000" , tag='grid_line')

		for i in range(0, h, 10):
			self.create_line([(0, i), (w, i)],fill="#000000" , tag='grid_line')

	def GetPositionFormIndex(self, Index):
		x = Index % 65
		y = (Index-x) // 65
		return x , y

	def GetIndexFormPosition(self, x , y):
		return  x + y * 65

	def GetBestPixelPosition(self, Xcor, Ycor):
		if (Xcor % 10 != 0):
			Xcor = Xcor - (Xcor % 10)
		if (Ycor % 10 != 0):
			Ycor = Ycor - (Ycor % 10)
		return Xcor, Ycor
	def DeletePixelByIndexAndTag(self, index ,tag):
		self.delete()
		pass

	def SetPixelColour(self,event , Colour = "#FFFF00"):
		x , y = self.GetBestPixelPosition(event.x , event.y)
		index = self.GetIndexFormPosition(x//10 , y//10)
		_tag = "Live"
		if (index in self.PixelsState.keys()):
			self.DeletePixelByIndex(index , self.PixelsState.get(index , "Dead"))
			if (self.PixelsState.get(index) == "Live"):
				_tag = "Dead"
				Colour = "#7E7E7E"
			else:
				_tag = "Live"
				Colour = "#FFFFFF"
		
		self.create_rectangle(x , y, x + 10 , y + 10 , fill=Colour, tag={index : _tag}) 
		self.PixelsState[index] = _tag

		data = [x , y , x+10 , y+10]
		self.Pixels[index] = data

		x1 , y1 = self.GetPositionFormIndex(index)
		print(("Index[%s] : (%s,%s)" % (index ,x1 * 10 ,y1 * 10 )))
		
	def zoomer(self,event):
		print(str(self.gettags('Live')))

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
		

	




class GameFrame(ttk.Frame):
	def __init__(self, Master = None):
		super().__init__(Master)
	def move():
		pass #TODO : 


root = Root(None,"Game Of Life" , "651x690+75+75")
MainFrame1 = MainFrame(root)

root.mainloop()