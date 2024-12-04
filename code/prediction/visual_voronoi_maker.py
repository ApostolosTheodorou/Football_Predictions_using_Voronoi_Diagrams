#define the voronoi diagram's dimensions (suggested ratio 3:2)
width= 6
height= 4

#  - -  Preparation steps  - -  #

#install mpl soccer library
# !pip install mplsoccer

#import the necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch, VerticalPitch
from tkinter import *

#define a class with all the usefull information to handle the events 
#(mouse clicking, key pressing) and produce the voronoi diagram
class Attempt:
    
    #define the players' positions list (initialy empty)
    teamA_x_axis=[]
    teamA_y_axis=[]

    teamB_x_axis=[]
    teamB_y_axis=[]

    ball_holder_x_axis=[]
    ball_holder_y_axis=[]

    #define the ids of the players of the two teams (id shows the team a player belongs to)
    #let 0 be the id for players in teamA and 1 for players of teamB
    teamA_ids= [] #initially empty
    teamB_ids= [] #initially empty
    ball_holder_id=[] #initially empty

    last_change_made= []   #a stack which contains the team that was affected by the last insertion
                           #useful data structure for undo function
    
    canvas_shapes_ids= []  #another stack to support the canvas.delete function of the GUI tkinter library
                           #stores the last inserted shape's id

    #dummy constructor
    def __init__(self):
        pass
    
    #insert a player's position in the pitch (depict it with a red dot for team A)
    def add_player_teamA(self, x,y, shape_id):
        self.teamA_x_axis+= x  
        self.teamA_y_axis+= y
        self.last_change_made+= ["A"]
        self.canvas_shapes_ids+= [shape_id]
              
    #insert a player's position in the pitch (depict it with a blue dot for team B)
    def add_player_teamB(self, x,y, shape_id):
        self.teamB_x_axis+= x  
        self.teamB_y_axis+= y
        self.last_change_made+= ["B"]
        self.canvas_shapes_ids+= [shape_id]

    #insert the ball holder's position in the pitch (depict it with a yellow dot)
    def add_ball_holder(self, x,y, shape_id):
        self.ball_holder_x_axis+= x
        self.ball_holder_y_axis+= y
        self.last_change_made+= ["C"]
        self.canvas_shapes_ids+= [shape_id]

    #undo the last insertion made (the user can consequtively undo all the insertions from the last until the first one)  
    def undo(self):
        if len(self.last_change_made) == 0:
            return -1
        team= self.last_change_made.pop()
        if team == "A":
            self.teamA_x_axis.pop()
            self.teamA_y_axis.pop()
            shape_id= self.canvas_shapes_ids.pop()
            return shape_id
        elif team == "B":
            self.teamB_x_axis.pop()
            self.teamB_y_axis.pop()
            shape_id= self.canvas_shapes_ids.pop()
            return shape_id
        elif team == "C":
            self.ball_holder_x_axis.pop()
            self.ball_holder_y_axis.pop()
            shape_id= self.canvas_shapes_ids.pop()
            return shape_id
        else:
            return -1

    #create the voronoi diagram inside a football pitch according to the players' positions        
    def make_voronoi_diagram(self):
        global width, height  #the width and height of the voronoi diagram 
    
        #define the team_id of each player (players of the same team have the same team_id)
        self.teamA_ids= list(np.zeros((len(self.teamA_x_axis),),dtype=int)) #0s for the first team
        self.teamB_ids= list(np.ones((len(self.teamB_x_axis),),dtype=int))  #1s for the second team
        if len(self.ball_holder_x_axis) == 1:
            self.ball_holder_id= [2]
        elif len(self.ball_holder_x_axis) > 1:
            print("ERROR:\nTrying to make voronoi with more than one players making the attempt!\n")
            return

        #create a dataframe with all the players coordinates
        #first all the palyers of teamA followed by all the players of teamB
        positions_data = pd.DataFrame({
        'x':self.teamA_x_axis+self.teamB_x_axis+self.ball_holder_x_axis,
        'y':self.teamA_y_axis+self.teamB_y_axis+self.ball_holder_y_axis,
        'team':self.teamA_ids+self.teamB_ids+self.ball_holder_id
        })
    
        #define the plot's dimension
        fig, ax = plt.subplots(figsize=(width,height))
        fig.set_facecolor('#ffffff')
        ax.patch.set_facecolor('#ffffff')

        #The statsbomb pitch from mplsoccer
        pitch = VerticalPitch(pitch_type='statsbomb',
                pitch_color= '#001a00', line_color='#ffffff', half= True)#, #figsize=(23, 28),
                #constrained_layout=False, tight_layout=True, half=True)

        pitch.draw(ax=ax)
        

        #plot voronoi diagram
        x=positions_data.x
        y=positions_data.y
        team1,team2,ball_holder = pitch.voronoi(x,y,positions_data.team)
        t1 = pitch.polygon(team1, ax=ax, fc='#006600', ec='black', lw=3, alpha=0.4)
        t2 = pitch.polygon(team2, ax=ax, fc='#e60000', ec='black', lw=3, alpha=0.4)
        t2 = pitch.polygon(team2, ax=ax, fc='#e60000', ec='black', lw=3, alpha=0.4) #repeat the drawing of the red team for more distinct colors
        bh = pitch.polygon(ball_holder, ax=ax, fc='#fc8c04', ec='black', lw=3, alpha=0.4 )
        #repeat the drawing of the player who made the attempt for more distinct colors
        bh = pitch.polygon(ball_holder, ax=ax, fc='#fc8c04', ec='black', lw=3, alpha=0.4 )
        bh = pitch.polygon(ball_holder, ax=ax, fc='#fc8c04', ec='black', lw=3, alpha=0.4 )
        bh = pitch.polygon(ball_holder, ax=ax, fc='#fc8c04', ec='black', lw=3, alpha=0.4 )
        bh = pitch.polygon(ball_holder, ax=ax, fc='#fc8c04', ec='black', lw=3, alpha=0.4 )
        bh = pitch.polygon(ball_holder, ax=ax, fc='#fc8c04', ec='black', lw=3, alpha=0.4 )
        bh = pitch.polygon(ball_holder, ax=ax, fc='#fc8c04', ec='black', lw=3, alpha=0.4 )
        bh = pitch.polygon(ball_holder, ax=ax, fc='#fc8c04', ec='black', lw=3, alpha=0.4 )
        bh = pitch.polygon(ball_holder, ax=ax, fc='#fc8c04', ec='black', lw=3, alpha=0.4 )

        # Plot players
        for i in range(len(positions_data['x'])):
            if positions_data['team'][i]==0:
                pitch.scatter(positions_data['x'][i],positions_data['y'][i],ax=ax,color='red')
            if positions_data['team'][i]==1:
                pitch.scatter(positions_data['x'][i],positions_data['y'][i],ax=ax,color='#00cc00')
            if positions_data['team'][i]==2:
                pitch.scatter(positions_data['x'][i],positions_data['y'][i],ax=ax,color='#fff200')
        
        
        plt.show()
        
#define an instance of the Attempt class
attempt= Attempt()




#  - -  Event handlers (mouse clicking, enter and backspace)  - -  #

#add player in the GUI pitch for the first team by left click
def add_player_team_one(event): 
    x= (event.x-20)*120/900  #scale down coordinates from 900x600 to 120x80
    y= (event.y-20)*80/600   #scale down coordinates from 900x600 to 120x80
    shape_id= canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, fill="#d40000" , outline= "#d40000", width= 5)
    x=[x]
    y=[y]
    attempt.add_player_teamA(x,y, shape_id)
    
#add player in the GUI pitch for the second team by right click
def add_player_team_two(event):
    x= (event.x-20)*120/900  #scale down coordinates from 900x600 to 120x80
    y= (event.y-20)*80/600   #scale down coordinates from 900x600 to 120x80
    shape_id= canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, fill= "#000d85", outline="#000d85" , width= 5)
    x=[x]
    y=[y]
    attempt.add_player_teamB(x,y, shape_id)

#add the player who made the attempt in the GUI pitch by middle (scroll) mouse clik
def add_ball_holder(event):
    x= (event.x-20)*120/900  #scale down coordinates from 900x600 to 120x80
    y= (event.y-20)*80/600   #scale down coordinates from 900x600 to 120x80
    shape_id= canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, fill="#fff200" , outline= "#fff200", width= 5)
    x=[x]
    y=[y]
    attempt.add_ball_holder(x,y, shape_id)

#delete the last dot in the GUI pitch and update the corresponding positions list
def undo_last_change(event):
    shape_id= attempt.undo()
    if shape_id != -1:
        canvas.delete(shape_id)

#construct the voronoi diagram
def make_voronoi(event):
    attempt.make_voronoi_diagram()
    
#close the window and exit
def exit(event):
    root.destroy()   
            
            
            
            
#  - -  Create the GUI soccer pitch for positions data insertion via mouse clicking  - -  #
            
#create the window
root = Tk()
root.geometry('950x650')

#create the grass
canvas = Canvas(root, height=640, width=940, bg="#5cd65c")


#  - - create the lines - -  #

#end lines, side lines
canvas.create_rectangle(20,20,920,620, outline= "white", width= 3)

#half-way line
canvas.create_line(470,20,470,620, fill="white", width= 3)

#half-way circle
canvas.create_oval(395,245,545,395, outline="white", width= 3)

#left goal post
canvas.create_line(20,292.55,20,347.45, fill="white", width= 5)

#left goal area
canvas.create_rectangle(20,245,65,395, outline= "white", width= 3)

#left penalty area
canvas.create_rectangle(20,155,155,485, outline= "white", width= 3)

#left penalty arc
canvas.create_arc(125,262,185,377, start= 270, extent= 180, outline= "white", width= 3)

#left penalty spot
canvas.create_oval(109,318, 113,322, fill= "white", outline= "white", width= 2)

#right goal post
canvas.create_line(920,292.55,920,347.45, fill="white", width= 5)

#right goal area
canvas.create_rectangle(920,245,875,395, outline= "white", width= 3)

#right penalty area
canvas.create_rectangle(920,155,785,485, outline= "white", width= 3)

#right penalty arc
canvas.create_arc(755,262,815,377, start= 90, extent= 180, outline= "white", width= 3)

#right penalty spot
canvas.create_oval(831,318, 827,322, fill= "white", outline= "white", width= 2)





#  - - Create the players positions (dots) by clicking and bind the keybord events to specific actions - -  #

#team A (left click)
canvas.bind('<Button-1>', add_player_team_one)

#team B (right click)
canvas.bind('<Button-3>', add_player_team_two)

#ball holder (the player who does the attempt)
canvas.bind('<Button-2>', add_ball_holder)

#undo last insertion by BackSpace
root.bind('<BackSpace>', undo_last_change)

#press Enter to create the voronoi diagram
root.bind('<Return>', make_voronoi)

#press q to exit
root.bind('q', exit)

canvas.pack()


root.mainloop()
