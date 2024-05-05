from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
import nextcord
import os

async def get_personal(interaction):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--log-level=3")
        user_agent = (
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,'
            'like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        )
        chrome_options.add_argument('user-agent={0}'.format(user_agent))
        chrome_options.add_argument("--window-size=1920,1200")

        # Specify the path to Chrome WebDriver executable
        chrome_driver_path = "/path/to/chromedriver"

        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
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
