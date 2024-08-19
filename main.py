# Repositório da API: https://github.com/digitalinnovationone/santander-dev-week-2023-api
sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

# TODO: Extrair os IDs do arquivo csv
import pandas as pd

df = pd.read_csv('src/doc/SDW2023.csv')
user_ids = df['UserID'].tolist()
# display(user_ids)

# TODO: Obter os dados de cada ID usando a API do Santander Dev Week 2023
import requests
import json

def get_user(id):
    response = requests.get(f'{sdw2023_api_url}/users/{id}')
    return response.json() if response.status_code == 200 else None

users = [ user for id in user_ids if (user := get_user(id)) is not None ]

print(json.dumps(users, indent = 2))
# %pip install openai
openai_api_key = 'TODO'

# TODO: Implementar a integração com o ChatGPT usando o modelo GPT-4

import openai
openai.api_key = openai_api_key


def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        # model="gpt-4",
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em markting bancário."
            },
            {
                "role": "user",
                "content": f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres)"
            }
        ]
    )
    responseChaGPT = completion.choices[0].message.content.strip("\"") # Remover as aspas da resposta do ChatGPT
    return responseChaGPT

for user in users:
    news = generate_ai_news(user)
    # print(news)
    user['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": news
    })

    def update_user(user):
    response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json = user)
    return True if response.status_code == 200 else False

for user in users:
    success = update_user(user)
    print(f"User {user['name']} updated: {success}")