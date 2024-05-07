import os

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import asyncio
import nextcord.ext.application_checks
import requests

from cmds import (  # noqa: F401
    get_major_order,
    send_new_order,
    scrape_personal,
    lookup_planet,
    get_store,
    itad_cmd
    )

if os.path.exists("env.py"):
    import env # noqa
TOKEN = os.environ.get('DISCORD_TOKEN')
intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents)
servers = [867600394196484107,1232979224835395657]


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


# Major Order Command #
@bot.slash_command(guild_ids=servers,
                   description="Get current Major Order")
async def major_order(interaction: Interaction):
    await get_major_order.get_major_order_cmd(interaction)

# Personal Order Command #
@bot.slash_command(guild_ids=servers,
                   description="Get current Personal Order")
async def personal_order(interaction: Interaction):
    await scrape_personal.get_personal(interaction)

# Store Command #
@bot.slash_command(guild_ids=servers,
                   description="Get current Store Contents")
async def store(interaction: Interaction):
    await get_store.get_store_contents(interaction)

# Planet Command #
@bot.slash_command(guild_ids=servers,
                   description="Search for Planet info")
async def planet(
    interaction: Interaction,
    planet: str = SlashOption(
        description="Enter the planet you wish to search for.", required=True)):
    await lookup_planet.get_planet(interaction, planet)

# ITAD Command #
@bot.slash_command(guild_ids=servers,
                   description="Search for a game on Is There Any Deal?")
async def itad(
    interaction: Interaction,
    game: str = SlashOption(
        description="Enter the game you wish to search for.", required=True)):
    await itad_cmd.get_price(interaction, game)

#Shutdown Bot
@bot.slash_command(guild_ids=servers,
                   description="Shutdown Bot")
async def shutdown(interaction: Interaction):
    if interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Shutting down bot", ephemeral=True)
        exit()
    else:
        await interaction.response.send_message("You don't have access to run this command", ephemeral=True)

def check_brief_change(new_brief):
    file_path = "brief.txt"
    try:
        with open(file_path, 'r') as file:
            old_brief = file.read()
            return new_brief != old_brief
    except FileNotFoundError:
        return True

async def check_brief_periodically():
    while True:
        channel = bot.get_channel(867600394875830284)
        await asyncio.sleep(3600)  # Wait for 300 seconds
        url = "https://api.diveharder.com/raw/major_order"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if len(data) > 0:
                    new_brief = data[0]['setting']['overrideBrief']
                    if channel:
                        if check_brief_change(new_brief):
                            await send_new_order.send_new_order_cmd(channel)
        except requests.exceptions.RequestException as e:
            print("Error:", e)

async def start_periodic_task():
    await check_brief_periodically()

nextcord.Client().loop.create_task(start_periodic_task())

bot.run(TOKEN)