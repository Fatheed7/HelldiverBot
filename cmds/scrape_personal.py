from bs4 import BeautifulSoup
import nextcord
import requests

async def get_personal(interaction):
    try:
        url = 'https://helldivers.io/'
        personal_order_text = get_personal_order_text(url)
        if personal_order_text:
            split_text = personal_order_text.split('<br>')
        else:
            print("Personal order text not found.")
        embed = nextcord.Embed(
                    title="Personal Order",
                    color=nextcord.Color.red())
        embed.add_field(name="Mission",
                        value=split_text[0],
                        inline=True)
        embed.add_field(name="Reward",
                value=split_text[1][8:],
                inline=True)
        await interaction.send(embed=embed)

    except Exception as e:
        print("Error:", e)
        await interaction.response.send_message(f"Sorry flower, there has been an error - {e}", ephemeral=True)
        return None


def get_personal_order_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    scripts = soup.find_all('script')

    script_text = [script.text for script in scripts]
    
    for text in script_text:
        if 'PERSONAL ORDER' in text:
            start_index = text.find("PERSONAL ORDER")
            end_index = text.find("Time Left", start_index)
            personal_order_text = text[start_index:end_index].strip()
            personal_order_text = personal_order_text[23:]
            return personal_order_text
    
    return None