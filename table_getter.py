import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


goal_url = 'https://en.wikipedia.org/wiki/List_of_tallest_buildings'
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.get(goal_url)


#Function to get table from an instance of a web-page
def get_table(html):

    #all the pandas dataframes from the web-page:
    dfs = pd.read_html(html)
    #Select only the second table
    df = dfs[2]
    data = []
    for i in range(0, 74):
        '''
        Select Rank, Name, City, Country, Height m, Height ft, Floors, Year and return them as list of lists:
        [[1, 'Burj Khalifa', 'Dubai', 'United Arab Emirates', 828.0, 2717, 163, 2010], [2, 'Shanghai Tower', 'Shanghai', 'China', 632.0, 2073, 128, 2015],...]
        '''
        data.append([df.iloc[i][0], df.iloc[i][1], df.iloc[i][3], df.iloc[i][4], df.iloc[i][5], df.iloc[i][6], df.iloc[i][7], df.iloc[i][8]])
    driver.quit()
    return data

