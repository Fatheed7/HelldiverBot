import nextcord
import requests
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io


async def get_planet(interaction, planet):  # sourcery skip
    url = "https://api.diveharder.com/v1/all"
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            results = []
            record_number = []
            planet_data = []
            for number, record in data['planets'].items():
                if 'name' in record and record['name'].lower().strip() == planet.lower().strip():
                    results.append(record)
                    record_number.append(number)
            for record in data['planet_stats']['planets_stats']:
                if str(record_number[0]) == str(record['planetIndex']):
                    planet_data.append(record)
            if len(results) > 0:
                biome = results[0]['biome']['name'].lower().replace(" ","-")
                title = f'Planet Data for {results[0]['name']}'
                embed = nextcord.Embed(
                    title=title,
                    color=nextcord.Color.red())
                # # # # # # # # # # # # # # # #
                embed.add_field(name="Name",
                    value=results[0]['name'],
                    inline=True)
                embed.add_field(name="",
                    value="",
                    inline=True)
                embed.add_field(name="Sector",
                    value=results[0]['sector'],
                    inline=True)
                # # # # # # # # # # # # # # # #
                embed.add_field(name="Biome",
                    value=results[0]['biome']['name'],
                    inline=False)
                embed.add_field(name="Biome Data",
                    value=results[0]['biome']['description'],
                    inline=False)
                # # # # # # # # # # # # # # # #
                embed.add_field(name="Environmentals",
                                value="",
                                inline=False)
                for item in results[0]['environmentals']:
                    embed.add_field(name=item['name'],
                            value=item['description'],
                            inline=False)
                # # # # # # # # # # # # # # # #
                if len(planet_data) > 0:
                    embed.add_field(name="",
                        value="\u200B")
                if len(planet_data) > 0:
                    embed.add_field(name="",
                        value="\u200B")
                if len(planet_data) > 0:
                    embed.add_field(name="",
                        value="\u200B")
                # # # # # # # # # # # # # # # #
                    embed.add_field(name="Missions Won",
                        value=format(planet_data[0]['missionsWon'],',d'),
                        inline=True) 
                    embed.add_field(name="Missions Lost",
                        value=format(planet_data[0]['missionsLost'],',d'),
                        inline=True) 
                    embed.add_field(name="Success Rate",
                        value=str(planet_data[0]['missionSuccessRate']) + "%",
                        inline=True) 
                # # # # # # # # # # # # # # # #
                    embed.add_field(name="Terminids squashed",
                        value=format(planet_data[0]['bugKills'],',d'),
                        inline=True) 
                    embed.add_field(name="Automatons Scrapped",
                        value=format(planet_data[0]['automatonKills'],',d'),
                        inline=True) 
                    embed.add_field(name="Illuminates Fisted",
                        value=format(planet_data[0]['illuminateKills'],',d'),
                        inline=True) 
                # # # # # # # # # # # # # # # #
                    embed.add_field(name="Lives given to Democracy",
                        value=format(planet_data[0]['deaths'],',d'),
                        inline=True) 
                    embed.add_field(name="",
                        value="",
                        inline=True) 
                    embed.add_field(name="Accidentals",
                        value=format(planet_data[0]['friendlies'],',d'),
                        inline=True) 
                # # # # # # # # # # # # # # # #
                if biome != "unknown":
                    embed.set_image(
                        f"https://helldiverstrainingmanual.com/images/biomes/webp/{biome}.webp"
                    )
                await interaction.send(embed=embed)
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None