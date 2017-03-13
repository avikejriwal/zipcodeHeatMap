import zipcode as zp
import pandas as pd
import gmplot
from pypostalcode import PostalCodeDatabase
from pyzipcode import ZipCodeDatabase

#parse the data into readable latitude/longitude
dat = pd.read_csv('insert data file here')

#parse appropriately
usCodes = dat[dat['Country'] == 'United States of America']
usCodes.dropna(subset = ['Zip'])
usCodes = usCodes['Zip']

#parse Canada data
canCodes = dat[dat['Country'] == 'Canada']
canCodes.dropna(subset=['Zip'])
canCodes = canCodes['Zip']

lat = []
lng = []
count = 0

zcdb = ZipCodeDatabase()

#not all US zipcodes are in the first library I used
for z in usCodes:
    r = z[:5]
    while len(r) < 5:
        r = '0' + r
    try:
        myZ = zp.isequal(str(r))
        myDict = myZ.to_dict()
        lat.append(myDict['lat'])
        lng.append(myDict['lon'])
    except:
        try:
            zC = zcdb[r]
            lat.append(zC.latitude)
            lng.append(zC.longitude)
        except:
            count +=1

pcdb = PostalCodeDatabase()

#parse Canada codes
for z in canCodes:
    r =  z[:3].upper()
    try:
        loc = pcdb[r]
        lat.append(loc.latitude)
        lng.append(loc.longitude)
    except:
        count +=1 
        
print count #number of misses; for a list of 500 records this is generally trivial

#plot on a Google Maps HTML page
gmap = gmplot.GoogleMapPlotter(39.0558, -84.311, 20)
gmap.heatmap(lat, lng)
gmap.draw('mymap.html')
