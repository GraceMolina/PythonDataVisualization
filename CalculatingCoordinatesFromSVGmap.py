"""
extract data from a SVG file
"""

from xml.dom import minidom
import re
import math
import csv

# get attributes from the SVG file
def get_county_attributes(svg_file_name):
    """
    Input:
        svg_file_name - name of a SVG file
    Output:
        Returns a list of 2-tuples. The first component of each 2-tuple is the path string id,
        and the second component is the path string d.
    """
    doc = minidom.parse(svg_file_name)  # read file
    path_id = [path.getAttribute('id') for path
                    in doc.getElementsByTagName('path')] # extract path string id
    path_d = [path.getAttribute('d') for path
                    in doc.getElementsByTagName('path')] # extract path string d
    doc.unlink()
    attributes = [(id, d) for id, d in zip(path_id, path_d)] # form list of 2-tuples
    return attributes

# extract coordinates from string
def get_boundary_coordinates(boundary_data):
    # find pairs of decimals separated by a comma
    matches = re.findall(r"([0-9.]+),([0-9.]+)", boundary_data)
    # convert pairs of strings to pairs of floats
    coordinates = [(float(x), float(y)) for x, y in matches]
    return coordinates

# estimate the center of a county using its boundary coordinates
def dist(pt1, pt2):
    """
    Returns the Euclidean distance between two points.
    """
    return math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

def compute_county_center(boundary_coordinates):
    """
    Input:
        boundary_coordinates - list of boundary coordinates (2-tuples)
    Output:
        Returns an stimate of the county center as a pair of floats.
        Assumes that coordinates form a closed polygon with the first coordinate 
        equal to the last one.
    """
    centroid = [0, 0]
    perimeter = 0
    for idx in range(len(boundary_coordinates) - 1):
        edge_length = dist(boundary_coordinates[idx], boundary_coordinates[idx + 1])
        centroid[0] += 0.5 * (boundary_coordinates[idx][0] + boundary_coordinates[idx + 1][0]) * edge_length
        centroid[1] += 0.5 * (boundary_coordinates[idx][1] + boundary_coordinates[idx + 1][1]) * edge_length
        perimeter += edge_length
    return [(centroid[0] / perimeter), (centroid[1] / perimeter)]

def write_csv_file(csv_table, file_name):
    """
    Given a nested list csv_table and a string name file_name, 
    write the fields in the csv_table into a comma-separated CSV file with the name file_name.
    """
    with open(file_name, 'w', newline = '') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter = ',')
        for row in csv_table:
            csvwriter.writerow(row)

#  save the center of each county as a CSV file
def process_county_attributes(svg_file_name, csv_file_name):
    """
    Inputs: 
        svg_file_name - name of a SVG file with path data
        csv_file_name - string to name the CSV file
    Outups: 
        Returns a CSV file with three columns: county FIPS code,
        horizontal coordinate of the county center, and vertical coordinate of the county center.
    """
    county_centers = []
    county_centers.append(['FIPS', 'horizontal coordinate', 'vertical coordinate'])
    attributes = get_county_attributes(svg_file_name)
    for county in attributes:
        county_data = []
        coordinates = get_boundary_coordinates(county[1])
        county_center = compute_county_center(coordinates)
        county_data.append(county[0])
        county_data.append(county_center[0])
        county_data.append(county_center[1])
        county_centers.append(county_data)
    write_csv_file(county_centers, csv_file_name)

process_county_attributes("USA_Counties_2014.svg", "County_Centers_Data.csv")

