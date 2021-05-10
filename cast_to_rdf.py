import pandas as pd 
import sys
import os
import itertools


def append_namespace():
	print('@prefix :<http://www.semanticweb.org/johnvoul/ontologies/2020/6/transport#> .')
	print('@prefix owl:<http://www.w3.org/2002/07/owl#> .')
	print('@prefix rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> .')
	print('@prefix xml:<http://www.w3.org/XML/1998/namespace> .')
	print('@prefix xsd:<http://www.w3.org/2001/XMLSchema#> .') 
	print('@prefix rdfs:<http://www.w3.org/2000/01/rdf-schema#> .')
	print('@prefix vrdf:<http://www.openlinksw.com/schemas/virtrdf#> .')
	print()



with open("routes.ttl", "a", encoding='utf-8') as f:
	sys.stdout = f
	try:
		routes = pd.read_csv("routes.txt", encoding='utf-8')
	except:
		routes = pd.read_csv("routes.csv")
	routes.fillna("UNK", inplace=True)
	routes.head(200)
	append_namespace()
	for index, row in routes.iterrows():
		name = row["route_short_name"]
		long_name = row["route_long_name"]
		if(row["route_type"] == 900): #Tram
			print(":r{} rdf:type owl:NamedIndividual .".format(name))
			print(":r{} rdf:type :Tram .".format(name))
			print(":r{} :belongsAgency :OASA .".format(name))
			print(":r{} :Name \"{}\" .".format(name, long_name))
			print()
		if(row["route_type"] == 1): #Metro
			print(":r{} rdf:type owl:NamedIndividual .".format(name))
			print(":r{} rdf:type :Metro .".format(name))
			print(":r{} :belongsAgency :OASA .".format(name))
			print(":r{} :Name \"{}\" .".format(name, long_name))
			print()
		if(row["route_type"] == 800): #Trolley
			print(":r{} rdf:type owl:NamedIndividual .".format(name))
			print(":r{} rdf:type :Trolley .".format(name))
			print(":r{} :belongsAgency :OASA .".format(name))
			print(":r{} :Name \"{}\" .".format(name,long_name))
			print()
		if(row["route_type"] == 3): #Bus
			print(":r{} rdf:type owl:NamedIndividual .".format(name))
			print(":r{} rdf:type :Bus .".format(name))
			print(":r{} :belongsAgency :OASA .".format(name))
			print(":r{} :Name \"{}\" .".format(name,long_name))
			print()


with open("trips.ttl", "a", encoding='utf-8') as f:
	sys.stdout = f
	try:
		trips = pd.read_csv("trips.txt", encoding='utf-8')
	except:
		trips = pd.read_csv("trips.csv", encoding = 'utf-8')
	trips.fillna("UNK", inplace=True)
	trips.head()
	append_namespace()
	for index, row in trips.iterrows():
	# for index, row in itertools.islice(trips.iterrows(), limit):
		route_id = row["route_id"].split("-")[0]
		trip_id = row["trip_id"].split("-")[0]
		name = row["trip_headsign"]
		print(":t{} rdf:type owl:NamedIndividual .".format(trip_id)) #vazoume ena "t"
		#mprosta apo ton arithmo gt alliws exei provlima to syntax
		print(":t{} rdf:type :Trips .".format(trip_id))
		print(":t{} :belongsAgency :OASA .".format(trip_id))
		print(":t{} :Name \"{}\" .".format(trip_id, name))
		print(":r{} :Serves :t{} .".format(route_id, trip_id))
		print()



with open("stops.ttl", "a",  encoding='utf-8') as f:
	sys.stdout = f
	try:
		stops = pd.read_csv("stops.txt", encoding='utf-8')
	except:
		stops = pd.read_csv("stops.csv",encoding='utf-8')
	stops.fillna("UNK", inplace=True)
	stops.head()
	append_namespace()
	for index, row in stops.iterrows():
		stop_id = row["stop_id"]
		name = row["stop_name"]
		description = row["stop_desc"]
		latitude = row["stop_lat"]
		longitude = row["stop_lon"]
		print(":s{} rdf:type owl:NamedIndividual .".format(stop_id))
		print(":s{} rdf:type :Station .".format(stop_id))
		print(":s{} :belongsAgency :OASA .".format(stop_id))
		print(":s{} :Coordinates \"POINT({} {})\"^^vrdf:Geometry ."
		.format(stop_id, latitude, longitude))
		print(":s{} :Name \"{}\" .".format(stop_id, name))
		print(":s{} :Description \"{}\" .".format(stop_id, description))
		print()


with open("stop_times.ttl", "a",  encoding='utf-8') as f:
	sys.stdout = f
	try:
		stop_times = pd.read_csv("stop_times.txt",encoding='utf-8')
	except:
		stop_times = pd.read_csv("stop_times.csv",encoding='utf-8')
	stop_times.fillna("UNK", inplace=True)
	stop_times.head()
	append_namespace()
	for index, row in stop_times.iterrows():
		# for index, row in itertools.islice(stop_times.iterrows(), limit):
		desc = row["trip_id"].split("-")
		trip_id = desc[0]
		desc = '-'.join(desc[2:len(desc) - 1])
		station_id = row["stop_id"]
		arrival = row["arrival_time"]
		departure = row["departure_time"]
		print(":As{} rdf:type owl:NamedIndividual .".format(index))
		print(":As{} rdf:type :StationArrival .".format(index))
		print(":As{} :belongsAgency :OASA .".format(index))
		print(":As{} :OnTime \"{}\" .".format(index, arrival))
		print(":As{} :Description \"{}\" .".format(index, desc))
		print(":As{} :hasStation :s{} .".format(index, station_id))
		print(":t{} :arrivesAt :As{} .".format(trip_id, index))
		print()
		print(":Ds{} rdf:type owl:NamedIndividual .".format(index))
		print(":Ds{} rdf:type :StationDeparture .".format(index))
		print(":Ds{} :belongsAgency :OASA .".format(index))
		print(":Ds{} :OnTime \"{}\" .".format(index, arrival))
		print(":Ds{} :Description \"{}\" .".format(index, desc))
		print(":Ds{} :hasStation :s{} .".format(index, station_id))
		print(":t{} :departsAt :Ds{} .".format(trip_id, index))
		print()
