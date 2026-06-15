"""
load a plot cancer risk data on a USA map
"""

import matplotlib.pyplot as plt
from PIL import Image
import csv
import math
import matplotlib

# dimentions of USA map in SVG format
USA_SVG_DIMENTIONS = [555, 352]

def read_csv_as_nested_list(filename, separator, quote):
    """
    Takes a CSV file, a separator, and a quote. Returns the data within 
    the file as a list of dictionaries.
    """
    table = []
    with open(filename, "rt", newline = '', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter = separator, 
                                   quotechar = quote)
        for row in csvreader:
            table.append(row)
        return table

def compute_county_cirle(county_population):
    """
    Input:
        county_population - integer representing the population of a county
    Output:
        Returns the value of a linear function evaluated at county_population. 
        This linear function maps the interval [67, 9519338] to [0, 500] and 
        serves to transform county population data.
    """
    b = 500/(9519338 - 67)
    y = b*county_population - b*67
    return y

# max and min values for cancer risk
MIN_CANCER_RISK = math.log(0.0000086)
MAX_CANCER_RISK = math.log(0.00015)

def create_riskmap(colormap):
    """
    Input:
        colormap - string denoting the name of a colormap in matplotlib
    Output:
        Returns a function that maps a level of cancer risk to an RGB in the given colormap.
    """
    cmap = plt.colormaps[colormap]
    norm = plt.Normalize(vmin = MIN_CANCER_RISK, vmax = MAX_CANCER_RISK)
    cancer_risk = matplotlib.cm.ScalarMappable(norm = norm, cmap = cmap)
    return lambda risk: cancer_risk.to_rgba(math.log(risk))

def draw_cancer_risk_map(joined_csv_file_name, map_name, num_counties = None):
    """
    Inputs:
        joined_csv_file_name - A CSV file containing cancer-risk data by county 
        and county center coordinates
        map_name - name of USA map
        num_counties - number of counties with higher cancer risk
    Outputs:
        Draws a map and adds a scatter point for the number of counties specified 
        by num_counties with the highest cancer risk. The size of the scatter point 
        is proportional to its population, and the color indicates cancer risk, 
        with red denoting high risk and blue low risk.
    """
    # read map image
    img = plt.imread(map_name)

    # get dimensions of the map
    height, width, channels = img.shape

    # create plot
    plt.imshow(img)

    # read merged dataset
    data = read_csv_as_nested_list(joined_csv_file_name, ',', '"')
    del data[0]

    # sort data by cancer risk
    data.sort(key = lambda x: float(x[4]), reverse = True)

    if num_counties is None:
        for row in data:
            x = float(row[5])
            y = float(row[6])
            county_position = [x, y]
            size = compute_county_cirle(float(row[3]))
            my_color = create_riskmap('jet')
            risk = float(row[4])
            color = my_color(risk)
            plt.scatter((county_position[0]/USA_SVG_DIMENTIONS[0])*width, (county_position[1]/USA_SVG_DIMENTIONS[1])*height, s = size, color = color)
    else:
        for county in range(0, num_counties):
            row = data[county]
            x = float(row[5])
            y = float(row[6])
            county_position = [x, y]
            size = compute_county_cirle(float(row[3]))
            my_color = create_riskmap('jet')
            risk = float(row[4])
            color = my_color(risk)
            plt.scatter((county_position[0]/USA_SVG_DIMENTIONS[0])*width, (county_position[1]/USA_SVG_DIMENTIONS[1])*height, s = size, color = color)

    # show the plot
    plt.show()

draw_cancer_risk_map('cancer_risk_dataset.csv', 'USA_Counties_555x352.png', 100)
draw_cancer_risk_map('cancer_risk_dataset.csv', 'USA_Counties_1000x634.png', 100)