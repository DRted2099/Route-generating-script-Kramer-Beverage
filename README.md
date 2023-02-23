# Routing_MATLAB

WHAT DOES THE SCRIPT DO?
It uses the information from the excel sheet (see Routing_GitHub.xlsx) to create a routing list. It takes into account the distance as well as the load carried by the vehicle. This can be changed by inputting desired value in line #35 of the script (change the value of variable 'limit_case'). A bit of data cleaning is also done using MATLAB to achieve required result.


BEFORE RUNNING SCRIPT READ THIS:
The script can run only when the excel file posted is used. The values and the size of the table can be changed, but the name of the columns should not be changed if the cose is to run as it is. If the column names are changed the respective table variables need to be changed in the script

The origin co-ordinate has to be inputted in the script. Currntly it contains a dummy value (Line 98 of the MATLAB script.)

The current excel sheet does not contain any latitudes and longitudes and need to be filled in by the user

The script uses Latitude and Longitude to calculate the distance between two places. But the in-built function used for this calculated the straight line distance and not the actual distance between places by road.

OUTPUT FILE
An output file has also been posted on the page. 

