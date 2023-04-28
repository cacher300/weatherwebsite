# Import necessary modules
import requests
import json
from ter import main
from flask import Flask, render_template, request
import pycountry

# Enter your API key here
api_key = '0e963c16a12edb73fef00ba1191d480e'

# Base URL for OpenWeatherMap API
url = 'http://api.openweathermap.org/data/3.0/weather'

# Create a new Flask instance
app = Flask(__name__)

# Define a route for the home page that accepts GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        # Get form data submitted by user
        country = request.form['country']
        city = request.form['city']

        # Call main function from the "ter" module with the form data as arguments
        main(country, city, api_key)

        x = 0
        # Use pycountry module to get the 2-letter ISO country code from the country name
        country_code = pycountry.countries.get(name=country).alpha_2
        country_code = country_code.lower()

        # Use the NewsAPI to get top business headlines from the specified country
        url = f"https://newsapi.org/v2/top-headlines?country={country_code}&category=business&apiKey=9501276c8cec4ec3af0a411eb87d5b44"
        response = requests.get(url)

        data = json.loads(response.text)
        article_list = []
        # Loop through the articles and add the titles and urls as a tuple to the list
        for article in data['articles']:
            if x < 5:
                title = article['title']
                url = article['url']

                article_list.append((title, url))
                x += 1

        # Render the "forecast.html" template with the top headlines list
        return render_template('forecast.html', headlines=article_list)

    # If no form data was submitted, render the "index.html" template with the form
    return render_template('index.html')

# Start the Flask application if this script is being run directly
if __name__ == '__main__':
    app.run(debug=True)
