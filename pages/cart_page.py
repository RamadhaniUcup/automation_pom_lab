
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CartPage(BasePage):
    """Page Object untuk halaman Shopping Cart SauceDemo."""

    CART_URL_FRAGMENT = "/cart.html"

    CART_TITLE = (
        By.XPATH,
        "//span[contains(@class, 'title') and normalize-space()='Your Cart']"
    )

    CART_LIST = (
        By.CSS_SELECTOR,
        ".cart_list"
    )

    CART_ITEMS = (
        By.XPATH,
        "//div[contains(concat(' ', normalize-space(@class), ' '), ' cart_item ')]"
    )

    CART_BADGE = (
        By.CSS_SELECTOR,
        ".shopping_cart_badge"
    )

    BACKPACK_CART_ITEM = (
        By.XPATH,
        "//div[contains(concat(' ', normalize-space(@class), ' '), ' cart_item ')]"
        "[.//div[normalize-space()='Sauce Labs Backpack']]"
    )

    REMOVE_BACKPACK_BUTTON = (
        By.CSS_SELECTOR,
        "[data-test='remove-sauce-labs-backpack']"
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
        self.wait.until(EC.url_contains(self.CART_URL_FRAGMENT))
        self.wait.until(EC.visibility_of_element_located(self.CART_TITLE))
        self.wait.until(EC.visibility_of_element_located(self.CART_LIST))
        # Tunggu sampai isi keranjang selesai dirender oleh React.
        self._wait_for_cart_state()

    def _get_badge_count(self):
        badges = self.driver.find_elements(*self.CART_BADGE)
        if not badges:
            return 0
        text = badges[0].text.strip()
        return int(text) if text.isdigit() else 0

    def _wait_for_cart_state(self):
        """Menunggu jumlah item keranjang sesuai dengan badge keranjang."""
        self.wait.until(
            lambda _: len(self.driver.find_elements(*self.CART_ITEMS))
            == self._get_badge_count()
        )

    def is_cart_displayed(self):
        return self.find_element(self.CART_TITLE).is_displayed()

    def get_cart_item_count(self):
        self._wait_for_cart_state()
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def remove_backpack(self):
        self._wait_for_cart_state()
        self.click(self.REMOVE_BACKPACK_BUTTON)
        self.wait.until(
            EC.invisibility_of_element_located(self.REMOVE_BACKPACK_BUTTON)
        )
        # Pastikan baris produk Backpack benar-benar hilang dari DOM.
        self.wait.until(
            lambda _: len(
                self.driver.find_elements(*self.BACKPACK_CART_ITEM)
            ) == 0
        )
        self._wait_for_cart_state()

    def click_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
