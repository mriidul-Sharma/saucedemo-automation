import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

class TestAuthentication:

    # Maps to Jira Ticket: [TC-01] Verify successful login
    def test_tc01_valid_login(self, driver):
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_cart_visible() is True
        assert inventory_page.get_page_title() == "Products"

    # Maps to Jira Ticket: [TC-02] Verify error banner for locked_out_user
    def test_tc02_locked_out_user(self, driver):
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login("locked_out_user", "secret_sauce")

        expected_error = "Epic sadface: Sorry, this user has been locked out."
        assert login_page.get_error_message() == expected_error

    # Maps to Jira Ticket: [TC-03] Verify validation error when password is empty
    def test_tc03_empty_password(self, driver):
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login("standard_user", "")

        expected_error = "Epic sadface: Password is required"
        assert login_page.get_error_message() == expected_error