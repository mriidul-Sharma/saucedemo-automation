from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class InventoryPage(BasePage):
    # Locators
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    PAGE_TITLE = (By.CLASS_NAME, "title")

    def __init__(self, driver):
        super().__init__(driver)

    def is_cart_visible(self):
        return self.is_visible(self.CART_ICON)

    def get_page_title(self):
        return self.get_text(self.PAGE_TITLE)