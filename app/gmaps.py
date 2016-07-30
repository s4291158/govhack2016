import googlemaps


def query_place(place):
    gmaps = googlemaps.Client(key='AIzaSyC64CU6Y2yihOLW9IIJq_I7IHhLpf483Rc')

    geocode_result = gmaps.places(place)

    lat_lng, lat_lng_bounds = None, None

    try:
        lat_lng = geocode_result['results'][0]['geometry']['location']
    except Exception as e:
        print(e)
        pass

    try:
        lat_lng_bounds = geocode_result['results'][0]['geometry']['viewport']
    except Exception as e:
        pass

    return lat_lng, lat_lng_bounds
