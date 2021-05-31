import cv2
import numpy as np
import pandas as pd
import argparse
import kmeans as km

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
colour_name = []

# Read the csv file
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# Resize an image according to the diminishFactor
def diminish(img, diminishFactor : int):
    row, col, temp = img.shape
    b_plane = img[:,:,0]
    g_plane = img[:,:,1]
    r_plane = img[:,:,2]

    # Calculate the size of the resized image
    resized_b_plane = b_plane[1::diminishFactor,1::diminishFactor]
    resized_g_plane = g_plane[1::diminishFactor,1::diminishFactor]
    resized_r_plane = r_plane[1::diminishFactor,1::diminishFactor]

    resized_img = np.zeros((row//diminishFactor, col//diminishFactor, temp),np.uint8)
    resized_img[:,:,0] = resized_b_plane
    resized_img[:,:,1] = resized_g_plane
    resized_img[:,:,2] = resized_r_plane
    return resized_img


# Calculate minimum distance from all colours and get the most matching color
def getColorName(R,G,B):
    minimum = 1e9
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            colour_name = csv.loc[i,"color_name"]
    return colour_name

# To calculate the complementary colour for a given colour
def getComplementaryColour(r : int , g : int , b : int):
    return [255-r, 255-g, 255-b]

# Get and return the index for the closest match Shirt for our pants
def getClosestMatch(colour_codes : list):
    comp_colour = getComplementaryColour(colour_codes[0][0], colour_codes[0][1], colour_codes[0][2])
    minimum = 1e9
    best = -1
    
    # Find the closest match with the minumum absolute difference
    for i in range(1, len(colour_codes)):
        d = np.sum(np.abs(np.subtract(comp_colour, colour_codes[i])))
        
        if(d<=minimum):
            minimum = d
            best = i
    return best

def displayMostSuitableTop(idx : int, img_path : list):
    # Read the image and rescale it to 70%
    cv2.destroyAllWindows()
    img = cv2.imread(img_path[idx])
    img = diminish(img, 2)

    # Set the window name and display the image
    windowName = "Match"
    cv2.namedWindow(windowName)
    while (1):
        cv2.imshow(windowName, img)
        # Draw a rectangle and display the text
        cv2.rectangle(img, (20, 20), (750, 60), (0,0,0), -1)
        text = "Best Match. ESC to exit."   
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # Break the loop when user hits 'esc' key
        if cv2.waitKey(20) & 0xFF == 27:
            cv2.destroyAllWindows()
            break

    

# Obtain the colour for each picture
for i in range(len(img_path)):
    b, g, r = 0,0,0
    clicked = False

    # Read and rescale the image
    img = cv2.imread(img_path[i])
    img = diminish(img, 2)
    
    # Compress the image colour using K-means algorithm
    img = km.perform_Kmeans(img)

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
            cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
            text = 'Colour: ' + getColorName(r, g, b) + ', Press TAB to confirm selection'

            # For very light colour_codes we will display text in black colour
            if (r + g + b >= 600):
                cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
            else:
                cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

            clicked=False

        # Break the loop when user hits 'esc' key
        if cv2.waitKey(20) & 0xFF == 9:
            colour_name.append(getColorName(r, g, b))
            colour_codes.append([r,g,b])
            cv2.destroyAllWindows()
            break

print(colour_codes)
print(colour_name)
idx = getClosestMatch(colour_codes)
# print("The closest match for your pants is {}-th shirt, with the colour of {}".format(idx+1, colours[idx]
print("The most suitable colour to match with your pants is", colour_name[idx])
displayMostSuitableTop(idx, img_path)