from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Configure Brave Browser
brave_path = "/usr/bin/brave-browser"  # Default Brave path on Kali
options = Options()
options.binary_location = brave_path

# Initialize WebDriver (automatically downloads if needed)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Navigate to the target website
driver.get("https://target.com")  # Replace with your target URL

# Add or modify the PHPSESSID cookie
driver.add_cookie({
    "name": "PHPSESSID",
    "value": "0d33e4b8481b3bce67c738edfd115442",  # Your session ID
    "domain": "target.com",  # Replace with the target domain
    "path": "/",
    "secure": False,  # Set to True if the site uses HTTPS
    "httpOnly": False
})

# Refresh to apply the cookie
driver.refresh()

# Keep the browser open (or use `driver.quit()` to close)
input("Press Enter to exit...")
driver.quit()
