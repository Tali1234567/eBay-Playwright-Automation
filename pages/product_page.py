
from playwright.async_api import Page
from pages.base_page import BasePage


class ProductPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        # Locators
        self.add_to_cart_button = self.page.get_by_role(
            "button",
            name="Add to cart"
        )

    # Adds all selected products to the shopping cart
    async def add_items_to_cart(self, urls: list[str]):

        for url in urls:

            # Navigate to the product page
            await self.page.goto(url)

            # Wait for the product page to load
            await self.page.wait_for_load_state("networkidle")

            # Wait for the Add to cart button to become visible
            await self.add_to_cart_button.wait_for(
                state="visible"
            )

            # Add the product to the shopping cart
            await self.add_to_cart_button.click()
