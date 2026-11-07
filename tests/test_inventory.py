
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class TestInventory:

    def login_to_inventory(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        return InventoryPage(driver)

    def test_add_to_cart_flow(self, driver):
        """TC-INV-01: Memastikan Backpack berhasil ditambahkan ke keranjang."""

        inventory_page = self.login_to_inventory(driver)

        # Menambahkan produk Backpack
        inventory_page.add_backpack_to_cart()

        # Assertion: Badge keranjang harus menunjukkan angka 1
        actual_badge = inventory_page.get_cart_badge_count()

        assert actual_badge == "1", (
            f"Jumlah badge seharusnya 1, tetapi mendapatkan {actual_badge}"
        )

    def test_logout_flow(self, driver):
        """TC-INV-02: Memastikan pengguna berhasil logout."""

        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)

        # Melakukan logout
        inventory_page.logout()

        # Assertion 1: Memastikan kembali ke URL login
        expected_url = "https://www.saucedemo.com/"
        actual_url = login_page.get_current_url()

        assert actual_url == expected_url, (
            f"URL tidak sesuai. Diharapkan {expected_url}, "
            f"tetapi mendapatkan {actual_url}"
        )

        # Assertion 2: Memastikan tombol login tampil kembali
        assert login_page.find_element(
            login_page.LOGIN_BUTTON
        ).is_displayed(), "Tombol login tidak tampil setelah logout."
