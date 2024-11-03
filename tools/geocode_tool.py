from opencage.geocoder import OpenCageGeocode
import os

geocoder = OpenCageGeocode(os.getenv('OPENCAGE_API_KEY'))

def get_country_code(city_name):
    result = geocoder.geocode(city_name)
    return result[0]['components'].get('country_code').upper() if result else None
