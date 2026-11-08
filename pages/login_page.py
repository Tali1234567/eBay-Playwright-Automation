import re

from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        # Login page locators
        self.sign_in_button = self.page.get_by_text(
            "Sign in", exact=True
        ).first

        self.switch_account_button = self.page.get_by_text(
            "Switch account", exact=True
        ).first

        self.email_input = self.page.get_by_role(
            "textbox", name=re.compile("Email or username", re.I)
        )

        self.continue_button = self.page.get_by_role(
            "button", name="Continue", exact=True
        )

        self.password_input = self.page.get_by_label(
            re.compile("Password", re.I)
        )

        self.submit_sign_in_button = self.page.get_by_role(
            "button", name="Sign in", exact=True
        )

        # Optional sign-in prompts
        self.cancel_passkey_button = self.page.get_by_role(
            "button", name="Cancel", exact=True
        )

        self.skip_sign_in_button = self.page.get_by_role(
            "button", name="Skip for now", exact=True
        )

    # Clicks an optional button only if it appears
    async def click_if_visible(self, locator):
        try:
            await locator.wait_for(state="visible", timeout=3000)
            await locator.click()
            return True
        except PlaywrightTimeoutError:
            return False

    # Performs the complete eBay sign-in process
    async def login(self, email: str, password: str):

        # Open the sign-in page
        await self.sign_in_button.click()

        # Switch account if this option appears
        await self.click_if_visible(self.switch_account_button)

        # Enter the email address
        await self.email_input.fill(email)

        # Continue to the password step
        await self.continue_button.click()

        # Enter the password
        await self.password_input.fill(password)

        # Submit the sign-in form
        await self.submit_sign_in_button.click()

        # Close the passkey prompt if it appears
        await self.click_if_visible(self.cancel_passkey_button)

        # Skip the simplified sign-in prompt if it appears
        await self.click_if_visible(self.skip_sign_in_button)