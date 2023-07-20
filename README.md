# MATLAB AND PYTHON

# WHAT DOES THE SCRIPT DO?

It uses the information from the excel sheet as a input (see Routing_GitHub.xlsx) to create a routing list. It takes into account the distance as well as the load carried by the vehicle. This can be changed by inputting desired value in line #35 of the script (change the value of variable 'limit_case'). The default value chosen was 800 cases. 

If the load of the truck exceeds the limit (limit_case), a route is created. In case the load is not perfectly allocated (as in current load is 790 and the next stop has 150 cases), the script splits it accordingly and updates the values. The program runs until all the values under the 'Cases' column become 0 in the table.

A bit of data cleaning is also done using MATLAB to achieve required result.

PYTHON SCRIPT (NEW):

The functionality of the script remains except for two changes.

Change 1: The script takes in a .csv file instead of an Excel file. So, while running the Python script, convert the .xlsx file to a .csv file wherever a file is read in the script.

Change 2: The script also considers negative values under the "Cases" column. The negative number of cases represents a pickup rather than a delivery at that stop.

# BEFORE RUNNING THE SCRIPT, READ THIS:

MATLAB:
CHANGE THE FILE PATH in line #29.

The script can run only when the excel file (Routing_GitHub.xlsx) is used. The values and the content of the table can be changed, but the name of the columns should not be changed if the script is to run as it is. If the column names are changed the respective table variables need to be changed in the script.

The origin coordinate has to be inputted in the script. Currently, it contains a dummy value (Line 98 of the MATLAB script.)

The current Excel sheet does not contain any latitudes and longitudes and needs to be filled in by the user. For the output files, actual latitudes and longitudes were used but have been removed for confidentiality.

The script uses Latitude and Longitude to calculate the distance between two places. But the in-built function used for this calculated the straight line distance, not the distance between places by road.

# ABOUT OUTPUT FILE:
MATLAB:
An output file has also been posted. All the distances are in kms.

