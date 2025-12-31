from selenium.webdriver.common.by import By

def scrape_about_sunbeam(driver):
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "div.main_info p")

    return {
        "title": "About Sunbeam",
        "content": [p.text.strip() for p in paragraphs if p.text.strip()]
    }
