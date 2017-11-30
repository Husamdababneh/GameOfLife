#Game Of life Made By Husam Dababneh
import math
import os
import random
import time
import tkinter
from tkinter import *
from tkinter import Canvas, ttk
from tkinter.ttk import *



WIDTH, HEIGHT = 650  , 650
DevidedBy = 10
WIDTH2 , HEIGHT2 = WIDTH//DevidedBy , HEIGHT//DevidedBy
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
		
		self.SimulationWindow = Grid(self, 10,width=WIDTH +1 , height=HEIGHT+1,
							highlightbackground ="#999999" , bg="#7E7E7E")#highlightbackground ="#999999"
		self.button = Button(self,text="Test" , command=self.genatare)#command=self.SimulationWindow.TestGeneration)
		self.button.pack()
		
	def genatare(self):
		self.SimulationWindow.TestGeneration()
		

		
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
		self.Cells = [] 
		self.Create_Grid(CellSize)
		#self.randomcells()

	def randomcells(self):
		for x in range(4000):
			self.testcreator(random.randint(0 , self.CellCount ))

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
		#os.system("cls")
		to_delete = []
		to_create = []
		for index in range(0, self.CellCount,1):
			NeighboursCount =  self.GetNeighboursCount(index)		

			if (NeighboursCount > 3 or NeighboursCount < 2) and (index in self.AliveCells.keys()) : #rule 1 & 2 & 3
				to_delete.append(index)
				#self.delete(self.AliveCells[index])

			if (NeighboursCount == 3 and (index not in self.AliveCells.keys())) :#dead cell with 3 neighbours #rule 4
				to_create.append(index)
				#self.testcreator(index)
		for index in to_delete:
			self.delete(self.AliveCells[index])
			del self.AliveCells[index]

		for index in to_create:
			self.testcreator(index)
		return

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


root = Root(None,"Game Of Life" , "690x690+75+75", False)
Game = MainFrame(root, bg="#D3D3D3")

root.mainloop()
