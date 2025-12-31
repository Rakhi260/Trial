from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_for_navbar(driver):
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "nav"))
    )


def get_about_us_element(driver):
    return WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//nav//a[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'ABOUT')]"
            )
        )
    )


def hover_about_us(driver):
    wait_for_navbar(driver)

    about_us = get_about_us_element(driver)

    # JS hover (much more reliable than ActionChains)
    driver.execute_script(
        "arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));",
        about_us
    )


def click_submenu(driver, href_contains):
    submenu = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//ul[contains(@class,'dropdown-menu')]//a[contains(@href,'{href_contains}')]"
            )
        )
    )

    driver.execute_script("arguments[0].click();", submenu)


def open_about_sunbeam(driver):
    hover_about_us(driver)
    click_submenu(driver, "about-us")


def open_branches(driver):
    hover_about_us(driver)
    click_submenu(driver, "branches")
