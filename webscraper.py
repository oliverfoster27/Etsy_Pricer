import selenium as selenium
from selenium import webdriver
import re
import itertools
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException


class WebInterface:

    def __init__(self, headless=True):

        # Get the driver
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        if headless:
            options.add_argument("--headless")
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})
        options.add_argument("--test-type")
        options.add_argument("--start-maximized")
        options.add_argument("--no-first-run")
        options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        self.driver = webdriver.Chrome(chrome_options=options)

    def go_to(self, link):

        if link != self.driver.current_url:
            self.driver.get(link)

    def enter_text(self, x_path, value, submit=False):

        input_element = self.driver.find_element_by_xpath(x_path)
        input_element.send_keys(value)
        if submit:
            input_element.submit()

    def get_text(self, x_path):
        return self.driver.find_element_by_xpath(x_path).get_attribute('textContent').strip()


class EtsyInterface(WebInterface):

    def get_ads(self):
        ads = []
        for ad_number in itertools.count(1):
            try:
                ad = self.get_text(
                    f'//*[@id="content"]/div/div[1]/div/div/div[2]/div[2]/div[3]/div/div[1]/div/li[{ad_number}]/div/a/div[2]')
            except NoSuchElementException:
                try:
                    ad = self.get_text(
                        f'//*[@id="content"]/div/div[1]/div/div/div[2]/div[2]/div[3]/div/div[1]/div/li[{ad_number}]/div/div/a/div[2]')
                except NoSuchElementException:
                    print("Done!")
                    break
            parsed_ad = self.parse_ad(ad)
            parsed_ad['Ad Number'] = ad_number
            ads.append(parsed_ad)
        return ads

    @staticmethod
    def parse_ad(ad):
        title = re.findall('^[^\n]*', ad)[0]
        try:
            shop = re.findall('(?<=Ad\sfrom\sshop\s)(.*)(?=\n)', ad)[0]
            paid_ad = True
        except IndexError:
            shop = re.findall('(?<=From\sshop\s)(.*)(?=\n)', ad)[0]
            paid_ad = False
        try:
            sale_price = re.findall('(?<=Sale\sPrice\sCA[$])([.\d]*)(?=\s)', ad)[0]
            original_price = re.findall('(?<=Original\sPrice\sCA[$])([.\d]*)(?=\s)', ad)[0]
            percent_off = re.findall('\((.*)\%\soff', ad)[0]
        except IndexError:
            original_price = re.findall('(?<=CA[$])(.*)(?=$|\n)', ad)[0]
            sale_price = original_price
            percent_off = None
        try:
            reviews = re.findall('(?<=\s)([^\s]*)(?=\sreviews)', ad)[0]
        except IndexError:
            reviews = 0
        d = {
            'Title': title,
            'Shop': shop,
            'Original Price': original_price,
            'Sale Price': sale_price,
            'Percent Off': percent_off,
            'Reviews': reviews,
            'Paid Ad': paid_ad
        }
        return d


if __name__ == "__main__":
    pass
