from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re

def get_rebo_listings():
    element_list = []

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://www.rebogroep.nl/nl/particulier/ons-aanbod/huren?page=1")

    wait = WebDriverWait(driver, 15)

    # Accept cookie popup if present
    try:
        cookie_button = wait.until(
            EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
        )
        cookie_button.click()
    except:
        pass  # no cookie banner appeared

    # open filter
    plaats_filter = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Plaats']"))
    )

    plaats_filter.click()

    # click Arnhem
    arnhem_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Arnhem')]"))
    )
    arnhem_button.click()

    # Wait until the Arnhem button is selected / active
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[contains(@class,'selected') and contains(., 'Arnhem')]")
        )
    )

    # wait until listings appear
    wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "object-card"))
    )

    # give JS a moment to refresh results
    driver.implicitly_wait(2)

    listings = driver.find_elements(By.CLASS_NAME, "object-card")

    for listing in listings:
        try:
            link = listing.get_attribute("href")
            title = listing.find_element(By.CSS_SELECTOR, ".location h5").text
            price_text = listing.find_element(By.CSS_SELECTOR, ".bottom h6").text
            match = re.search(r"\d[\d\.]*", price_text)
            if match:
                price = "€ " + match.group().replace(".", "")
            else:
                price = price_text
            element_list.append({"title": title, "price": price, "url": link})
        except Exception as e:
            print("Error:", e)

    driver.quit()
    return element_list