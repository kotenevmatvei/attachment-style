import time
import csv
from playwright.sync_api import Page

scores = []
with open("correct_scores_before_revert.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        scores.append(row)

        


def test_giga(page: Page) -> None:

    for case_scores in scores:
        page.goto("http://127.0.0.1:8050/")
        page.get_by_role("button", name="Assess Yourself").click()

        page.locator("#age").click()
        page.locator("#age").fill("23")
        page.locator("#relationship-status").select_option("single")
        page.locator("#gender").select_option("male")
        page.locator("#therapy-experience").select_option("extensive")

        page.get_by_role("button", name="Continue to the test").click()


        for score in case_scores:
            if score != 1:
                page.locator(f"span:nth-child({score})").first.click()
                time.sleep(0.01)
                page.get_by_role("button", name="").click()
            else:
                page.get_by_role("slider").click() 
                time.sleep(0.01)
                page.get_by_role("button", name="").click()
            time.sleep(0.01)

        page.get_by_role("button", name="To Results").click()
        time.sleep(1)


