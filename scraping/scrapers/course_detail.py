from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_course_detail(driver, course):
    driver.get(course["url"])

    wait = WebDriverWait(driver, 10)

    # Try common content containers (in order of reliability)
    content = ""

    selectors = [
        (By.CLASS_NAME, "inner_page_wrap"),
        (By.CLASS_NAME, "container"),
        (By.TAG_NAME, "body")
    ]

    for by, value in selectors:
        try:
            element = wait.until(EC.presence_of_element_located((by, value)))
            content = element.text.strip()
            if content:
                break
        except:
            continue

    return {
        "name": course["name"],
        "duration": course["duration"],
        "url": course["url"],
        "content": content
    }
