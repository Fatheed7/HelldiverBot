import nextcord
import requests
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io


async def get_major_order_cmd(interaction):  # sourcery skip
    url = "https://api.diveharder.com/raw/major_order"
    type_data = load_types()
    reward_data = load_rewards()
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            if len(data) == 0:
                title = "No current major orders!"
                embed = nextcord.Embed(
                    title=title,
                    color=nextcord.Color.red())
                embed.set_thumbnail(
                    "https://helldiverscompanionimagescdn.b-cdn.net/icons/factions/Humans.png"
                )
                embed.add_field(name="",
                                value="There are currently no active major orders. Good job, Helldivers!",
                                inline=False)
                await interaction.send(embed=embed)
            else:
                order_type = data[0]['setting']['tasks'][0]['type']
                reward_type = data[0]['setting']['reward']['type']
                brief = data[0]['setting']['overrideBrief']
                deadline = int(datetime.now().timestamp()) + data[0]['expiresIn']
                file_path = "brief.txt"
                with open(file_path, 'w') as file:
                    # Write the variable to the file
                    file.write(brief)
                # Return the JSON response
                title = data[0]['setting']['overrideTitle']
                embed = nextcord.Embed(
                    title=title,
                    color=nextcord.Color.red())
                embed.set_thumbnail(
                    "https://helldiverscompanionimagescdn.b-cdn.net/icons/factions/Humans.png"
                )
                embed.add_field(name="Type",
                    value=type_data[str(order_type)],
                    inline=True)
                embed.add_field(name="Reward",
                    value= str(data[0]['setting']['reward']['amount']) +
                    " " + reward_data[str(reward_type)],
                    inline=True)
                embed.add_field(name="Brief",
                                value=brief,
                                inline=False)
                embed.add_field(name="Description",
                                value=data[0]['setting']['taskDescription'],
                                inline=False)
                embed.add_field(name="Status",
                    value=(
                        str(data[0]['progress'][0]) + " / " +
                        str(data[0]['setting']['tasks'][0]['values'][0])),
                    inline=True)
                embed.add_field(name="Deadline",
                    value=(f"<t:{int(deadline)}:R> - <t:{int(deadline)}:f>"),
                    inline=True)
                await interaction.send(embed=embed)
        else:
            raise Exception(f"Expected Response Code 200 but receieved {response.status_code}: {response.json()['detail']}")
    except Exception as e:
        print("Error:", e)
        await interaction.response.send_message(f"Sorry flower, there has been an error - {e}", ephemeral=True)
        return None
    

def load_types():
    file = "json/type.json"
    with open(file, 'r') as j:
        # Find gem with matching name in json
        data = json.loads(j.read())
        return data
    
def load_rewards():
    file = "json/reward_type.json"
    with open(file, 'r') as j:
        # Find gem with matching name in json
        data = json.loads(j.read())
        return data