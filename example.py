# SKELETON FOR COMBINING SELENIUM WITH SCRAPY
from scrapy import Selector
# Other Selenium and Scrapy imports

# Selenium tasks and actions to render the webpage with required content
selenium_response_text = driver.page_source
new_selector = Selector(text=selenium_response_text)
# Scrapy tasks to extract data from Selector
#Example using OpenAQ
#Similar to the Selenium tutorial, this example too shall be using 3 steps to extract PM2.5 data from http://openaq.org. These 3 steps are:
#Collecting country names as displayed on OpenAQ countries webpage. This would be used in selecting appropriate checkboxes.
#Collecting URLs that contain PM2.5 data from each country. There are countries that contain more than 20 PM2.5 readings from various locations. It would require further manipulation of the webpage, which is explained in the code section.
#Opening up the individual URL and extracting PM2.5 data.
#These steps would be performed by 3 basic spiders and the output from these spiders would be stored in JSON format. NOTE: A prior working knowledge of Selenium & Scrapy is required to understand this example. The code for this example can be found in my GitHub repository.
#countries_spider
#Below is the code for the spider that extracts country names and stores it in a JSON file. It can be seen that this spider does not adhere to the skeleton of combining Selenium with Scrapy. The main reason is that it would be efficient to just pass on the cards already extracted by Selenium to Scrapy’s yield functionality which would automatically write it to a JSON file implicitly. The skeleton of combining these two is followed in the spider that extracts PM2.5 values from individual locations.
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logzero import logfile, logger

class CountriesSpiderSpider(scrapy.Spider):
    # Initializing log file
    logfile("openaq_spider.log", maxBytes=1e6, backupCount=3)   
    name = "countries_spider"
    allowed_domains = ["toscrape.com"]
# Using a dummy website to start scrapy request
    def start_requests(self):
        url = "http://quotes.toscrape.com"
        yield scrapy.Request(url=url, callback=self.parse_countries)

    def parse_countries(self, response):
    # driver = webdriver.Chrome()  # To open a new browser window and navigate it
    # Use headless option to not open a new browser window
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
        # Getting list of Countries
        driver.get("https://openaq.org/#/countries")
        # Implicit wait
        driver.implicitly_wait(10)
        # Explicit wait
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card__title")))
        countries = driver.find_elements_by_class_name("card__title")
        countries_count = 0
        # Using Scrapy's yield to store output instead of explicitly writing to a JSON file
        for country in countries:
            yield {
                "country": country.text,
            }
            countries_count += 1
        driver.quit()
        logger.info(f"Total number of Countries in openaq.org: {countries_count}")