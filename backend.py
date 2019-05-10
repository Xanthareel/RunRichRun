# -*- coding: utf-8 -*-
"""
Created on Tue May  7 21:03:26 2019

@author: Richard Hardis, Senthil Kannan
"""

import folium
import json

import numpy as np
import pandas as pd

from openrouteservice import client, places
from shapely import wkt, geometry
from shapely.geometry.point import Point

api_key = '5b3ce3597851110001cf62485c6c7bacc60f42bab791280c6252271c'
clnt = client.Client(key=api_key)


#wkt_str = 'Polygon ((13.43926404 52.48961046, 13.42040115 52.49586382, 13.42541101 52.48808523, 13.42368155 52.48635829, 13.40788599 52.48886084, 13.40852944 52.487142, 13.40745989 52.48614988, 13.40439187 52.48499746, 13.40154731 52.48500125, 13.40038591 52.48373202, 13.39423818 52.4838664, 13.39425346 52.48577149, 13.38629096 52.48582648, 13.38626853 52.48486362, 13.3715694 52.48495055, 13.37402099 52.4851697, 13.37416365 52.48771105, 13.37353615 52.48798191, 13.37539925 52.489432, 13.37643416 52.49167597, 13.36821531 52.49333093, 13.36952826 52.49886974, 13.37360623 52.50416333, 13.37497726 52.50337776, 13.37764916 52.5079675, 13.37893813 52.50693045, 13.39923153 52.50807711, 13.40022883 52.50938108, 13.40443425 52.50777471, 13.4052848 52.50821063, 13.40802944 52.50618019, 13.40997081 52.50692569, 13.41152096 52.50489127, 13.41407284 52.50403794, 13.41490921 52.50491634, 13.41760145 52.50417013, 13.41943091 52.50564912, 13.4230412 52.50498109, 13.42720031 52.50566607, 13.42940229 52.50857222, 13.45335235 52.49752496, 13.45090795 52.49710803, 13.44765912 52.49472124, 13.44497623 52.49442276, 13.43926404 52.48961046))'
#
#aoi_geom = wkt.loads(wkt_str) # load geometry from WKT string

aoi_geom = Point(13.4,52.4).buffer(0.015) #create a circle
print("Area: ", aoi_geom.area,"\nType: ",type(aoi_geom)) #check area
print("\nCoordinates: \n\n", list(aoi_geom.exterior.coords)) #check coordinates

aoi_coords = list(aoi_geom.exterior.coords) # get coords from exterior ring
aoi_coords = [(y,x) for x,y in aoi_coords] # swap (x,y) to (y,x). Really leaflet?!
aoi_centroid = aoi_geom.centroid # Kreuzberg center for map center

aoi_json = geometry.mapping(geometry.shape(aoi_geom))
query = {'request': 'pois',
        'geojson': aoi_json,
        'filter_category_ids': [569],
        'sortby': 'distance'}
pubs = clnt.places(**query)['features'] # Perform the actual request and get inner json

# Amount of pubs in Kreuzberg
print("\nAmount of pubs: {}".format(len(pubs)))
print(pubs[0])




map_hooray = folium.Map(location=[48, 1],
                        tiles='Stamen Terrain',
                        zoom_start = 11)

folium.Circle([48, 1],
                    radius=6000,
                    popup='Trial Marker',
                    color='blue',
                    ).add_to(map_hooray)


map_hooray.save('Map_trial.html')