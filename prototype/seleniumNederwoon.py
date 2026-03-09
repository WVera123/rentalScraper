from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_nederwoon_listings():
    element_list = []
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    nederwoonUrl = 'https://www.nederwoon.nl/search?search_type=1&city=Arnhem+%2810%29'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(nederwoonUrl)

    listings = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'location'))
    )

    for listing in listings:
        try:
            findDivTitle = WebDriverWait(listing, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.col-lg-4.col-md-3.click-see-page-button'))
            )
            title_element = findDivTitle.find_element(By.TAG_NAME, 'h2').find_element(By.TAG_NAME, 'a')
            title = title_element.text.strip()
            url = title_element.get_attribute('href')

            findDivPrice = WebDriverWait(listing, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.col-lg-4.col-md-3.vertical-items.start-items.click-see-page-button .item-start.fixed-lh'))
            )
            price_element = findDivPrice.find_element(By.CSS_SELECTOR, '.heading-md.text-regular.color-primary')
            price = price_element.text.strip().split(",")[0]

            element_list.append({"title": title, "price": price, "url": url})
        except Exception as e:
            print(f"Error processing listing: {e}")

    driver.quit()
    return element_list