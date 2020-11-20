from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest
from operator import itemgetter
from natsort import natsorted
import table_getter as tg


@pytest.fixture()
def setup():
    print("SETUP START")
    global driver
    goal_url = 'https://en.wikipedia.org/wiki/List_of_tallest_buildings'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(goal_url)
    global original_table
    original_table = tg.get_table(driver.page_source)
    yield "setup"
    print("SETUP END")
    driver.close()
    driver.quit()


def test_sorting_by_rank(setup):

    # make two clicks on Rank column, two clicks needed because the first click activates the descending order, which is displayed by default
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/thead/tr[1]/th[1]').click()
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/thead/tr[1]/th[1]').click()
    sorted_table_by_rank = tg.get_table(driver.page_source)
    assert sorted_table_by_rank == sorted(original_table, key=itemgetter(0), reverse=True)
    print("Sorting by rank: pass")

def test_sorting_by_name(setup):

    # only one click needed, as by default the table is sorted by rank
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/thead/tr[1]/th[2]').click()
    sorted_table_by_name = tg.get_table(driver.page_source)
    # Using natural sorting in the next assert to avoid problems with elements containing strings and ints.
    assert sorted_table_by_name[0][0] == natsorted(original_table, key=itemgetter(1), reverse=False)[0][0]
    print("sorting by name: pass")

def test_buildings_max_count():

    countries_list = [element[3] for element in original_table]
    country_max_count = max(countries_list, key=countries_list.count)
    assert country_max_count == "China"
    print(f"Checked if {country_max_count} is the county with maximum number of buildings: pass")

def test_oldest_building():

    # select all the years from the original table
    years_list = [element[7] for element in original_table]
    for element in original_table:
        if element[7] == min(years_list):
            oldest_building = element[1]
    assert oldest_building == "Empire State Building"
    print(f"Checked if {oldest_building} is the oldest building: pass")




