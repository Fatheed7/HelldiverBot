import nextcord
import requests
import json
import os
from datetime import datetime


async def send_new_order_cmd(channel):  # sourcery skip
    url = "https://api.diveharder.com/raw/major_order"
    type_data = load_types()
    reward_data = load_rewards()
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            order_type = data[0]['setting']['tasks'][0]['type']
            reward_type = data[0]['setting']['reward']['type']
            brief = data[0]['setting']['overrideBrief']
            deadline = int(datetime.now().timestamp()) + data[0]['expiresIn']
            file_path = "brief.txt"
            # If file does not exist, create it
            # and don't send a discord message
            if not os.path.exists(file_path):
                file_created = True
            with open(file_path, 'w') as file:
                # Write the variable to the file
                file.write(brief)
            if not file_created:
                # Return the JSON response
                title = data[0]['setting']['overrideTitle']
                embed = nextcord.Embed(
                    title=title,
                    color=nextcord.Color.red())
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
                await channel.send("New Major Order!", embed=embed, view=None)
        else:
            raise Exception(f"Expected Response Code 200 but receieved - {response.status_code}: {response.json()['detail']}")
    except requests.exceptions.RequestException as e:
        print("Error:", e)
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