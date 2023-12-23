import requests
import json

def obter_dados_api(codigo_orgao, data_inicial, num_paginas):
    url = "https://api.portaldatransparencia.gov.br/api-de-dados/contratos"
    key = "34ed1e6231d354e35948e24139e48ee9"

    params = {"codigoOrgao": codigo_orgao, "quantidade": 100, "dataInicial": data_inicial, "pagina": 1}
    headers = {"accept": "*/*", "chave-api-dados": key}

    all_data = []  # Create a single list to store all data

    while params["pagina"] <= num_paginas:
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            dados_json = response.json()

            if not dados_json:
                break

            all_data.extend(dados_json)  # Append data to the single list
            params["pagina"] += 1

        except requests.exceptions.RequestException as e:
            print("Erro ao fazer a requisição:", e)
            break

    return all_data

def salvar_em_json(data, nome_arquivo):
    with open(nome_arquivo, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

codigo_orgao = "52111"  # Replace with your organization code
data_inicial = "01/01/2018"  # Replace with your start date
num_paginas = 500  # Replace with the desired number of pages
nome_arquivo_json = "output_data.json"  # Replace with your desired output file name

dados_paginas = obter_dados_api(codigo_orgao, data_inicial, num_paginas)
salvar_em_json(dados_paginas, nome_arquivo_json)