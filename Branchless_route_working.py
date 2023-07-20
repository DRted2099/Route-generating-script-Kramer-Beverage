import csv
import math as m

''' Function to calculate distance between 2 points using lat and long co-ordinates '''

def distance(lat1, lat2, lon1, lon2):

	'''Input should be in degrees
	   
	   Convert to radians'''

	lat1 = m.radians(lat1)
	lon1 = m.radians(lon1)
	lat2 = m.radians(lat2)
	lon2 = m.radians(lon2)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	'''Haversine formula '''
	a = m.sin(dlat/2)**2 + m.cos(lat1) * m.cos(lat2) * m.sin(dlon/2)**2

	c = 2 * m.asin(m.sqrt(a))

	'''Radius of earth in kilometers. Use 3956 for miles '''
	r = 6371

	return c*r

''' Function to split cases : split_cases(int1, int2, int3)

	int1 : The number of cases to be delivered (obtained from main table)
	int2 : A placeholder variable that keeps track of the number of cases that are on the truck currently
	int3 : The maximum cases the truck can hold
	
	Its also used to check a condition: casesToBeDel > 0 and casesToBeDel + cases_on_truck > case_limit
	
	casesToBeDel > 0: This condition is used as there are negative values under the cases column in the main table. These negative
					   values denote the number of cases to be picked up from customer 

	casesToBeDel + cases_on_truck > case_limit : Used to check if the cases that are going to be added to the truck exceed the limit

	If condition is met then the cases can't fit in the truck and need to be split so the 
	function gives 1) The number of cases that can be put in the truck
				   2) The number of cases left over which can be updated to the main table

   If the condition is not met it returns the 1) "casesToBeDel" and
   											  2) "0"             		 '''

def split_cases(casesToBeDel, cases_on_truck, case_limit):

	condition = casesToBeDel > 0 and casesToBeDel + cases_on_truck > case_limit

	cases_fit = case_limit - cases_on_truck
	cases_left = abs(cases_fit - casesToBeDel)

	return (cases_fit, cases_left) *condition \
		+  (casesToBeDel, 0) * (not condition)

		
''' Initializing variables and empty lists to store distances and indices '''

dist = list()			# To store the distance between stops
ind_route = list()		# To store the order of indices for the route ie; order of delivery
next_truck = list()		# To store indices of when the truck changes
done_places = set()		# To store indices of all locations that have been assigned trucks
cases = list()			# List for cases for each stop
cases_ph = 0      # placeholder to keep track of cases on truck
counter = 0		  # To keep track when a truck changes ie; when cases on truck exceed its limit
case_limit = 800  # Maximum cases a truck can fit

kramer = [39.616910, -74.818310] #Origin co-ordinates

'''Reading lat and lon data from csv file '''

cord_cases = {'Index': [], 'Latitude': [], 'Longitude': [], 'Cases': [] }

with open('Sales_order.csv','r', encoding='latin-1') as csv_file:
	
	csv_reader = csv.DictReader(csv_file)

	for index,line in enumerate(csv_reader):

		cord_cases['Index'].append(index)
		cord_cases['Latitude'].append(line['Latitude'])
		cord_cases['Longitude'].append(line['Longitude'])
		cord_cases['Cases'].append(line['Cases'])

cases_orig = [int(ele) for ele in cord_cases['Cases']]       # List of all cases for all stops as in the main table
latitude = [float(ele) for ele in cord_cases['Latitude']]	 # List of all latitudes for all stops as in the main table
longitude = [float(ele) for ele in cord_cases['Longitude']]	 # List of all longitudes for all stops as in the main table
index_orig = [int(ele) for ele in cord_cases['Index']]		 # List of all indices for all stops as in the main table

# Plots distances between origin and points of interest (POI) with POI's index

while len(done_places) < index_orig[-1] + 1: 

	counter  += 1 
	
	if cases_ph == 0 or cases_ph >= case_limit:

		cases_ph = 0

		# Finds distances between origin and all POI's and does not repeat if the cases for POI is 0 

		dist_origin = [(distance(kramer[0], latitude[ind], kramer[1], longitude[ind]), index_orig[ind]) \
			for ind in range(0, index_orig[-1] + 1) if ind not in done_places]

		# Storing min distance and its index from above calculated distances 

		dist.append(min(dist_origin)[0])
		ind_route.append(min(dist_origin)[1])

		# Splits cases and updates the 'cases' list and the variable 'cases_ph'

		splitCase = split_cases(cases_orig[ind_route[-1]],cases_ph,case_limit)

		cases_orig[ind_route[-1]] = splitCase[1]
		
		cases.append(splitCase[0])


		if splitCase[1] > 0:

			next_truck.append(counter) 


		if splitCase[1] == 0:

			done_places.add(index_orig[ind_route[-1]])
		
		
		cases_ph = (cases_ph + cases[-1]) * (splitCase[0] >= 0) + (cases_ph + 0) * (splitCase[0] < 0)	

	else:	


		#Finds distances between POI-1 and all POI's and does not repeat if the cases for POI is 0


		dist_p2p = [(distance(latitude[ind_route[-1]], latitude[ind], longitude[ind_route[-1]], longitude[ind]), index_orig[ind]) \
			for ind in range(0, index_orig[-1] + 1) if ind not in done_places]
	
		# Same as If condition

		dist.append(min(dist_p2p)[0])
		ind_route.append(min(dist_p2p)[1])


		splitCase = split_cases(cases_orig[ind_route[-1]],cases_ph,case_limit)

		cases_orig[ind_route[-1]] = splitCase[1]
		
		cases.append(splitCase[0])

		if splitCase[1] > 0:

			next_truck.append(counter) 


		if splitCase[1] == 0:

			done_places.add(index_orig[ind_route[-1]])
		
		
		cases_ph = (cases_ph + cases[-1]) * (splitCase[0] >= 0) + (cases_ph + 0) * (splitCase[0] < 0)



# Extracting all the names from the main table 

with open('Sales_order.csv','r', encoding = 'latin-1') as csv_file:
	
	csv_reader = csv.DictReader(csv_file)

	names = [[line['ShipCity'], line['CusName']] for line in csv_reader]


# Sorting names according to the route order

names_order = [names[index] for index in ind_route]

# Creating a dictionary to store all the list contents extracted from the while loop

routesheet = {'Customer Name':[], 'Ship City':[], 'Distance':[], 'Cases':[], 'Next Truck':[]}

for i in range(0,len(ind_route)):

	routesheet['Ship City'].append(names_order[i][0])
	routesheet['Customer Name'].append(names_order[i][1])
	routesheet['Distance'].append(str(dist[i]))
	routesheet['Cases'].append(str(cases[i]))

	if i in next_truck:

		routesheet['Next Truck'].append('Next Truck')

	else:

		routesheet['Next Truck'].append('')

# Creating a csv file to generate the route sheet

with open('route_sheet1.csv', 'w') as r_s:

	fieldnames = ['Customer_Name', 'Ship City', 'Distance', 'Cases', 'Next Truck']

	csv_writer = csv.writer(r_s)

	csv_writer.writerow(fieldnames)

	r = zip(*routesheet.values())

	for index, line in enumerate(r):
		
		csv_writer.writerow(line)


