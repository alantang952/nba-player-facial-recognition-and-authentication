import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import urllib.request
import urllib
import os

driver = webdriver.Firefox()
os.chdir("scraped")
for i in range(0, 31):
    driver.get("https://www.nba.com/teams")
    driver.execute_script("window.scrollTo(0, 500)")
    l = driver.find_elements_by_link_text("Profile")
    link = l[i]
    link.click()
    # driver.execute_script("window.scrollTo(0, 400)")
    players = driver.find_elements_by_css_selector(".primary.text")[1: ]
    player_names = []
    for p in players:
        player_names.append(p.text)
    team_url = driver.current_url
    for n in player_names:
        driver.implicitly_wait(20)
        driver.get(team_url)
        driver.execute_script("window.scrollTo(0, 400)")
        driver.find_element_by_link_text(n).click()
        driver.implicitly_wait(10)
        # headshot_tag = '[alt="' + n + ' Headshot"]'
        
        link_elem = driver.find_element_by_xpath("//img[contains(@src,'headshot')]")
        hs_link = link_elem.get_attribute("src")
 
        name_list = n.split(" ")
        fn = name_list[1] + ", " + name_list[0]
        if not os.path.exists(fn):
            os.makedirs(fn)

        save_loc = fn + "/" + name_list[1] + name_list[0] + ".jpg"
        try:
            urllib.request.urlretrieve(hs_link, save_loc)
        except urllib.error.HTTPError as e:
            print(n)


