import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import cv2
import os.path
from datetime import date
import numpy as np
import explorer_handler as eh
import stats_n_graphs as sg

#creatig a path variable to work wit the right directory
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
os.chdir(__location__)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# pd.reset_option('display.max_rows')
# pd.reset_option('display.max_columns')

def create_testplot():
    plt.plot(range(10))
    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax = create_court(ax, 'black')
    plt.savefig('testplot.png')

# Function to draw basketball court
def create_court(ax:plt, color):


    # General plot parameters
    mpl.rcParams['font.family'] = 'Arial'
    mpl.rcParams['font.size'] = 18
    mpl.rcParams['axes.linewidth'] = 2

    # Short corner 3PT lines
    ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
    ax.plot([220, 220], [0, 140], linewidth=2, color=color)

    # 3PT Arc
    ax.add_patch(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, 
                                 facecolor='none', edgecolor=color, lw=2, zorder=2))

    # Lane and Key
    ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
    ax.plot([80, 80], [0, 190], linewidth=2, color=color)
    ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
    ax.plot([60, 60], [0, 190], linewidth=2, color=color)
    ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
    ax.add_patch(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=2, zorder=2))

    # Rim
    ax.add_patch(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=2, zorder=2))

    # Backboard
    ax.plot([-30, 30], [40, 40], linewidth=2, color=color)

    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Set axis limits
    ax.set_xlim(-250, 250)
    ax.set_ylim(0, 470)
    
    return ax

    # Draw basketball court

# Function to get shot coords
def create_shot_arrays(player_data:list):
    X_COORD = []
    Y_COORD = []
    for i in range(0,len(player_data)):
        if player_data[i][0] is not None:
            X_COORD.append(player_data[i][0])
        if player_data[i][1] is not None:
            Y_COORD.append(player_data[i][1])
    X_COORD = np.array(X_COORD)
    Y_COORD = np.array(Y_COORD)
    return X_COORD, Y_COORD

# Function to create heatmap
def create_heatmap(hm_name:str, X:list[int], Y:list[int], color):
    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax = create_court(ax, 'black')
    ax = plt.hexbin(1.25*X - 250, -(47/40)*Y + 470, gridsize=(10,10), 
                    extent=(-250, 250, 0, 470), bins= None, cmap=color, alpha = 0.8)   
     
    eh.create_folders_in_path(hm_name)
    #plt.show()
    fig.savefig(hm_name + '\\heatmap ' + str(date.today()) + '.png', dpi=fig.dpi)

# function to display the coordinates of the points clicked on the image
def click_event(event, x, y, flags, params):

    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:

        # displaying the circle on the Shell
        cv2.circle(params[1],(x,y),5,(0,0,0),2)
        params[0][1].append([x,y])
        print(params[0])
        cv2.imshow(params[0][0], params[1])

    # checking for right mouse clicks
    if event==cv2.EVENT_RBUTTONDOWN:

        # displaying the coordinates
        # on the Shell
        cv2.line(params[1], (x-2, y+2), (x+2, y-2), (0, 0, 0), 2)
        cv2.line(params[1], (x-2, y-2), (x+2, y+2), (0, 0, 0), 2)
        params[0][2].append([x,y])
        print(params[0])

        cv2.imshow(params[0][0], params[1])

# creates the temp list we need to save the shots' coordinates keeps a list of the roster of the team
def tempshotlist():

    global roster, df
    #create a list of tupples that will contain name, [X_shot_success, Y_shot_success], [X_shot_fail, Y_shot_fail]
    roster = []
    no_players = int(input("Give the number of the players"))
    for i in range(0,no_players):
        player_name = input("Enter player name")
        #we create a global with the player's name that is a list
        player_data = (player_name, [], [])
        df = pd.DataFrame(columns= [str(date.today()) + "_X_success", str(date.today()) + "_Y_success"])
        
        roster.append(player_data)

def start_recording():
    # reading the image
    images = [] 
    # displaying the image
    for i in range(0, len(roster)):
        images.append(cv2.imread('testplot.png', 1))
        cv2.namedWindow(roster[i][0], cv2.WINDOW_NORMAL)
        cv2.imshow(roster[i][0], images[i])
        # setting mouse handler for the image and calling the click_event() function
        cv2.setMouseCallback(roster[i][0], click_event, [roster[i],images[i],i])

def assess_data(save=True, hm=False): 
    columns= [str(date.today()) + "_X_success", str(date.today()) + "_Y_success",
              str(date.today()) + "_X_fail", str(date.today()) + "_Y_fail"]

    for player in roster:
        # create the directories
        shots_path = os.path.join(__location__, "Roster", str(player[0]))
        eh.create_folders_in_path(shots_path)

        if save:
            X_COORD_SUCCESS, Y_COORD_SUCCESS = create_shot_arrays(player[1])
            X_COORD_FAIL, Y_COORD_FAIL = create_shot_arrays(player[2])

            data = pd.concat([pd.Series(X_COORD_SUCCESS,name=columns[0]),
                              pd.Series(Y_COORD_SUCCESS,name=columns[1]),
                              pd.Series(X_COORD_FAIL,name=columns[2]),
                              pd.Series(Y_COORD_FAIL,name=columns[3])], 
                              axis=1)
            print("data :", data)
            export_data(data, shots_path)

        if hm:
            create_heatmap(shots_path + "\\SUCCESS", X_COORD_SUCCESS, Y_COORD_SUCCESS, "Blues")
            create_heatmap(shots_path+ "\\FAIL", X_COORD_FAIL, Y_COORD_FAIL, "Reds")

def export_data(dataframe, dir):
        ex_data = eh.append_shot_data_to_csv(dir + "\\shots.csv", dataframe)
        cat_data = sg.categorize_shot_data(dir + "\\shots.csv")
        sg.shot_density(cat_data)
    
def stop_recording():
    cv2.destroyAllWindows()


# driver function
def main():
    global X_COORD_SUCCESS, Y_COORD_SUCCESS, X_COORD_FAIL, Y_COORD_FAIL
    
    tempshotlist()
    start_recording()
    # wait for a key to be pressed to exit
    cv2.waitKey(0)

    #asses data before stop recording
    assess_data(save=True,hm=True)
        
    stop_recording()

if not os.path.isfile('testplot.png'):
    create_testplot()

img  = cv2.imread('testplot.png', 1)

if __name__=="__main__":
    main()

    pass

