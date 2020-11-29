import selenium as selenium
from selenium import webdriver
import re
import itertools
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
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

    def xpath_click(self, x_path):

        input_element = self.driver.find_element_by_xpath(x_path)
        input_element.click()

    def text_click(self, text):

        input_element = self.driver.find_element_by_link_text(text)
        input_element.click()

    def get_text_by_xpath(self, x_path):
        return self.driver.find_element_by_xpath(x_path).text

    def go_to(self, link):

        if link != self.driver.current_url:
            self.driver.get(link)

    def enter_text(self, x_path, value, submit=False):

        input_element = self.driver.find_element_by_xpath(x_path)
        input_element.send_keys(value)
        if submit:
            input_element.submit()

    def get_text(self, x_path):
        for attempt in range(10):
            try:
                text = self.driver.find_element_by_xpath(x_path).get_attribute('textContent').strip()
                return text
            except StaleElementReferenceException:
                pass
        raise StaleElementReferenceException


class EtsyInterface(WebInterface):

    def __init__(self, headless=True):
        super(EtsyInterface, self).__init__(headless)
        self.current_page = 1

    def next_page(self):
        self.current_page += 1
        for div in range(1, 1000):
            for page_index in range(1, 10):
                try:
                    x_path = f'//*[@id="content"]/div/div[1]/div/div/div[2]/div[2]/div[4]{"/div" * div}[2]/nav/ul/li[{page_index}]'
                    # print(x_path)
                    if f'Page {self.current_page}' in self.get_text_by_xpath(x_path):
                        self.xpath_click(x_path)
                        print(f"Navigated to Page {self.current_page} (page_index: {page_index}, div: {div})")
                        return
                except NoSuchElementException:
                    pass
            if page_index > self.current_page + 100:
                raise ValueError("Something went wrong...")

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
                    break
            parsed_ad = self.parse_ad(ad)
            if parsed_ad != -1:
                parsed_ad['page_num'] = self.current_page
                parsed_ad['ad_num'] = ad_number
                ads.append(parsed_ad)
        return ads

    @staticmethod
    def parse_ad(ad):
        title = re.findall('^[^\n]*', ad)[0]
        try:
            shop = re.findall('(?<=Ad\sfrom\sshop\s)(.*)(?=\n)', ad)[0]
            paid_ad = 1
        except IndexError:
            shop = re.findall('(?<=From\sshop\s)(.*)(?=\n)', ad)[0]
            paid_ad = 0
        try:
            sale_price = re.findall('(?<=Sale\sPrice\sCA[$])([.\d]*)(?=\s)', ad)[0]
            original_price = re.findall('(?<=Original\sPrice\sCA[$])([.\d]*)(?=\s)', ad)[0]
            percent_off = re.findall('\((.*)\%\soff', ad)[0]
        except IndexError:
            if 'CA$' in ad:
                original_price = re.findall('(?<=CA[$])(.*)(?=$|\n)', ad)[0]
                sale_price = original_price
                percent_off = 0
            elif 'Sold' in ad:
                return -1
            else:
                raise ValueError("No price listed")
        try:
            reviews = re.findall('(?<=\s)([^\s]*)(?=\sreviews)', ad)[0]
        except IndexError:
            reviews = 0
        d = {
            'title': title,
            'shop': shop,
            'original_price': float(original_price),
            'sale_price': float(sale_price),
            'percent_off': float(percent_off),
            'reviews': int(str(reviews).replace(',', '')),
            'paid_ad': int(paid_ad)
        }
        return d


if __name__ == "__main__":
    pass
