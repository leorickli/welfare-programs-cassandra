import requests
import json

def get_api_data(organization_code, initial_date, number_of_pages):
    url = "https://api.portaldatransparencia.gov.br/api-de-dados/contratos"
    key = "34ed1e6231d354e35948e24139e48ee9"

    params = {"codigoOrgao": organization_code, "quantidade": 100, "dataInicial": initial_date, "page": 1}
    headers = {"accept": "*/*", "chave-api-dados": key}

    all_data = []  # Create a single list to store all data

    while params["page"] <= number_of_pages:
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            json_data = response.json()

            if not json_data:
                break

            all_data.extend(json_data)  # Append data to the single list
            params["page"] += 1

        except requests.exceptions.RequestException as e:
            print("Error making the request:", e)
            break

    return all_data

def save_in_json(data, file_name):
    with open(file_name, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

organization_code = "52111"  # Replace with your organization code
initial_date = "01/01/2018"  # Replace with your start date
number_of_pages = 500  # Replace with the desired number of pages
json_file_name = "output_data.json"  # Replace with your desired output file name

page_data = get_api_data(organization_code, initial_date, number_of_pages)
save_in_json(page_data, json_file_name)