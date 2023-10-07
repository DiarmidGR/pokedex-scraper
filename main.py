import requests
import pandas as pd
import json
from bs4 import BeautifulSoup


def main():
    #input_url = 'https://pokemondb.net/pokedex/game/black-white'
    input_url = 'https://pokemondb.net/pokedex'

    response = requests.get(input_url)

    if response.status_code == 200:
        html_content = response.text
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Initialize an empty set to store unique links
        unique_links = set()

        # Find all anchor elements with href containing '/pokedex/game/'
        game_links = soup.find_all('a', href=lambda href: href and '/game/' in href)

        # Extract and add unique links to the set
        for link in game_links:
            href = link.get('href')
            unique_links.add('https://pokemondb.net' + href)

        collection = []
        # Scrape each link and append data to main collection
        for link in unique_links:
            game = link
            if len(link.split('/game/')) == 2:
                game = link.split('/game/')[1]
            data = {
                "game": game,
                "pokedex": scrape_game(link),
            }
            collection.append(data)
        export_json(collection, "pokedex_data.json")


def export_json(data_input, name_output):
    with open(name_output, "w") as write:
        json.dump(data_input, write)
        print(f"Json file '{name_output}' has been created.")


def scrape_game(input_url):
    response = requests.get(input_url)

    # Initialize a list to store the data
    collection = []

    if response.status_code == 200:
        html_content = response.text
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all div elements with class "infocard"
        infocard_spans = soup.find_all('span', class_='infocard-lg-data')

        # Iterate through the infocard_data_spans list and extract Name and Number
        for span in infocard_spans:
            # Find the Name (inside the <a> element with class "ent-name")
            name = span.find('a', class_='ent-name').text.strip()

            # Find the Number (inside the first <small> element)
            number = span.find('small').text.strip()

            # Create a dictionary with the Name and Number
            data = {
                "name": name,
                "number": number.replace('#', ''),
            }

            # Append the data to the collection
            collection.append(data)
    return collection


main()
