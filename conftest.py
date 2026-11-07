
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def driver():
    """Inisialisasi browser Google Chrome untuk setiap fungsi pengujian."""
    options = Options()

    options.add_argument("--log-level=3")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    yield driver

    # Menutup browser setelah pengujian selesai
    driver.quit()
