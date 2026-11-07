from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class InventoryPage(BasePage):
    """Page Object untuk halaman Inventory SauceDemo."""

    INVENTORY_TITLE = (
        By.XPATH,
        "//span[@data-test='title' and normalize-space()='Products']"
    )

    INVENTORY_ITEMS = (
        By.XPATH,
        "//div[@data-test='inventory-item']"
    )

    
    ADD_BACKPACK_BUTTON = (
        By.XPATH,
        "//button[contains(@data-test, 'add-to-cart-sauce-labs-backpack')]"
    )

    
    CART_BADGE = (
        By.XPATH,
        "//span[@data-test='shopping-cart-badge']"
    )

  
    BURGER_MENU_BUTTON = (
        By.XPATH,
        "//button[@id='react-burger-menu-btn']"
    )

    
    LOGOUT_LINK = (
        By.XPATH,
        "//a[@id='logout_sidebar_link']"
    )

    def is_page_displayed(self):
        return self.find_element(self.INVENTORY_TITLE).is_displayed()

    def get_product_count(self):
        self.wait.until(EC.visibility_of_element_located(self.INVENTORY_ITEMS))
        return len(self.driver.find_elements(*self.INVENTORY_ITEMS))

    def add_backpack_to_cart(self):
        self.click(self.ADD_BACKPACK_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.CART_BADGE))

    def get_cart_badge_count(self):
        return self.get_text(self.CART_BADGE)

    def logout(self):
        self.click(self.BURGER_MENU_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.LOGOUT_LINK))
        self.click(self.LOGOUT_LINK)