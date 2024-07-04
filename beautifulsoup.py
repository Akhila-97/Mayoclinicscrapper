from bs4 import BeautifulSoup as bs
import requests

url = 'http://www.mayoclinic.org/diseases-conditions/index?letter=a'
r = requests.get(url)
soup = bs(r.text, "html.parser")

# Find the div containing conditions starting with "A"
div_a_conditions = soup.find("div", class_="cmp-azresults cmp-azresults-from-model")
print(div_a_conditions)

import string
from bs4 import BeautifulSoup
import requests
import json

# Base URL
base_url = 'http://www.mayoclinic.org/diseases-conditions/index?letter='


all_conditions_data = []


for letter in string.ascii_uppercase:
    print(f"Fetching conditions for letter: {letter}")
    url = f"{base_url}{letter}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    div_a_conditions = soup.find("div", class_="cmp-azresults cmp-azresults-from-model")


    if div_a_conditions:

        conditions_list = div_a_conditions.find_all("li")

        for condition in conditions_list:

            disease_name = condition.text.strip()
            disease_link = condition.find("a")["href"] if condition.find("a") else None

            print(f"Disease: {disease_name}")
            print(f"Link: {disease_link}")

            if disease_link:

                disease_url = f"{disease_link}"
                disease_page = requests.get(disease_url)
                disease_soup = BeautifulSoup(disease_page.content, 'html.parser')

                # Find symptoms section
                symptoms_section = disease_soup.find("h2", text="Symptoms")
                if symptoms_section:
                    description = []

                    next_sibling = symptoms_section.find_next_sibling()
                    while next_sibling:
                        if next_sibling.name == "ul":
                            symptoms_list = next_sibling.find_all("li")
                            if symptoms_list:
                                for symptom in symptoms_list:
                                    description.append(symptom.text.strip())
                        elif next_sibling.name == "p":
                            description.append(next_sibling.text.strip())
                        next_sibling = next_sibling.find_next_sibling()


                    if not description:
                        description.append("Symptoms section does not contain <ul> or <p> tags.")

                else:
                    description = ["Symptoms section not found."]

                # Add data to the list
                all_conditions_data.append({
                    "Disease": disease_name,
                    "Link": disease_link,
                    "Description": description
                })
        if not conditions_list:
            print(f"No conditions found for letter '{letter}'.")

    else:
        print(f"No conditions found for letter '{letter}'.")


with open('conditions_data.json', 'w') as json_file:
    json.dump(all_conditions_data, json_file, indent=4)

print("Data has been written to conditions_data.json")
