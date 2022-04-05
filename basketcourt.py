import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.image as mpimg
import cv2
import inspect
import os.path
from datetime import date
import numpy as np


def create_testplot():
    plt.plot(range(10))
    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax = create_court(ax, 'black')
    plt.savefig('testplot.png')

# Function to draw basketball court
def create_court(ax, color, heatmap=False):


    # General plot parameters
    mpl.rcParams['font.family'] = 'Avenir'
    mpl.rcParams['font.size'] = 18
    mpl.rcParams['axes.linewidth'] = 2

    # Short corner 3PT lines
    ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
    ax.plot([220, 220], [0, 140], linewidth=2, color=color)

    # 3PT Arc
    ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))

    # Lane and Key
    ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
    ax.plot([80, 80], [0, 190], linewidth=2, color=color)
    ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
    ax.plot([60, 60], [0, 190], linewidth=2, color=color)
    ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
    ax.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=2))

    # Rim
    ax.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=2))

    # Backboard
    ax.plot([-30, 30], [40, 40], linewidth=2, color=color)

    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Set axis limits
    ax.set_xlim(-250, 250)
    ax.set_ylim(0, 470)

    if heatmap == True:
            ax.hexbin(X_COORD*60/35 - 125*60/35 -30, Y_COORD*(-130/75)+(467+1/3), gridsize=(30, 30), extent=(-300, 300, 0, 940), bins='log', cmap='Blues')
            ax.text(0, 1.05, player_name, transform=ax.transAxes, ha='left', va='baseline')

    # Draw basketball court

def create_heatmap():
    global X_COORD, Y_COORD
    global player_name
    player_name = input("name the players hitmap that you want")
    X_COORD = []
    Y_COORD = []
    for i in range(0,len(eval(player_name))):
        X_COORD.append(eval(player_name)[i][0])
        Y_COORD.append(eval(player_name)[i][1])
    X_COORD = np.array(X_COORD)
    Y_COORD = np.array(Y_COORD)
    print(X_COORD)
    print(Y_COORD)
    plt.plot(range(10))
    fig = plt.figure(figsize=(3.17708, 3.29167))
    ax = fig.add_axes([0, 0, 1, 1])
    ax = create_court(ax, 'black', heatmap=True)
    plt.savefig('testplot'+ str(date.today()) + '.png')


# function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flags, params):

    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:

        # displaying the circle
        # on the Shell
        cv2.circle(params[1],(x,y),5,(0,0,0),2)
        eval(roster[params[2]]).append([x,y])
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(img, str(x) + ',' +
        #            str(y), (x,y), font,
        #            1, (255, 0, 0), 2)
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(img, str(b) + ',' +
                    str(g) + ',' + str(r),
                    (x,y), font, 1,
                    (255, 255, 0), 2)
        cv2.imshow(params[0], params[1])

    # checking for right mouse clicks
    if event==cv2.EVENT_RBUTTONDOWN:

        # displaying the coordinates
        # on the Shell
        #print(x, ' ', y)
        cv2.line(params[1], (x-2, y+2), (x+2, y-2), (0, 0, 0), 2)
        cv2.line(params[1], (x-2, y-2), (x+2, y+2), (0, 0, 0), 2)
        eval(roster[params[2]]).append([x,y])
        # displaying the coordinates
        # on the image window
        #font = cv2.FONT_HERSHEY_SIMPLEX
        #b = img[y, x, 0]
        #g = img[y, x, 1]
        #r = img[y, x, 2]
        #cv2.putText(img, str(b) + ',' +
                    #str(g) + ',' + str(r),
                    #(x,y), font, 1,
                    #(255, 255, 0), 2)
        cv2.imshow(params[0], params[1])

# creates the temp list we need to save the shots' coordinates
# keeps a list of the roster of the team
def tempshotlist():

    global roster
    no_players = int(input("Give the number of the players"))
    roster = []
    for i in range(0,no_players):
        player_name = input("Enter player name")
        globals()[player_name] = []
        roster.append(player_name)
        print(roster)

def statrecording():

    courtpng = Image.open('testplot.png')
    courtpng.save('court.png')
    # reading the image
    img0  = cv2.imread('testplot.png', 1)
    img1  = cv2.imread('testplot.png', 1)
    img2  = cv2.imread('testplot.png', 1)
    c = [img0, img1, img2]
    # displaying the image
    for i in range(0, len(roster)):
        cv2.namedWindow(roster[i], cv2.WINDOW_NORMAL)
        cv2.resizeWindow(roster[i], 305, 316)
        cv2.imshow(roster[i], c[i])
        # setting mouse handler for the image
        # and calling the click_event() function
        cv2.setMouseCallback(roster[i], click_event, [roster[i],c[i],i])
    # wait for a key to be pressed to exit
    cv2.waitKey(0)
    # close the window
    create_heatmap()
    cv2.destroyAllWindows()


# driver function
def main():
    tempshotlist()
    statrecording()

if not os.path.isfile('testplot.png'):
    create_testplot()

img  = cv2.imread('testplot.png', 1)

if __name__=="__main__":
    main()

#print(eval('kimon')[0])
#cv2.createButton("Undo",undo,None,cv2.QT_PUSH_BUTTON,1)

#def undo(*args):

    pass

