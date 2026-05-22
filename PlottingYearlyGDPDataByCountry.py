"""
plot yearly GDP data by countries
save plot as a SVG file
"""

import csv
import pygal

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Imputs:
        filename - a CSV file
        keyfield - name of the colum with the id of each observation in the CSV file
        separator - delimiter of the CSV file
        quoate - text qualifiers used to encapsulate entries with delimiters
    Output:
        returns the data within the file as a dictionary of dictionaries
    """
    table = {}
    with open(filename, "rt", newline = '', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter = separator, 
                                   quotechar = quote)
        for row in csvreader:
            table[row[keyfield]] = row
        return table

def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
        gdpinfo - dictionary with information of the GDP data
        gdpdata - dictionary with yearly GDP data for a single country
    Output:
        Returns a list of 2-tuples; the first element of each tuple 
        represents a year (integer), while the second element corresponds 
        to the GDP (float) for that year. Skips years with missing values.
    """
    plot_values = []
    for year in gdpdata.keys():
        gdp = gdpdata[year]
        if year.isdigit() and gdp != '' and gdpinfo["min_year"] <= int(year) <= gdpinfo["max_year"]:
            aux_tuple = (int(year),float(gdp))
            plot_values.append(aux_tuple)
    return plot_values

def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
        gdpinfo - dictionary with information of the GDP data
        country_list - list of country names
    Output:
        Returns a dictionary where the keys are the countries in country_list, 
        and the corresponding values are a list of yearly GDP data. If a 
        country is not included in the GDP data file, such a country is 
        still included in the dictionary, but the corresponding value is an empty list.
    """
    gdp_data = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"], 
                                       gdpinfo["separator"], gdpinfo["quote"])
    yearly_gdp_by_country = {}
    for country in country_list:
        if country in gdp_data:
            yearly_data = {}
            for key in gdp_data[country].keys():
                if key.isdigit():
                    yearly_data[key] = gdp_data[country][key]
            sorted_yearly_data = dict(sorted(yearly_data.items(), 
                                             key = lambda item: int(item[0])))
            yearly_gdp_by_country[country] = build_plot_values(gdpinfo, sorted_yearly_data)
        else:
            yearly_gdp_by_country[country] = []
    return (yearly_gdp_by_country)

def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
        gdpinfo - dictionary with information of the GDP data
        country_list - list of country names
        plot_file - name used to save the plot file
    Outputs:
        Generates an SVG plot displaying yearly GDP data for each 
        country in the country_list, and saves the plot as plot_file.
    """
    yearly_gdp_data = build_plot_dict(gdpinfo, country_list)
    xyplot = pygal.XY(height = 400)
    xyplot.title = "Yearly GDP data by country"
    for country in country_list:
        if country in yearly_gdp_data and yearly_gdp_data[country] != []:
            xyplot.add(country, yearly_gdp_data[country])
    xyplot.render_to_file(plot_file)

gdpinfo = {
    "gdpfile": "proyect1/isp_gdp.csv",        # Name of the GDP CSV file
    "separator": ",",                # Separator character in CSV file
    "quote": '"',                    # Quote character in CSV file
    "min_year": 1960,                # Oldest year of GDP data in CSV file
    "max_year": 2016,                # Latest year of GDP data in CSV file
    "country_name": "Country Name",  # Country name field name
    "country_code": "Country Code"   # Country code field name
    }

country_list = ["United Kingdom", "United States", "Honduras"]

render_xy_plot(gdpinfo, country_list, "yearly_gdp_data_by_country.svg")
