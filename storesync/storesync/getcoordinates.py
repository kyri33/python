from geopy import geocoders

def get_coordinates(inputAddress):
    nono = ['and','No.', ',',]
    for no in nono:
        inputAddress = inputAddress.replace(no , '+')

    
    inputAddress = inputAddress.replace('Cnr Conradie and Strand Streets' , 'Norkem Park High School')
    inputAddress = inputAddress.replace('Cnr Main & Kelly Roads' , 'Norkem Park High School')
    g = geocoders.GoogleV3(api_key='AIzaSyDCwqJ1BMQx6tcNRliQwZFWhweQVK-vviQ')
    location = g.geocode(inputAddress, timeout=10)
    coordinate = {'latitude': 0, 'longitude':0}
    
    coordinate['latitude'] = location.latitude
    coordinate['longitude'] = location.longitude

    if location == "":
        coordinate = {'latitude': 0, 'longitude':0}
    else:
        return coordinate