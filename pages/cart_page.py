
import re

from playwright.async_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        # Locators
        self.cart_button = self.page.locator("#gh-cart-n")
        self.subtotal = self.page.locator(
            '[data-test-id="SUBTOTAL"]'
        )

    # Verifies that the cart total does not exceed the allowed budget
    async def assert_cart_total_not_exceeds(
        self,
        budget_per_item: float,
        items_count: int
    ):

        # Opens the shopping cart
        await self.cart_button.click()

        # Waits for the cart page to load
        await self.page.wait_for_load_state("domcontentloaded")

        # Waits for the subtotal to become visible
        await self.subtotal.wait_for(state="visible")

        # Extracts the subtotal text
        subtotal_text = await self.subtotal.inner_text()

        # Removes currency symbols and other non-numeric characters
        clean_total = re.sub(r"[^\d.]", "", subtotal_text)

        # Checks that a valid price was extracted
        assert clean_total, (
            f"Could not extract cart subtotal from: {subtotal_text}"
        )

        # Converts the subtotal to a numeric value
        total = float(clean_total)

        # Calculates the maximum allowed cart total
        threshold = budget_per_item * items_count

        # Verifies that the cart total is within the allowed budget
        assert total <= threshold, (
            f"Cart total {total} exceeds allowed budget {threshold}"
        )
