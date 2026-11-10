from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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
        By.ID,
        "add-to-cart-sauce-labs-backpack"
    )

    REMOVE_BACKPACK_BUTTON = (
        By.ID,
        "remove-sauce-labs-backpack"
    )

    CART_BADGE = (
        By.CSS_SELECTOR,
        ".shopping_cart_badge"
    )

    BURGER_MENU_BUTTON = (
        By.ID,
        "react-burger-menu-btn"
    )

    SIDEBAR_MENU = (
        By.CSS_SELECTOR,
        ".bm-menu-wrap"
    )

    LOGOUT_LINK = (
        By.ID,
        "logout_sidebar_link"
    )

    LOGIN_BUTTON = (
        By.ID,
        "login-button"
    )

    LOGIN_URL = "https://www.saucedemo.com/"

    def is_page_displayed(self):
        return self.find_element(self.INVENTORY_TITLE).is_displayed()

    def get_product_count(self):
        products = self.wait.until(
            EC.visibility_of_all_elements_located(self.INVENTORY_ITEMS)
        )
        return len(products)

    def add_backpack_to_cart(self):
        """Menambahkan Backpack lalu memverifikasi hasilnya di DOM.

        Setelah klik berhasil, tombol Add to cart diganti menjadi Remove.
        Kondisi itulah yang ditunggu (bukan sekadar badge), kemudian badge
        dipastikan tampil dan berisi angka 1.
        """
        for attempt in range(3):
            self.click(self.ADD_BACKPACK_BUTTON)

            try:
                WebDriverWait(self.driver, 3).until(
                    EC.visibility_of_element_located(
                        self.REMOVE_BACKPACK_BUTTON
                    )
                )
                self.wait.until(
                    EC.text_to_be_present_in_element(self.CART_BADGE, "1")
                )
                return
            except TimeoutException:
                # Jika tombol Add to cart sudah tidak ada, klik sudah
                # diproses tetapi state tidak sesuai; jangan klik ulang.
                if not self.driver.find_elements(*self.ADD_BACKPACK_BUTTON):
                    raise
                if attempt == 2:
                    raise

    def get_cart_badge_count(self):
        return self.get_text(self.CART_BADGE).strip()

    def _is_sidebar_open(self):
        try:
            menu = self.driver.find_element(*self.SIDEBAR_MENU)
            logout_link = self.driver.find_element(*self.LOGOUT_LINK)
        except (NoSuchElementException, StaleElementReferenceException):
            return False

        try:
            return bool(
                self.driver.execute_script(
                    """
                    const menu = arguments[0];
                    const link = arguments[1];
                    const menuRect = menu.getBoundingClientRect();
                    const linkRect = link.getBoundingClientRect();

                    if (
                        menuRect.width <= 0 ||
                        menuRect.right <= 0 ||
                        menuRect.left >= window.innerWidth ||
                        linkRect.width <= 0 ||
                        linkRect.left < 0
                    ) {
                        return false;
                    }

                    const transform = window.getComputedStyle(menu).transform;
                    if (transform === 'none') return true;
                    const matrix = new DOMMatrixReadOnly(transform);
                    return Math.abs(matrix.m41) < 1 && Math.abs(matrix.m42) < 1;
                    """,
                    menu,
                    logout_link,
                )
            )
        except StaleElementReferenceException:
            return False

    def _wait_for_sidebar_animation(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda _: self._is_sidebar_open()
        )

    def _open_sidebar(self):
        for use_javascript in (False, True, True):
            if self._is_sidebar_open():
                return

            if use_javascript:
                button = self.wait.until(
                    EC.presence_of_element_located(
                        self.BURGER_MENU_BUTTON
                    )
                )
                self.driver.execute_script(
                    "arguments[0].click()", button
                )
            else:
                self.click(self.BURGER_MENU_BUTTON)

            try:
                self._wait_for_sidebar_animation(timeout=3)
                return
            except TimeoutException:
                continue

        self._wait_for_sidebar_animation(timeout=5)

    def logout(self):
        self._open_sidebar()

        logout_link = self.wait.until(
            EC.element_to_be_clickable(self.LOGOUT_LINK)
        )

        logout_link.click()
        try:
            WebDriverWait(self.driver, 3).until(
                EC.url_to_be(self.LOGIN_URL)
            )
        except TimeoutException:
            logout_link = self.wait.until(
                EC.element_to_be_clickable(self.LOGOUT_LINK)
            )
            self.driver.execute_script(
                "arguments[0].click()", logout_link
            )

        self.wait.until(EC.url_to_be(self.LOGIN_URL))
        self.wait.until(
            EC.visibility_of_element_located(self.LOGIN_BUTTON)
        )
