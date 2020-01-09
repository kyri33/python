from geopy import geocoders

def get_coordinates(inputAddress):
    nono = ['and','No.', ',',]
    for no in nono:
        inputAddress = inputAddress.replace(no , '+')

    
    inputAddress = inputAddress.replace('Cnr Conradie and Strand Streets' , 'Norkem Park High School')
    inputAddress = inputAddress.replace('Cnr Main & Kelly Roads' , 'Norkem Park High School')
    
    try:
        location = g.geocode(inputAddress, timeout=10)
    except:
        return {'latitude': 0, 'longitude': 0}

    coordinate = {'latitude': 0, 'longitude':0}
    
    if location == "" or location == None:
        coordinate = {'latitude': 0, 'longitude':0}
    else:
        coordinate['latitude'] = location.latitude
        coordinate['longitude'] = location.longitude
    
    return coordinate

    