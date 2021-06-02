import cv2
import numpy as np
import pandas as pd
import argparse
import kmeans as km
import matplotlib as mpl
from PIL import Image

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

# Nearest-neighbour (NN) interpolation, used to rescale the image
def nn_interpolate(A, new_size):
    """

    new_size: tuple of (height, width, channel)
    channel = 3 for rgb
    Example: (512,512,3) is an image with 512 x 512, with RGB code for each pixel.

    """
    old_size = A.shape
    row_ratio, col_ratio, _ = np.array(new_size)/np.array(old_size)

    # row wise interpolation 
    row_idx = (np.ceil(range(1, 1 + int(old_size[0]*row_ratio))/row_ratio) - 1).astype(int)

    # column wise interpolation
    col_idx = (np.ceil(range(1, 1 + int(old_size[1]*col_ratio))/col_ratio) - 1).astype(int)

    final_matrix = A[:, col_idx][row_idx, :]

    return final_matrix

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
    """

    colour_codes: list of colour codes for all of the images, the first element
    would be the pants.
    [[b,g,r],[b,g,r],...[b,g,r]]
    
    """
    # Get the complement colour for our pants
    comp_colour = getComplementaryColour(colour_codes[0][0], colour_codes[0][1], colour_codes[0][2])
    minimum = 1e9
    best = -1 # To store the index for our best match, initialise to -1
    
    # Find the closest match with the minumum absolute difference
    for i in range(1, len(colour_codes)):
        d = np.sum(np.abs(np.subtract(comp_colour, colour_codes[i])))
        
        if(d<=minimum): # Replace the best match
            minimum = d
            best = i
    return best

def displayMostSuitableTop(idx : int, img_path : list):
    # Destroy all remaining windows
    cv2.destroyAllWindows()

    # Rescale the image
    img = np.array(Image.open(img_path[idx]))
    max_width = max([img.shape[0]//5, 500])
    max_height = max([img.shape[1]//5, 500])
    img = nn_interpolate(img,(max_width, max_height,3))
    img = Image.fromarray(img.astype('uint8')).convert('RGB')
    
    # Convert back to openCV2 format
    img = np.array(img) 
    img = img[:, :, ::-1].copy() 

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
    img = np.array(Image.open(img_path[i]))
    max_width = max([img.shape[0]//5, 500])
    max_height = max([img.shape[1]//5, 500])
    img = nn_interpolate(img,(max_width, max_height,3))
    img = Image.fromarray(img.astype('uint8')).convert('RGB')

    # Convert back to openCV2 format
    img = np.array(img) 
    img = img[:, :, ::-1].copy() 
    
    # Compress the image colour using K-means algorithm
    print("Performing K-Mean Clustering on Image {}".format(i+1))
    _, img = km.perform(img)

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

# Main Driver Code
print("The colour code for each cloth is", colour_codes)
print("The colour name for each cloth is", colour_name)
idx = getClosestMatch(colour_codes)
print("The most suitable colour to match with your pants is", colour_name[idx])
print("CTRL - C on the terminal or press ESC on the image to exit the program.")
displayMostSuitableTop(idx, img_path)