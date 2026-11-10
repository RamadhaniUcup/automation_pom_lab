
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def driver():
    """Inisialisasi browser Google Chrome untuk setiap fungsi pengujian."""
    options = Options()

    options.add_argument("--log-level=3")
    options.add_argument("--start-maximized")

    # Menonaktifkan Chrome Password Manager beserta deteksi kebocoran
    # password. Popup "Change your password" adalah UI browser (bukan DOM),
    # sehingga menutupi halaman dan menelan klik Selenium tanpa error.
    options.add_argument("--password-store=basic")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument(
        "--disable-features="
        "PasswordLeakDetection,PasswordManagerOnboarding,"
        "AutofillServerCommunication"
    )
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
            "autofill.profile_enabled": False,
            "autofill.credit_card_enabled": False,
        },
    )

    driver = webdriver.Chrome(options=options)

    yield driver

    # Menutup browser setelah pengujian selesai
    driver.quit()
