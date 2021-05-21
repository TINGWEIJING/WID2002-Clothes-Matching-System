import cv2
import numpy as np
import pandas as pd
import argparse

#Creating argument parser to take image path from command line
ap = argparse.ArgumentParser()
ap.add_argument('-b', '--bottom', required=True, help="Image Path of bottom")
ap.add_argument('-t', '--top', required=True, help="Image Path of top, separated by comma")
args = vars(ap.parse_args())

# Combine the path of bottom and top
img_path = [args['bottom']]
for x in args['top'].split(sep=','):
    img_path.append(x)
print(img_path)

# Array to store the colour and colour codes of pants and shirts
colour_codes = []
colours = []

#Reading csv file with pandas and giving names to each column
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

#function to calculate minimum distance from all colors and get the most matching color
def getColorName(R,G,B):
    minimum = 1e9
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            colour_name = csv.loc[i,"color_name"]
    return colour_name

# Obtain the colour for each picture
for i in range(len(img_path)):
    b, g, r = 0,0,0
    clicked = False

    # Read and resize the image
    img = cv2.imread(img_path[i])
    width = int(img.shape[1] * 70 / 100)
    height = int(img.shape[0] * 70 / 100)
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    windowName = ""

    def draw_function(event, x, y, flags, param):
        global b, g, r, clicked
        if event == cv2.EVENT_LBUTTONDBLCLK:
            clicked = True
            b, g, r = img[y, x]
            b = int(b)
            g = int(g)
            r = int(r)

    if i == 0:
        windowName = "Bottom"

    else:
        windowName = "Top"

    cv2.namedWindow(windowName)
    cv2.setMouseCallback(windowName, draw_function)

    # display the image and requst user to click
    while (1):
        cv2.imshow(windowName, img)
        if (clicked):

            # cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
            cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

            # Creating text string to display( Color name and RGB values )
            text = 'Colour: ' + getColorName(r, g, b) + ', Press TAB to confirm selection'

            # For very light colour_codes we will display text in black colour
            if (r + g + b >= 600):
                cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
            else:
                # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
                cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

            clicked=False

        # Break the loop when user hits 'esc' key
        if cv2.waitKey(20) & 0xFF == 9:
            colours.append(getColorName(r, g, b))
            colour_codes.append([r,g,b])
            cv2.destroyAllWindows()
            break

print(colour_codes)
print(colours)