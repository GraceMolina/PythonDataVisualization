
"""
merge CSV files that contain cancer risk data from the United States
"""

import csv

def read_csv_as_list_dict(filename, separator, quote):
    """
    Takes a CSV file, a separator, and a quote and returns the data within 
    the file as a list of dictionaries.
    """
    table = []
    with open(filename, "rt", newline = '', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter = separator, 
                                   quotechar = quote)
        for row in csvreader:
            table.append(row)
        return table

def write_csv_file(csv_table, file_name):
    """
    Given a nested list csv_table and a string name file_name, 
    write the fields in the csv_table into a comma-separated CSV file with the name file_name.
    """
    with open(file_name, 'w', newline = '') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter = ',')
        for row in csv_table:
            csvwriter.writerow(row)

def make_dict(table, key_col):
    """
    Inputs: 
        table - list of lists. Each list represents a row in table.
        key_col - integer indexing the column whose values will be used to create keys
    Outpus:
        This function returns a dictionary where each key-value pair represents a row 
        from table. Each row is transformed into a key-value pair in which the key is 
        the value from the column specified by key-col, and the corresponding value is 
        a list of the remaining elements in that row.
    """
    list_to_dict = {}
    for row in table:
        row_copy = row.copy()
        del row_copy[key_col]
        list_to_dict[row[key_col]] = row_copy
    return list_to_dict

CANCER_RISK_FIPS_COL = 2 # index for column with FIPS codes in the cancer risk dataset
CENTER_FIPS_COL = 0 # index for column with FIPS codes in the county center dataset

def merge_csv_files(cancer_csv_file, center_csv_file, joined_csv_file):
    """
    Inputs:
        cancer_csv_file - the name of the CSV file containing cancer-risk data. 
        center_csv_file - the name of the CSV file with each county's center. 
        joined_csv_file - the name to save the merged dataset.
    Output:
        Merges both CSV files using the shared FIPS codes. Saves the merged dataset 
        as a CSV file named joined_csv_file. The saved file contains the following 
        columns: State, County name, FIPS code, Population, Cancer risk, Horizontal 
        coordinate of county center (with respect to the USA SVG map), Vertical 
        coordinate of county center (with respect to the USA SVG map)
    """
    cancer_risk = read_csv_as_list_dict(cancer_csv_file, ',', '"')
    county_centers = read_csv_as_list_dict(center_csv_file, ',', '"')
    county_centers_dict = make_dict(county_centers, CENTER_FIPS_COL)
    merged_data = []
    merged_data.append(['State', 'County name', 'FIPS code', 'Population', 'Cancer risk', 
                   'Horizontal coordinate of county center (with respect to the USA SVG map)', 
                   'Vertical coordinate of county center (with respect to the USA SVG map)'])
    for row in cancer_risk:
        if row[CANCER_RISK_FIPS_COL] in county_centers_dict.keys():
            row.append(county_centers_dict[row[CANCER_RISK_FIPS_COL]][0])
            row.append(county_centers_dict[row[CANCER_RISK_FIPS_COL]][1])
            merged_data.append(row)
        else:
            print("Warning: County code", row[CANCER_RISK_FIPS_COL], "in cancer risk dataset " \
            "not found in county center dataset.")
    write_csv_file(merged_data, joined_csv_file)
    cancer_risk_dict = make_dict(cancer_risk, CANCER_RISK_FIPS_COL)
    for row in county_centers:
        if row[CENTER_FIPS_COL] in cancer_risk_dict.keys():
            pass
        else:
            print("Warning: County code", row[CENTER_FIPS_COL], "in county center dataset " \
            "not found in cancer risk dataset.")

merge_csv_files("cancer_risk_trimmed_solution.csv", "USA_Counties_with_FIPS_and_centers.csv", "merged_dataset.csv")
