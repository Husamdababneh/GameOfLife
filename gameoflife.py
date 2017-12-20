#Game Of life Made By Husam Dababneh
import math
import matplotlib.pyplot as plt
import os
import random
import time
import tkinter
from tkinter import *
from tkinter import Canvas, ttk
from tkinter.ttk import *

WIDTH, HEIGHT = 650  , 650
CellCounter = []
GenCounter = []

class Root(tkinter.Tk):
	def __init__(self, Master = None, Title = "Untitled", Size= "100x100",	Resizeable = False, **kw):
		super().__init__(Master, **kw)
		self.title(Title)
		self.geometry(Size)
		if (Resizeable == False):
			self.resizable(0,0)


class MainFrame(tkinter.Frame):
	def __init__(self, Master = None, **kw):
		super().__init__(Master, **kw)
		self.pack(expand = True, fill= "both")

		style = ttk.Style()
		style.configure("TScale", background='#D3D3D3')
		style.configure("TButton", background='#D3D3D3')


		self.life = 0 #0 stop ---- 1 start
		self.SimulationWindow = GameOfLife(self, 10,width=WIDTH +1 , height=HEIGHT+1,highlightbackground ="#999999" , bg="#7E7E7E")

#		buttonstyle = ttk.Style()
#		buttonstyle.configure
		self.button = Button(self,text="Start" ,command=self.Generate)
		#self.button.grid()
		self.button.pack(side= "left")

		self.button1 = Button(self,text="Clear" , command=self.ClearTheWorld)
		self.button1.pack(side = "left", padx= 5)

		self.plotButton = Button(self, text="Plot Result", command = self.PlotTheResult)
		self.plotButton.pack(side = "right")

		self.var = IntVar(self , 0)
		self.Generations = IntVar(self , 0)
		self.Generations.trace('w',self.Update)
		self.String = StringVar(self,"Gen = 0")
		
		self.T = ttk.Scale(self, style="TScale" ,from_ = 0  ,to= 1000#, variable = self.var)
		,command=lambda value : self.var.set(int(float(value))))
		self.T.pack(side = "left")

		self.MS = 988
		self.ScaleLabel = Label(self,textvariable=self.var, background='#D3D3D3')
		self.ScaleLabel.pack(side= "left",padx=20)

		self.GenerationLabel = Label(self, textvariable= self.String,background='#D3D3D3')
		self.GenerationLabel.pack(side= "left",)

		
		self.String2 = StringVar(self,"Count = " +str(self.SimulationWindow.GetCellCount()))
		self.CountLabel = Label(self, textvariable=self.String2 ,background='#D3D3D3')
		self.CountLabel.pack(side= "left" )
		
	def Update(self,*args):
		global GenCounter , CellCounter
		self.String.set("Gen ="+ str(self.Generations.get()))
		self.String2.set("Count =" + str(self.SimulationWindow.GetCellCount()))
		GenCounter.append(int(self.Generations.get()))
		CellCounter.append(int(self.SimulationWindow.GetCellCount()))

	def PlotTheResult(self):
		plt.plot(CellCounter,GenCounter)
		plt.xlabel('Generation')
		plt.ylabel('Cell Count')
		plt.show()

	def Start(self):
		#print("Var = " + str(int(self.var.get())))
		self.SimulationWindow.Generate()
		if self.life == 1:
			ms = int(abs(self.MS - self.var.get()))
			#print("MS = " + str(ms))
			if ms < 10:
				ms = 10
			self.loop = self.after( ms ,self.Start)

	def Stop(self):
		self.life = 0
		self.button.config(text = "Start")
		
	def Generate(self):
		if self.life == 0:
			self.life = 1
			self.button.config(text = "Stop")
			self.Start()
		else :
			self.Stop()
			try :
				self.after_cancel(self.loop)
			except Exception as e:
				pass


	def ClearTheWorld(self):
		self.SimulationWindow.ClearAll()
		
class Grid(Canvas):
	def __init__(self, Master = None , CellSize = 10 , **kw):
		super().__init__(Master, **kw)
		self.pack(expand=True)		
		self.update()
		#################### 
		#some important constants
		self.CellSize = CellSize
		self.CalculateConstants()
		
		########################
	def CalculateConstants(self):
		self.bd = int(self.cget("bd")) + 2 
		self.width = self.winfo_width() - (self.bd * 2)
		self.height = self.winfo_height() - (self.bd * 2)

		self.CellCount = (self.width *  self.height) // (self.CellSize**2)
		#print("CellCount {}".format(self.CellCount))		
		self.widthCells = int(math.sqrt(self.CellCount)) #assumming that the world is square 
		
		#self.widthCells = self.width // self.CellSize  

	def GetBestPixelPosition(self, Xcor, Ycor):
		X = Xcor - (Xcor % self.CellSize) 
		Y = Ycor - (Ycor % self.CellSize) 
		if X >= self.width: X = self.width - self.CellSize -1
		if Y >= self.height: Y  = self.height - self.CellSize -1
		#print("{}...{}".format(Xcor ,Ycor ))
		return X , Y 

	def GetPositionFormIndex(self, Index):
		x = (Index % int(math.sqrt(self.CellCount)))
		y = (Index-x) // (self.width // self.CellSize)
		return x  * self.CellSize, y  * self.CellSize

	def GetIndexFormPosition(self, x , y):
		return  x // self.CellSize + (y//self.CellSize * (self.width // self.CellSize))
	
	def GetPositionFromId(self,Id):
		for index , cellId in (self.AliveCells.items()):
			if Id == cellId:
				return (self.GetPositionFormIndex(index))
	
	def Create_Grid(self,CellSize):
		self.CalculateConstants()
		bd = self.bd
		n_width = self.width 
		n_height = self.height

		for i in range(0, n_width , CellSize):
			self.create_line([(i + bd ,0), (i + bd , n_height + 1)] , fill="#999999" , tag='grid_line')#"#999999" 

		for i in range(0, n_height  , CellSize):
			self.create_line([(0, i + bd), (n_width+1, i + bd)] , fill="#999999" , tag='grid_line')

		print("{}...{}...{}".format(n_width,n_height, bd))
	

class GameOfLife(Grid):
	def __init__(self, Master = None , CellSize = 10 , **kw):
		super().__init__(Master, CellSize ,**kw)
		self.Master = Master
		self.bind("<1>", self.CreateCell)
		#self.bind("<MouseWheel>", self.zoom)
		self.AliveCells = {} # {index : id}
		self.Cells = [] 
		self.Create_Grid(CellSize)
		self.randomcells()

	def randomcells(self):
		for x in range(4000):
			self.ReviveCell(random.randint(0 , self.CellCount ))
	def GetCellCount(self):
		return len(self.AliveCells)
	def FixCells(self):
		#print(self.AliveCells.items())
		for id , index in self.AliveCells.items():
			#print(str(type(id)))
			x , y = self.GetPositionFormIndex(index)
			bbox = x + self.bd  + 1  , y + self.bd + 1 , x +  self.CellSize + self.bd   , y +  self.CellSize + self.bd 
			self.coords(id, bbox)
		#randomcells()
	def CreateCell(self ,event , Colour = "#FFFF00" , size = 10):
		#print("--------------" + str(type(event)))
		#self.CalculateConstants()
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
		#count = self.HighlightNeighbours(index)
		#print(str(count))

	def ReviveCell(self, index,Colour = "#FFFF00"):
		event = tkinter.Event()
		event.x ,event.y = self.GetPositionFormIndex(index)
		event.x += 2 
		event.y +=2
		self.CreateCell(event,Colour)

	def HighlightNeighbours(self, index):
		neighbours = [ index - self.widthCells - 1 , index - self.widthCells , index - self.widthCells +1,
				index -1 , index + 1,
				index + self.widthCells -1 , index + self.widthCells ,  index + self.widthCells +1
			]
		for neighbour in  neighbours:

			x , y = self.GetPositionFormIndex(neighbour)
			bd = self.bd
			bbox =  x + bd + 1  , y + bd + 1 , x +  self.CellSize + bd  , y +  self.CellSize + bd
			id = self.create_rectangle(bbox, fill="#FFFFFF", outline = "#999999" , tag="Live",width = 0) 

	def GetNeighboursCount(self,  index):
		neighbours = [ index - self.widthCells - 1 , index - self.widthCells , index - self.widthCells +1,
				index -1 , index + 1,
				index + self.widthCells -1 , index + self.widthCells ,  index + self.widthCells +1
			]
		count = 0 
		for neighbour in  neighbours:
			if  neighbour in self.AliveCells.keys():
				count +=1
		return count
		
#############################
# #Rules
# 1 Overpopulation: if a living cell is surrounded by more than three living cells, it dies.
# 2 Stasis: if a living cell is surrounded by two or three living cells, it survives.
# 3 Underpopulation: if a living cell is surrounded by fewer than two living cells, it dies.
# 4 Reproduction: if a dead cell is surrounded by exactly three cells, it becomes a live cell.
##############################
	def Generate(self):
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
			self.ReviveCell(index)
		self.Master.Generations.set(self.Master.Generations.get() + 1)
		return
	
	def ClearAll(self):
		for index in range(0, self.CellCount,1):
			if (index in self.AliveCells.keys()) :
				self.delete(self.AliveCells[index])
				del self.AliveCells[index]
	def zoom(self, event = None):
		if event == None :
			return
		if event.delta > 0 : 
			print("Zoom In")
			self.delete("grid_line")
			self.CellSize = 5
			self.Create_Grid(5)
			self.FixCells()
		if event.delta < 0 :
			print("Zoom out")
			self.delete("grid_line")
			self.CellSize = 10
			self.Create_Grid(10)
			self.FixCells()

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


root = Root(None,"Game Of Life" , "700x700+75+75", False)
Game = MainFrame(root, bg="#D3D3D3")

root.mainloop()
