import json
import os

from scraping.driver import get_driver
from scraping.navigator import open_about_sunbeam, open_branches
from scraping.scrapers.about_sunbeam import scrape_about_sunbeam
from scraping.scrapers.branches import get_branch_detail_links
from scraping.scrapers.branch_detail import scrape_branch_detail
from scraping.scrapers.courses_list import get_modular_courses
from scraping.scrapers.course_detail import scrape_course_detail


def main():
    driver = get_driver()
    driver.get("https://www.sunbeaminfo.in")

    final_data = {}

    print(">>> Scraping About Sunbeam")
    open_about_sunbeam(driver)
    about_data = scrape_about_sunbeam(driver)
    print("About Sunbeam paragraphs:", len(about_data.get("content", [])))
    final_data["about_sunbeam"] = about_data

    print(">>> Scraping Branches")
    open_branches(driver)
    branch_links = get_branch_detail_links(driver)
    print("Branch links found:", branch_links)

    branches_data = {}
    for branch in branch_links:
        branches_data[branch["name"]] = scrape_branch_detail(driver, branch)

    final_data["branches"] = branches_data

    print(">>> Scraping Modular Courses")
    driver.get("https://www.sunbeaminfo.in/modular-courses-home")
    courses = get_modular_courses(driver)
    print("Courses found:", courses)

    courses_data = {}
    for course in courses:
        courses_data[course["name"]] = scrape_course_detail(driver, course)

    final_data["modular_courses"] = courses_data

    output_path = "scraping/data/sunbeam.json"
    abs_path = os.path.abspath(output_path)
    print(">>> Writing JSON to:", abs_path)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4, ensure_ascii=False)

    driver.quit()
    print(">>> DONE")


if __name__ == "__main__":
    main()
