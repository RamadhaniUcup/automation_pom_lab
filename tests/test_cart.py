
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


class TestCart:

    def login_and_add_product(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)
        inventory_page.add_backpack_to_cart()

        cart_page = CartPage(driver)
        cart_page.open_cart()

        return cart_page

    def test_cart_page_displayed(self, driver):
        cart_page = self.login_and_add_product(driver)

        assert cart_page.is_cart_displayed() is True

    def test_cart_product_count(self, driver):
        cart_page = self.login_and_add_product(driver)

        assert cart_page.get_cart_item_count() == 1

    def test_remove_product_from_cart(self, driver):
        cart_page = self.login_and_add_product(driver)

        cart_page.remove_backpack()

        assert cart_page.get_cart_item_count() == 0
