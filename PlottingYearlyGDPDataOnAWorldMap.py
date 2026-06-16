"""
plot yearly GDP data on a world map
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

def build_country_code_converter(codeinfo):
    """
    Input:
        codeinfo - A dictionary that stores the information of the 
        dataset consisting of the different codes used for each country.
    Output:
        Returns a dictionary whose key-value pairs correspond to 
        country codes. The key in each pair is the country code 
        used by the plotting library, and the corresponding value 
        is the country code used by the GDP dataset.
    """
    country_codes = read_csv_as_nested_dict(codeinfo['codefile'], 
                                            codeinfo['plot_codes'], 
                                            codeinfo['separator'], 
                                            codeinfo['quote'])
    plot_gdp_codes = {}
    for code in country_codes:
        plot_gdp_codes[code] = country_codes[code][codeinfo['data_codes']]
    return plot_gdp_codes

def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Input:
        codeinfo - A dictionary that stores the information of the 
        dataset consisting of the different codes used for each country.
        plot_countries - A dictionary that stores information about the 
        countries that the plot library handles. Each key-value pair contains 
        a country code as the key and the country name as the value.
        gdp_countries - A dictionary that stores information about the 
        countries that appear in the GDP dataset. The key of each key-value 
        pair is a country code within the GDP dataset, and its corresponding 
        value can be anything.
    Output:
        Returns a dictionary and a set. The dictionary contains country codes. 
        The key of each key-value pair is a country code from plot_country that 
        corresponds to a country also in gdp_countries. The corresponding value 
        is the country code in gdp_countries. The set contains the country codes 
        in plot_countries that correspond to countries not in gdp_countries.
    """
    plot_dgp_codes = build_country_code_converter(codeinfo)
    common_codes = {}
    uncommon_codes = set()
    for code in plot_countries:
        uncommon_codes.add(code)
    for code1, code2 in plot_dgp_codes.items():
        for country1 in plot_countries:
            for country2 in gdp_countries:
                if (country1.casefold() == code1.casefold() 
                    and country2.casefold() == code2.casefold()):
                    uncommon_codes.discard(country1)
                    common_codes[country1] = country2
    return common_codes, uncommon_codes

def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs: 
        gdpinfo - Dictionary with information describing the GDP dataset.
        codeinfo - A dictionary that stores the information of the 
        dataset consisting of the different codes used for each country.
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
    gdp_countries = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_code"], 
                                            gdpinfo["separator"], gdpinfo["quote"])
    common_countries, uncommon_countries = reconcile_countries_by_code(codeinfo, 
                                                                       plot_countries, 
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
    
def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
        gdpinfo - Dictionary with information describing the GDP dataset.
        codeinfo - A dictionary that stores the information of the 
        dataset consisting of the different codes used for each country.
        plot_countries - A dictionary whose key-value pairs correspond 
        to the countries accepted by a plotting library. The key of each 
        pair is a country code, and the corresponding value is the country name.
        year - Integer denoting the year used to plot GDP data.
        map_file - String denoting the name of the SVG file. 
    Outputs:
        Returns an SVG plot named map_file of GDP data on a world map for the specified year.
    """
    data, uncommon, no_gdp = build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year)
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

########################
# plot yearly GDP data #
########################

codeinfo = {
        "codefile": "final_project\\isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

gdpinfo = {
        "gdpfile": "final_project\\isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

# get the country codes and names that pygal handles
pygal_countries = pygal.maps.world.COUNTRIES

# plot gdp data by year
render_world_map(gdpinfo, codeinfo, pygal_countries, 2010, "gdp_map.svg")
