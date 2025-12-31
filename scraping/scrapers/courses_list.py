from selenium.webdriver.common.by import By

def get_modular_courses(driver):
    courses = []

    # Each course card
    cards = driver.find_elements(By.CSS_SELECTOR, "div.c_cat_box")

    for card in cards:
        try:
            info_text = card.find_element(By.CLASS_NAME, "c_info").text.strip()
        except:
            continue

        lines = [l.strip() for l in info_text.split("\n") if l.strip()]
        name = lines[0] if len(lines) > 0 else ""
        duration = lines[1] if len(lines) > 1 else ""

        try:
            link = card.find_element(By.CSS_SELECTOR, "a.c_cat_more_btn").get_attribute("href")
        except:
            link = ""

        if link and name:
            courses.append({
                "name": name,
                "duration": duration,
                "url": link
            })

    return courses
