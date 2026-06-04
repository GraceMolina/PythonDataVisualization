"""
plot GDP data in a world map for a given year
"""

import csv
import pygal
import math

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Imputs:
        filename - Name of the CSV file that will be read.
        keyfield - Name of the colum with the id of each observation in the CSV file.
        separator - Delimiter of the CSV file.
        quote - Text qualifiers used in the CSV file to encapsulate entries with delimiters.
    Output:
        Returns the data within the file as a dictionary of dictionaries.
    """
    table = {}
    with open(filename, "rt", newline = '', encoding = 'utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter = separator, 
                                   quotechar = quote)
        for row in csvreader:
            table[row[keyfield]] = row
        return table

def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
        plot_countries - A dictionary whose key-value pairs correspond 
        to the countries accepted by a plotting library. The key of each 
        pair is a country code, and the corresponding value is the country name.
        gdp_countries -  A dictionary whose key-value pairs correspond
        to the countries in a GDP dataset. The key of each pair must be a country name.
    Outputs
        A dictionary and a set. The key of each key-value pair in the dictionary 
        is a country code from plot_countries, such that its corresponding name 
        can be found in gdp_countries. The value associated with each key is the 
        country's name as listed in gdp_countries. The set consists of the country 
        codes in plot_countries whose names are not in gdp_countries.
    """
    common_countries = {}
    uncommon_countries = set()
    for code, name in plot_countries.items():
        if name in gdp_countries.keys():
            common_countries[code] = name
        else:
            uncommon_countries.add(code)
    return common_countries, uncommon_countries

def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
        gdpinfo - Dictionary with information describing the GDP dataset.
        plot_countries - A dictionary whose key-value pairs correspond 
        to the countries accepted by a plotting library. The key of each 
        pair is a country code, and the corresponding value is the country name.
        year - Integer denoting the year used to plot GDP data.
    Outputs:
        Returns a dictionary and two sets. The key in each key-value pair is 
        a country code from plot_countries, such that its corresponding name 
        is in the GDP dataset. The value associated with each key is the logarithm 
        of that country's GDP in the given year. The first set contains the country 
        codes in plot_countries whose names are not in the GDP dataset. The second 
        set contains the country codes in plot_countries whose names appear in the 
        GDP dataset but have no GDP data for the given year.
    """
    gdp_countries = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"], 
                                            gdpinfo["separator"], gdpinfo["quote"])
    common_countries, uncommon_countries = reconcile_countries_by_name(plot_countries, 
                                                                       gdp_countries)
    if gdpinfo["min_year"] <= int(year) <= gdpinfo["max_year"]:
        no_gdp_data = set()
        data_dict = {}
        for key, value in common_countries.items():
            if gdp_countries[value][str(year)] != '':
                gdp = float(gdp_countries[value][str(year)])
                data_dict[key] = math.log10(gdp)
            else:
                no_gdp_data.add(key)
        return data_dict, uncommon_countries, no_gdp_data
    else:
        return 0, 0, 0

def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
        gdpinfo - Dictionary with information describing the GDP dataset.
        plot_countries - A dictionary whose key-value pairs correspond 
        to the countries accepted by a plotting library. The key of each 
        pair is a country code, and the corresponding value is the country name.
        year - Integer denoting the year used to plot GDP data.
        map_file - String denoting the name of the SVG file. 
    Outputs:
        Returns an SVG plot named map_file of GDP data on a world map for the specified year.
    """
    data, uncommon, no_gdp = build_map_dict_by_name(gdpinfo, plot_countries, year)
    if data != 0 and uncommon != 0 and no_gdp != 0:
        worldmap = pygal.maps.world.World(truncate_legend=-1)
        worldmap.title = 'Log(GDP) for the year ' + str(year)
        worldmap.add('Log(GDP)', data)
        worldmap.add('Not included in dataset', uncommon)
        worldmap.add('Missing GDP data', no_gdp)
        worldmap.render_to_file(map_file)
        #worldmap.render_in_browser() # render plot in browser
    else:
        print("Invalid year.")

gdpinfo = {
        "gdpfile": "project2/isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

# get the country codes and names that pygal handles
pygal_countries = pygal.maps.world.COUNTRIES

render_world_map(gdpinfo, pygal_countries, 2015, "map_gdp.svg")