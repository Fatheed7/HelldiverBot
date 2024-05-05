from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from io import BytesIO
import nextcord
import requests

async def get_personal(interaction):
    try:
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument("--log-level=3")
        user_agent = (
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,'
            'like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        )
        options.add_argument("--window-size=1920,1200")
        options.add_argument('user-agent={0}'.format(user_agent))

        driver = webdriver.Chrome(
            options=options,
            service=ChromeService(ChromeDriverManager().install()))

        driver.get("https://helldivers.io/")

        canvas = driver.find_element(By.CSS_SELECTOR, "canvas")

        canvas_width = canvas.size["width"]
        canvas_height = canvas.size["height"]

        capture_width = int(canvas_width * 0.25)
        capture_height = int(canvas_height * 0.15)

        screenshot = driver.get_screenshot_as_png()

        screenshot = Image.open(BytesIO(screenshot))
        cropped_image = screenshot.crop((canvas.location['x'] + 100, canvas.location['y'] + 60,
                                        canvas.location['x'] + capture_width + 100,
                                        canvas.location['y'] + capture_height + 60))

        cropped_image.save("canvas.png")
        file = nextcord.File("canvas.png", filename="canvas.png")

        driver.quit()
        embed = nextcord.Embed(
            title="Personal Order",
            color=nextcord.Color.red())
        embed.set_image(url="attachment://canvas.png")
        await interaction.send(file=file, embed=embed)

    except Exception as e:
        print("Error:", e)
        await interaction.response.send_message(f"Sorry flower, there has been an error - {e}", ephemeral=True)
        return None
