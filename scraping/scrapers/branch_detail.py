from selenium.webdriver.common.by import By

def scrape_branch_detail(driver, branch):
    driver.get(branch["url"])

    # Main content
    content = driver.find_element(By.CLASS_NAME, "main_info").text

    return {
        "name": branch["name"],
        "url": branch["url"],
        "content": content
    }
