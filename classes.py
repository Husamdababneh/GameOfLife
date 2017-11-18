import tkinter
from tkinter import Canvas, ttk

from common import *

'''
Allowed game space from (2,2) -> (652, 652) because of the frame borders 

'''


class GridWindow(Canvas):
	def __init__(self, Master=None, **kw):
		super().__init__(Master , **kw)
		self.bind("<MouseWheel>",self.zoomer)
		self.bind("<ButtonPress-1>" ,self.SetPixelColour)
		# Test Purpos
		self.bind('<3>', self.save_mouse_location)
		self.bind("<B3-Motion>", self.MoveCanvas)
	
	#	self.bind("<Motion>", self.out)
		self.PixelsId = {}
		self.PixelsState = {}
		
		self.pack(expand=True)
		self.update()
		#self.FixSize()
		

		self.test()

		print("(%s,%s)" % (self.winfo_height(), self.winfo_width()))
		
		self.CreateGrid()
		#self.label = MLabel(Master ,text="Game of life", justify="right")
	def FixSize(self):
		self.configure(width = (self.winfo_width() -(self.winfo_width() % 10) ) )

	def save_mouse_location(self,event):
		self.xa, self.ya = event.x ,event.y
		height = self.winfo_height()
		width = self.winfo_width() 
		#1,685
		print("(%s,%s)" % (height, width))

	def test(self):
		index = 4224
		x1 , y1 = self.GetPositionFormIndex(index)
		bbox = x1 , y1, x1 + 10 , y1 + 10
		bbox2 =  0 ,0 ,10,10
		#id = self.create_rectangle(bbox2, fill="red", tag="Live") 
		#id = self.create_rectangle(bbox, fill="red", tag="Live") 
		#print(("Id[%s] Index[%s] : (%s,%s)" % (id ,index ,x1  ,y1  )))

	def MoveCanvas(self, event):
		x1, y1 = self.winfo_x() + event.x - self.xa , self.winfo_y() + event.y - self.ya
		self.place(x=x1 , y=y1 )

	def out(self,event = None):
		x , y = event.x, event.y
		string = ("(%s,%s)" % (x,y))
		print(string)

	def CreateGrid(self, event=None , _DevidedBy = 10):
		height = self.winfo_height()
		width = self.winfo_width() 

		w = int(self.cget("width"))
		h = int(self.cget("height"))

		#w = height - 2 * int(self.cget("bd"))
		#h = width - 2 * int(self.cget("bd"))

		#self.delete('grid_line')# Will only remove the grid_line
		#for i in range(0, 652, 10):
			#a = [(i, 0), (i , 652)]
			#self.create_line(a, fill="#999999", tag="grid_line")
		for i in range(0, 651, _DevidedBy):
			self.create_line([(i, 0), (i, 650)], fill="#999999" , tag='grid_line')
			
		for i in range(0, 651, _DevidedBy):
			self.create_line([(0, i), (650, i)],fill="#999999" , tag='grid_line')
	
	def GetPositionFormIndex(self, Index):
		x = (Index % 65)
		y = (Index-x) // 65
		return x  * 10, y  * 10

	def GetIndexFormPosition(self, x , y):
		return  x + y * 65

	def GetBestPixelPosition(self, Xcor, Ycor):
		if (Xcor % 10 != 0):
			Xcor = Xcor - (Xcor % 10) 
		if (Ycor % 10 != 0):
			Ycor = Ycor - (Ycor % 10) 
		return Xcor + 1, Ycor + 1

	def DeletePixelById(self, id ):
		self.delete(self.PixelsId[id])
		pass

	def SetPixelColour(self,event , Colour = "#FFFF00" , size = 10):
		x , y = self.GetBestPixelPosition(event.x , event.y)
		if x >= 650 or y >= 650:
			return
		index = self.GetIndexFormPosition(x//10 , y//10)

		if (index in self.PixelsState.keys()):
			if (self.PixelsState.get(index) == "Live"):
				self.DeletePixelById(index)
				self.PixelsState[index] = "Dead"
				return

		bbox = x  , y, x + size - 1  , y + size - 1
		id = self.create_rectangle(bbox, fill=Colour, outline = "#999999" , tag="Live",width = 0) 

		self.PixelsState[index] = "Live"
		self.PixelsId[index] = id
		x1 , y1 = self.GetPositionFormIndex(index)
		print(("Id[%s] Index[%s] : (%s,%s)" % (id ,index ,x1 ,y1  )))
		
	def zoomer(self,event):
		pass
	def move_start(self, event):
		self.scan_mark(event.x, event.y)

	def move_move(self, event):
		self.scan_dragto(event.x, event.y, gain=1)
	def pr(self):
		print("Call BAck")

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



















		#print(self.gettags(CURRENT))
		#print(self.find_withtag("Live"))
		#a= self.find_withtag("Live")
		#if(1<= len(a)):
		#	for x in range(len(a)):
		#		self.delete(a[x])
		#test = self.gettags(ALL)

		#self.delete("Live")
		#self.delete("Dead")
