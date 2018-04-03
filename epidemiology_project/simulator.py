import random
import math
from matplotlib import pyplot as plt

def normpdf(x, mean, sd):
    """
    Return the value of the normal distribution 
    with the specified mean and standard deviation (sd) at
    position x.
    You do not have to understand how this function works exactly. 
    """
    var = float(sd)**2
    denom = (2*math.pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom

def pdeath(x, mean, sd):
    start = x-0.5
    end = x+0.5
    step =0.01    
    integral = 0.0
    while start<=end:
        integral += step * (normpdf(start,mean,sd) + normpdf(start+step,mean,sd)) / 2
        start += step            
    return integral    
    
recovery_time = 4 # recovery time in time-steps
virality = 0.2    # probability that a neighbor cell is infected in 
                  # each time step                                                  
#average amout of counts until a cell dies
avg_die_time =3
#standard deviation until death
dev =1
class Cell(object):

    def __init__(self,x, y):
        self.x = x
        self.y = y 
        self.state = "S" # can be "S" (susceptible), "R" (resistant = dead), or 
                         # "I" (infected)
        self.infect_counter =0
    def infect(self):
        #change cell attribute
        self.state = "I"
        self.infect_counter =1
    def process(self, adjacent_cells):
        #check to see if cell is infected
        #do no action if cell is dead or susceptable
        if(self.state!="I"):
            return
        #allow recovery
        self.infect_counter+=1
        if(self.infect_counter==recovery_time):
            self.state="S"
            self.infect_counter=0
        #allow for death
        if((self.state=="I") and 
           random.random()<pdeath(self.infect_counter,avg_die_time,dev)):
            self.state="R"
        #check adjacent cells
        #there is a chence their state will change
        #we can only infect susceptable cells
        i =0
        rand = random.random()
        while ((self.state=="I") and i<len(adjacent_cells)):
            if((rand<=virality) and (adjacent_cells[i].state=="S")):
                adjacent_cells[i].infect()
            i+=1
class Map(object):
    
    def __init__(self):
        self.height = 150
        self.width = 150 
        self.cells = {}          
    def add_cell(self, cell):
        ##in cells, the keys are (x,y)
        #keys are the cell instance
        self.cells[(cell.x,cell.y)] =cell
        
    def display(self):
        #start by instantiating a 150*150 array
        #default pixel is black
        image = []
        for y in range(0,151):
            row =[]
            for x in range(0,150):
                row.append((0.0,0.0,0.0))
            image.append(row)
        #iterate through dictionary of cells
        #change the pixels according to what
        #the Cells stored in cells are
        for k in self.cells.keys():
            cell_type = self.cells[k].state
            if (cell_type =="S"):
                image[int(k[0])][int(k[1])] = (0.0,1.0,0.0)
            if (cell_type =="R"):
                image[int(k[0])][int(k[1])] = (0.5,0.5,0.5)
            if (cell_type =="I"):
                image[int(k[0])][int(k[1])] = (1.0,0.0,0.0)
        #end fxn by showing the image
        plt.imshow(image)
    def time_step(self):
        #proccess the infection at every cell
        for k,v in self.cells.items():
            v.process(self.adjacent_cells(k[0],k[1]))
        self.display()
        
    def adjacent_cells(self, x,y):
        ans_list =[]
        #check to see if the coordinates to the E,S,N,W
        #directions are cells or just water
        #if so, then add it to the list
        if((x,y-1) in self.cells):
            ans_list.append(self.cells[(x,y-1)]) 
        if((x,y+1) in self.cells):
            ans_list.append(self.cells[(x,y+1)]) 
        if((x+1,y) in self.cells):
            ans_list.append(self.cells[(x+1,y)])                    
        if((x-1,y) in self.cells):
            ans_list.append(self.cells[(x-1,y)])  
        return ans_list
            
def read_map(filename):
    m = Map()
    f = open(filename, 'r')
    for line in f.readlines():
    ##partition csv-line into an array    
        line_arr = line.split(',')
    ##create a cell based on the x,y value
        ##add the new cell to the map    
        m.add_cell(Cell(int(line_arr[0]) , int(line_arr[1])))      
    return m