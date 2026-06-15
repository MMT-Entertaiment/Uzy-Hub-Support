import discord
import yaml
import requests
import os
from discord.ext import commands

# URL du fichier raw sur GitHub
DB_URL = "https://raw.githubusercontent.com/MMT-Entertaiment/Uzy-Hub-Support/main/DB.yaml"

def load_db():
    try:
        response = requests.get(DB_URL)
        response.raise_for_status()
        return yaml.safe_load(response.text)
    except Exception as e:
        print(f"Erreur lors du chargement de la DB : {e}")
        return None

db = load_db()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if db and 'data' in db:
        content = message.content.lower()
        # Parcours des topics dans la DB
        for item in db['data']:
            if item['topic'].lower() in content:
                await message.channel.send(item['info'])
                break # On arrête après la première correspondance trouvée
    
    await bot.process_commands(message)

# Récupération du token via les Secrets de Hugging Face
token = os.getenv('DISCORD_TOKEN')
bot.run(token)
