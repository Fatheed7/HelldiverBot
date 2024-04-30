import nextcord
import requests
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io


async def get_planet(interaction, planet):  # sourcery skip
    url = "https://api.diveharder.com/v1/planets"
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            results = []
            for record_number, record in data.items():
                if 'name' in record and record['name'].lower().strip() == planet.lower().strip():
                    results.append(record)
            if len(results) > 0:
                biome = results[0]['biome']['name'].lower().replace(" ","-")
                print(biome)
                title = f'Planet Data for {results[0]['name']}'
                embed = nextcord.Embed(
                    title=title,
                    color=nextcord.Color.red())
                embed.set_thumbnail(
                    "https://helldiverscompanionimagescdn.b-cdn.net/icons/factions/Humans.png"
                )
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
                    inline=True)
                embed.add_field(name="",
                    value="",
                    inline=True)
                embed.add_field(name="Biome",
                    value=results[0]['biome']['description'],
                    inline=True)
                # # # # # # # # # # # # # # # #
                embed.add_field(name="Environmentals",
                                value="",
                                inline=False)
                for item in results[0]['environmentals']:
                    embed.add_field(name=item['name'],
                            value=item['description'],
                            inline=False)
                # # # # # # # # # # # # # # # #
                if biome != "unknown":
                    embed.set_image(
                        f"https://helldiverstrainingmanual.com/images/biomes/webp/{biome}.webp"
                    )
                await interaction.send(embed=embed)
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None