"""
read a county-level map of the USA in PNG format using matplotlib
and add two scatter point to it
"""

import matplotlib.pyplot as plt
from PIL import Image

# location of Houston in a USA map in SVG format
USA_SVG_DIMENTIONS = [555, 352]
HOUSTON_POS = [302, 280]

def draw_USA_map(map_name):
    """
    Input:
        map_name - name of a USA map in PNG format 
    Output:
        Returns a drawing of the map with a scatter point 
        at the center of the map and in Houston.
    """
    # read map image
    img = plt.imread(map_name)

    # get dimensions of the map
    height, width, channels = img.shape

    # create plot
    plt.imshow(img)
    
    # add a green scatter point in the center of the map
    plt.scatter(width/2, height/2, s = 20, c = 'g')

    # add red scatter point on Houston, TX
    # using its location in the USA map in SVG format
    plt.scatter((HOUSTON_POS[0]/USA_SVG_DIMENTIONS[0])*width, (HOUSTON_POS[1]/USA_SVG_DIMENTIONS[1])*height, s = 20, c = 'r')

    # show the plot
    plt.show()

draw_USA_map('USA_Counties_555x352.png')
draw_USA_map('USA_Counties_1000x634.png')
