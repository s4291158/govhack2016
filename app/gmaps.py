import googlemaps

def query_place(place):
    gmaps = googlemaps.Client(key='AIzaSyAygZ1T2_ZBZ1UnJyv68BEL1riDsnQW_-w')
    geocode_result = gmaps.geocode(place)[0]

    postal_code = geocode_result['address_components'][-1]['long_name']
    lat_lng = geocode_result['geometry']['location']

    my_dict = {'postal': postal_code, **lat_lng}

    return my_dict