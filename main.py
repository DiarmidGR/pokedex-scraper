import requests
import pandas as pd
import json
from bs4 import BeautifulSoup


def main():
    input_url = 'https://pokemondb.net/pokedex/game/black-white'

    response = requests.get(input_url)

    if response.status_code == 200:
        html_content = response.text
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all div elements with class "infocard"
        infocard_spans = soup.find_all('span', class_='infocard-lg-data')

        # Initialize a list to store the data
        collection = []

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

        export_json(collection, "pokemon_red.json")

        # Create a Pandas DataFrame from the list of data
        df = pd.DataFrame(collection)

        # Create an Excel writer object
        excel_writer = pd.ExcelWriter('pokemon_data.xlsx', engine='openpyxl')

        # Add the DataFrame to the Excel writer object
        df.to_excel(excel_writer, index=False, sheet_name='Pokemon Data')

        # Get the workbook and worksheet objects
        workbook = excel_writer.book
        worksheet = excel_writer.sheets['Pokemon Data']

        # Save the Excel file
        excel_writer.close()

        print("Excel file 'pokemon_data.xlsx' has been created.")

    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)


def export_json(data_input, name_output):
    with open(name_output, "w") as write:
        json.dump(data_input, write)
        print(f"Json file '{name_output}' has been created.")


main()
