import time

def get_weather(location):
    """
    Simulates fetching weather information for a given location.
    Args:
        location (str): The city or area to get weather for.
    Returns:
        dict: A dictionary with 'status' and 'result' of the operation.
    """
    print(f"[Tool: Weather] Fetching weather for {location}...")
    time.sleep(1.5) # Simulate API call delay

    # Dummy weather data for demonstration
    weather_data = {
        "karachi": "Sunny with a chance of light breeze. Temperature: 32°C.",
        "lahore": "Partly cloudy. Temperature: 30°C.",
        "islamabad": "Clear skies. Temperature: 28°C.",
        "new york": "Cloudy with occasional rain. Temperature: 15°C.",
        "london": "Overcast and chilly. Temperature: 10°C."
    }

    normalized_location = location.lower()
    info = weather_data.get(normalized_location)

    if info:
        print(f"[Tool: Weather] Weather info found for {location}.")
        return {"status": "success", "result": f"The weather in {location.title()} is: {info}"}
    else:
        print(f"[Tool: Weather] Weather data not available for {location}.")
        return {"status": "failure", "result": f"Sorry, I don't have weather data for {location.title()}."}

if __name__ == '__main__':
    # Simple test for the tool
    print(get_weather("Karachi"))
    print(get_weather("New York"))
    print(get_weather("Unknown City"))