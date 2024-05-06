import nextcord
import requests
from nextcord.ext import menus

async def get_store_contents(interaction):
    url = "https://api.diveharder.com/v1/store_rotation"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
        pages = CustomButtonMenuPages(source=DataSource(data))
        await pages.start(interaction=interaction)
    except Exception as e:
        print("Error:", e)
        await interaction.response.send_message(f"Sorry flower, there has been an error - {e}", ephemeral=True)
        return None

class CustomButtonMenuPages(menus.ButtonMenuPages, inherit_buttons=False):
        def __init__(self, source, timeout=60):
            super().__init__(source, timeout=timeout, disable_buttons_after=True, clear_buttons_after=True)

            self.add_item(menus.MenuPaginationButton(emoji=self.FIRST_PAGE, label="First"))
            self.add_item(menus.MenuPaginationButton(emoji=self.PREVIOUS_PAGE, label="Prev"))
            self.add_item(menus.MenuPaginationButton(emoji=self.NEXT_PAGE, label="Next"))
            self.add_item(menus.MenuPaginationButton(emoji=self.LAST_PAGE, label="Last"))

            # Rearrange the buttons (place the Stop button (first button) at the end of the list)
            self.children = self.children[1:] + self.children[:1]

            # Disable buttons that are unavailable to be pressed at the start
            self._disable_unavailable_buttons()

        @nextcord.ui.button(emoji="\N{BLACK SQUARE FOR STOP}", label="Stop")
        async def stop_button(self):
            self.stop()

class DataSource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data['items'], per_page=2)

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        embed = nextcord.Embed(title="Store Rotation")
        embed.set_thumbnail(
                    "https://helldiverscompanionimagescdn.b-cdn.net/icons/factions/Humans.png"
                )
        for i, entry in enumerate(entries, start=offset):
            embed.add_field(name=f"{entry['name']}", value=entry['description'], inline=False)
            embed.add_field(name=f"Type: ", value=entry['type'], inline=True)
            embed.add_field(name=f"Slot: ", value=entry['slot'], inline=True)
            embed.add_field(name=f"Cost: ", value=entry['store_cost'], inline=True)
            embed.add_field(name=f"Armour: ", value=entry['armor_rating'], inline=True)
            embed.add_field(name=f"Speed: ", value=entry['speed'], inline=True)
            embed.add_field(name=f"Stamina Regen: ", value=entry['stamina_regen'], inline=True)
            embed.add_field(name=f"Passive: ", value=entry['passive']['name'] + " - " + entry['passive']['description'], inline=False)
            embed.add_field(name="", value="\u200B", inline=False)
        return embed