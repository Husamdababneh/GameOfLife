import math
import os
import tkinter
from tkinter import Canvas, ttk

from common import *


'''
Allowed game space from (2,2) -> (652, 652) because of the frame borders 

'''
class Grid(Canvas):
	def __init__(self, Master = None , CellSize = 10 , **kw):
		super().__init__(Master, **kw)
		self.bind("<1>", self.SetPixelColour)
		self.pack(expand=True)
		self.update()

		#################### 
		#some important constants
		self.CellSize = CellSize
		self.bd = int(self.cget("bd")) + 2 
		self.CellCount = self.winfo_width() *  self.winfo_height() // (self.CellSize**2)
		self.widthCells = int(math.sqrt(self.CellCount)) #assumming that the world id square 
		print("CellCount {}".format(self.CellCount))		
		self.width = self.winfo_width() - (self.bd * 2)
		self.height = self.winfo_height() - (self.bd * 2)
		########################
		self.AliveCells = {} # {index : id}
		self.Create_Grid(CellSize)
		self.randomcells()

	def randomcells(self):
		pass
	def GetBestPixelPosition(self, Xcor, Ycor):
		Xcor = Xcor - (Xcor % self.CellSize) 
		Ycor = Ycor - (Ycor % self.CellSize) 
		if Xcor >= self.width: Xcor = self.width - self.CellSize
		if Ycor >= self.width: Ycor  = self.width - self.CellSize
		#print("{}...{}".format(Xcor ,Ycor ))
		return Xcor , Ycor 

	def GetPositionFormIndex(self, Index):
		x = (Index % int(math.sqrt(self.CellCount)))
		y = (Index-x) // (self.width // self.CellSize)
		return x  * 10, y  * 10

	def GetIndexFormPosition(self, x , y):
		return  x // 10 + (y//10 * (self.width // self.CellSize))
	
	def GetPositionFromId(self,Id):
		for index , cellId in (self.AliveCells.items()):
			if Id == cellId:
				return (self.GetPositionFormIndex(index))
	
	def Create_Grid(self,CellSize):
		bd = self.bd
		n_width = self.width 
		n_height = self.height

		for i in range(0, n_width , CellSize):
			self.create_line([(i + bd ,0), (i + bd , n_height + 1)] , fill="#999999" , tag='grid_line')#"#999999" 

		for i in range(0, n_height  , CellSize):
			self.create_line([(0, i + bd), (n_width+1, i + bd)] , fill="#999999" , tag='grid_line')

		print("{}...{}...{}".format(n_width,n_height, bd))
	
	def SetPixelColour(self ,event , Colour = "#FFFF00" , size = 10):
		#print("--------------" + str(type(event)))
		x , y = self.GetBestPixelPosition(event.x -2 , event.y-2)
		bd = self.bd 
		bbox =  x + bd + 1  , y + bd + 1 , x +  self.CellSize + bd  , y +  self.CellSize + bd
		index = self.GetIndexFormPosition(x,y)
		if index in self.AliveCells:
			self.delete(self.AliveCells[index])	
			del self.AliveCells[index]
			return
		id = self.create_rectangle(bbox, fill=Colour, outline = "#999999" , tag="Live",width = 0) 
		self.AliveCells[index] = id

	def testcreator(self, index):
		event = tkinter.Event()
		event.x ,event.y = self.GetPositionFormIndex(index)
		event.x += 2 
		event.y +=2
		self.SetPixelColour(event)

	def GetNeighboursCount(self,  index):
		neighbours = [ index - self.widthCells - 1 , index - self.widthCells , index - self.widthCells +1,
				index -1 , index + 1,
				index + self.widthCells -1 , index + self.widthCells ,  index + self.widthCells +1
			]
		count = 0 
		for neighbour in  neighbours:
			if  neighbour in self.AliveCells.keys():
				count +=1
		#print(count)
		return count
		
#############################
# #Rules
# 1 Overpopulation: if a living cell is surrounded by more than three living cells, it dies.
# 2 Stasis: if a living cell is surrounded by two or three living cells, it survives.
# 3 Underpopulation: if a living cell is surrounded by fewer than two living cells, it dies.
# 4 Reproduction: if a dead cell is surrounded by exactly three cells, it becomes a live cell.
##############################
	def TestGeneration(self):
		os.system("cls")
		for index in range(0, self.CellCount,1):
			NeighboursCount =  self.GetNeighboursCount(index)		

			if (NeighboursCount > 3 or NeighboursCount < 2) and (index in self.AliveCells.keys()) : #rule 1 & 2 & 3
				self.delete(self.AliveCells[index])

			if (NeighboursCount == 3 and (index not in self.AliveCells.keys())) :#dead cell with 3 neighbours #rule 4
				 self.testcreator(index)

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
		

		#self.test()

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
		Xcor = Xcor - (Xcor % 10) 
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

	def GetIndexFromId(self, Id):
		for item in self.PixelsId.items():
			key , value = item[0] , item[1]
			if value == Id:
				return key
		return -1
	
		#for item in self.PixelsId.items():
			#print("Item " + str(item))
	def GetNeighbours(self,Id):
		'''
		first , second , third neighbours = index - 65 -1 , index - 65  , index - 65 +1
		fourth ,fifth  		   neighbours = index  -1 ,  index + 1
		sixth , seventh , eighth neighbours = index + 65 -1 , index + 65  , index + 65 +1
		'''
		index = self.GetIndexFromId(Id)
		if index == -1:
			return
		x, y = self.GetPositionFormIndex(index)
		Neighbours = [index - 65 -1 , index - 65  , index - 65 +1 ,
					index  -1 ,  index + 1,
						index + 65 -1 , index + 65  , index + 65 +1]
		for NeighbourIndex in Neighbours:
			if NeighbourIndex in self.PixelsState and self.PixelsState[NeighbourIndex] == "Live":
				print(str(NeighbourIndex) + " is Live")
		#print("(%s,%s)" % (x, y))

	def TestGeneration(self):
		a = self.find_withtag("Live")
		for x in a:
			Neighbours = self.GetNeighbours(x)
			#print(a)

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
