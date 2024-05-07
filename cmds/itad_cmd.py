import requests
import os
import nextcord
import json
from slugify import slugify

if os.path.exists("env.py"):
    import env # noqa
KEY = os.environ.get('ITAD_KEY')


async def get_price(interaction, game):
    try:
        initial_response = requests.get(
            "https://api.isthereanydeal.com/games/lookup/v1?key="
            + KEY + "&title=" + slugify(game) + "&region=eu2")
        game_id = initial_response.json()['game']['id']
        response = requests.post(
            "https://api.isthereanydeal.com/games/prices/v2?key="
            + KEY + "&nondeals=true&country=gb",json=[game_id])
        parsed_data = response.json()
        if len(parsed_data) > 0:
            embed = nextcord.Embed(
                title="Are there any deals for " + game + "?",
                color=nextcord.Color.blue())
            embed.set_author(
                    name="Is There Any Deal",
                    icon_url=(
                        "https://scontent-man2-1.xx.fbcdn.net/v/t39.30808-6/359510045_1010356070269384_4740146774791971432_n.jpg?"
                        "_nc_cat=100&ccb=1-7&_nc_sid=5f2048&_nc_ohc=o0b4EqrAS28Q7kNvgHAYjzN&_nc_ht=scontent-man2-1.xx&cb_e2o_trans"
                        "=q&oh=00_AfBtl7sfPwhu1JzEwLjq_prs6TLa3k2Id0mYviSR1d8c5A&oe=663FF5B4"))
            for game in parsed_data:
                for deal in game['deals']:
                    embed.add_field(name=deal['shop']['name'],
                                    value='[£' + f"{deal['price']['amount']:.2f}" +
                                    '](' + deal['url'] + ')',
                                    inline=True)
                await interaction.send(embed=embed)
        else:
            await interaction.send(
                "Sorry daddy, there are no results for that game.")
    except Exception as e:
        print("Error:", e)
        await interaction.response.send_message(f"Sorry flower, there has been an error - {e}", ephemeral=True)
        return None