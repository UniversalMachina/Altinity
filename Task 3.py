from selenium.webdriver.common.by import By
from testflows.core import TestScenario, TestModule, Module, Given, When, Then, main
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

print('Program starting')
options = Options()
options.add_argument('-headless')
firefox_binary_path = '/usr/bin/firefox'
options.binary_location = firefox_binary_path
# Set up the Firefox service with the GeckoDriverManager
firefox_service = Service(executable_path=GeckoDriverManager().install())
driver = webdriver.Firefox(options=options, service=firefox_service)
print("Firefox Ready")

# @TestScenario
def test_altinity_blog():
    """Test Altinity's website by navigating to the blog page and checking the title."""
    print("Going To webpage")
    with When("I navigate to https://altinity.com/"):
        driver.get("https://altinity.com/")
    print("Clicking on button")
    with Then("I click the BLOG button in the top menu"):
        blog_button = driver.find_element(By.XPATH, "/html/body/div[2]/header/div[1]/div/div/div/div[2]/div/div/div/div[2]/div[1]/nav/div/ul/li[5]/a")
        blog_button.click()
    print("Checking URL")
    with Then("I am redirected to https://altinity.com/blog/"):
        assert driver.current_url == "https://altinity.com/blog/"
    print("Checking Header")
    with Then("The title in the header section is 'Altinity Blog'"):
        header_title = driver.title
        print(header_title)
    driver.quit()


test_altinity_blog()