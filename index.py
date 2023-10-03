import pandas as pd
import requests
import json
import openai
from openaiAPIKey import openai_api_key

df = pd.read_csv("SDW2023.csv")
user_ids = df["UserID"].to_list()

sdw2023_api_url = "https://sdw-2023-prd.up.railway.app"
openai.api_key = openai_api_key


def get_user(id):
    response = requests.get(f"{sdw2023_api_url}/users/{id}")
    return response.json() if response.status_code == 200 else None


users = [user for id in user_ids if (user := get_user(id)) is not None]

print(json.dumps(user, indent=2))


def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em desenvolvimento de software.",
            },
            {
                "role": "user",
                "content": f"Crie uma mensagem para {user['name']} dando informações sobre as linguagens de programação mais usadas no mercado e como iniciar em cada uma delas. (máximo de 300 caracteres)",
            },
        ],
    )
    return completion.choices[0].message.content.strip('"')


for user in users:
    news = generate_ai_news(user)
    print(news)
    user["news"].append(
        {
            "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
            "description": news,
        }
    )
