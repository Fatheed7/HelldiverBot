import nextcord
import requests
import json


async def role_add(guild, interaction):  # sourcery skip
    try:
        member = interaction.user
        role = guild.get_role(1099697899866161162)
        await member.add_roles(role)
        await interaction.send(
            "Helldiver role granted", ephemeral = True)
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
    