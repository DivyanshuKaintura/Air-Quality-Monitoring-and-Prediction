import requests
import pandas as pd
import joblib 
from geopy.geocoders import Nominatim

# Replace with your own OpenWeatherMap API key
API_KEY = "ac4b58880597e40aae5eac9565cac52d"
# CITY = "Delhi"
API_URL = f"http://api.openweathermap.org/data/2.5/air_pollution"

def get_air_quality(lat, lon):
    """Fetch air quality data from OpenWeatherMap API based on latitude and longitude."""
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    
    # Check if the response status is OK (200)
    if response.status_code == 200:
        try:
            # Try to parse the JSON response
            data = response.json()
            return data
        except ValueError as e:
            # Print error if JSON decoding fails
            print("Error: Unable to decode JSON response")
            print("Raw response content:", response.text)
            return None
    else:
        print(f"Error: Received status code {response.status_code}")
        print("Response content:", response.text)
        return None

def get_lat_long(city_name):
    geolocator = Nominatim(user_agent="geo")
    location = geolocator.geocode(city_name)
    
    if location:
        return (location.latitude, location.longitude)
    else:
        return "City not found"

def main():
    # Example coordinates for Delhi (You can use the Geocoding API to get coordinates of any city)
    latitude = 28.6139
    longitude = 77.2090
    
    CITY = input("Enter city ")
    latitude, longitude = get_lat_long(CITY)
    
    # Fetch air quality data
    air_quality_data = get_air_quality(latitude, longitude)
    
    if air_quality_data:
        # Extract relevant data from the API response
        air_quality_index = air_quality_data['list'][0]['main']['aqi']
        components = air_quality_data['list'][0]['components']
        
        print(f"Air Quality Index (AQI) in {CITY}: {air_quality_index}")
        print("Pollutants levels:")
        print(f"CO: {components['co']} μg/m³")
        print(f"NO: {components['no']} μg/m³")
        print(f"NO2: {components['no2']} μg/m³")
        print(f"O3: {components['o3']} μg/m³")
        print(f"SO2: {components['so2']} μg/m³")
        print(f"PM2.5: {components['pm2_5']} μg/m³")
        print(f"PM10: {components['pm10']} μg/m³")
        print(f"NH3: {components['nh3']} μg/m³")
        
        model = joblib.load('RN_model.pkl')
        test = [components['pm2_5'], components['no'],
                components['no2'], 32, components['co'],
                components['so2'], components['o3'],
                3.4, 9.3, air_quality_index*100]
        
        test = [float(x) for x in test]
        prediction = model.predict([test])
        quality = prediction[0]
        print("Prediction = ", quality)
        
        moderate = "1. If you're part of a sensitive group (asthmatics, elderly, or those with heart/lung conditions), avoid prolonged outdoor activities like running or heavy exercise. \n2. For others, you can still exercise outdoors but pay attention to how you are feeling. If you feel short of breath, slow down or take breaks. \n3. Consider using an air purifier with a HEPA filter indoors, especially in bedrooms and living spaces. \n4. Avoid activities that may worsen indoor air quality (e.g., smoking, burning candles, cooking without proper ventilation)."
        satisfactory = "1. Enjoy outdoor exercise and activities freely, as the air quality is safe for everyone, including sensitive groups like children and the elderly. \n2. Use public transport, walk, or bike to reduce vehicle emissions and contribute to maintaining the good air quality. \n3. Encourage others to adopt eco-friendly habits like reducing waste and using energy-efficient appliances."
        poor = "1. Avoid strenuous activities like running or cycling outdoors. If you need to go outside, try to stay indoors during peak pollution hours (like rush hours or times of heavy traffic). \n2. Wear a mask, preferably an N95 or P100, to reduce inhalation of particulate matter. Use air purifiers with HEPA filters indoors to maintain clean indoor air. \n3. Shut windows and doors to prevent polluted air from entering your home. If necessary, use air conditioning on recirculation mode to cool the air without pulling in outdoor pollutants."
        very_poor = "1. Avoid going outside, especially for prolonged or strenuous activities. Keep children, elderly, and individuals with respiratory conditions indoors. \n2. Ensure you have a high-quality air purifier with a HEPA filter to clean indoor air. Keep it running in the rooms you use most, like bedrooms and living areas. \n3. If you must go outside, wear a properly fitted N95 or P100 mask to protect yourself from inhaling harmful particles. Limit the time spent outdoors and avoid heavy exertion."
        good = "1. Engage in outdoor exercise, sports, or any other activities without concern, as the air poses no health risks. \n2. Practice eco-friendly habits like using public transportation, carpooling, and conserving energy to help maintain the good air quality. \n3. Stay informed about the air quality in your area to be prepared if conditions worsen due to weather or pollution."
        severe = "1. Refrain from going outside unless absolutely necessary. Stay in well-ventilated indoor spaces with filtered air, and avoid strenuous activities even indoors if possible.\n2. Run air purifiers with HEPA filters continuously to reduce indoor pollution. Keep windows and doors tightly closed to prevent polluted air from entering your home. Consider sealing gaps with weather strips. \n3. If you must go outside for essential activities, wear a certified N95 or P100 mask to reduce exposure to harmful particulates and pollutants. Limit your time outdoors as much as possible."
        
        measures = {'Moderate': moderate,
            'Satisfactory': satisfactory,
            'Poor': poor,
            'Very Poor': very_poor,
            'Good': good,
            'Severe': severe}
        
        print(f"\n Air quality of {CITY} is ", quality)
        print("Follow the measure provided below: \n\n", measures[quality])
        
        
        
        
    else:
        print("Failed to retrieve data")
        
    
    

if __name__ == "__main__":
    main()
