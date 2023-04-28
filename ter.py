def main(country, city, api_key):
    import requests
    import os
    import json
    from datetime import datetime, timedelta
    import matplotlib.pyplot as plt
    print('hi')

    cwd = os.getcwd()
    save_dir = os.path.join(cwd, 'static')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    # Convert city to latitude and longitude using OpenCage Geocoding API
    url = f'https://api.opencagedata.com/geocode/v1/json?q={city},{country}&key=f6f613b4fd3f475c85718a61a97980b3'
    response = requests.get(url)
    data = json.loads(response.text)
    if data['results']:
        lat = data['results'][0]['geometry']['lat']
        lon = data['results'][0]['geometry']['lng']
    else:
        print(f'Could not find latitude and longitude for {city}, {country}')
        return
    api_key = '547e4e1e7c99ee57e3ed55b51a3085a2'

    exclude = "minutely,hourly,alerts"
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid={api_key}&units=metric'

    # Make a request to the API endpoint
    response = requests.get(url)

    # Parse the JSON response
    data = json.loads(response.text)

    # Extract the daily forecast data for the next 7 days
    forecast_data = data['daily'][:7]

    # Extract the temperature and date data for each forecast
    dates = []
    temps = []
    for forecast in forecast_data:
        forecast_date = datetime.utcfromtimestamp(forecast['dt']).strftime('%Y-%m-%d')
        forecast_temp = forecast['temp']['day']
        dates.append(forecast_date)
        temps.append(forecast_temp)

    # Plot the temperature forecast on a graph
    plt.figure(figsize=(10, 6))  # Set the size of the plot to be 10 inches wide and 6 inches high
    plt.plot(dates, temps)
    plt.title('7-Day Temperature Forecast')
    plt.xlabel('Date')
    plt.ylabel('Temperature (Celsius)')

    # Set the x-axis ticks to be every other day starting from the first date
    first_date = datetime.strptime(dates[0], '%Y-%m-%d')
    last_date = datetime.strptime(dates[-1], '%Y-%m-%d')
    ticks = [d.strftime('%Y-%m-%d') for d in [first_date + timedelta(days=x) for x in range(0, (last_date-first_date).days+1, 2)]]
    plt.xticks(ticks)

    # Save the plot as a PNG image
    plt.savefig(os.path.join(save_dir, 'temperature_forecast.png'))
    plt.clf()
