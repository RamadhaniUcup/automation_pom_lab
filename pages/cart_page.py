
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CartPage(BasePage):
    """Page Object untuk halaman Shopping Cart SauceDemo."""

    CART_TITLE = (
        By.XPATH,
        "//span[contains(@class, 'title') and normalize-space()='Your Cart']"
    )

    CART_ITEMS = (
        By.XPATH,
        "//div[contains(concat(' ', normalize-space(@class), ' '), ' cart_item ')]"
    )

    REMOVE_BACKPACK_BUTTON = (
        By.XPATH,
        "//button[@data-test='remove-sauce-labs-backpack']"
    )

    CHECKOUT_BUTTON = (
        By.XPATH,
        "//button[@data-test='checkout']"
    )

    CART_LINK = (
        By.XPATH,
        "//a[@data-test='shopping-cart-link']"
    )

    def open_cart(self):
        self.click(self.CART_LINK)

    def is_cart_displayed(self):
        return self.find_element(self.CART_TITLE).is_displayed()

    def get_cart_item_count(self):
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def remove_backpack(self):
        self.click(self.REMOVE_BACKPACK_BUTTON)
        self.wait.until(
            EC.invisibility_of_element_located(self.REMOVE_BACKPACK_BUTTON)
        )

    def click_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
