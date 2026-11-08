
import re
from playwright.async_api import Page
from pages.base_page import BasePage


class SearchPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        # Locators
        self.search_input = self.page.get_by_role(
            "combobox", name="Search for anything"
        )
        self.search_button = self.page.get_by_role(
            "button", name="Search", exact=True
        )

        self.max_price_input = (
            '//div[contains(@class, "input-wrapper")]'
            '//input[contains(@aria-label,"Maximum value")]'
        )

        self.price_apply_button = self.page.get_by_role(
            "button", name="Submit price range"
        )

        self.product_cards = '//li[contains(@class,"s-card")]'
        self.product_price = './/span[contains(@class,"s-card__price")]'
        self.product_link = './/a[contains(@class,"s-card__price")]'

        self.next_page_button = '//a[contains(@aria-label,"next")]'

    # Reads the search parameters from the YAML configuration
    def get_search_parameters(self, config: dict):

        search_config = config["test"]["search"]

        query = search_config["query"]
        max_price = float(search_config["max_price"])
        limit = search_config.get("limit")

        # Uses 5 as the default limit if no limit was provided
        if limit is None:
            limit = 5

        return query, max_price, limit

    # Performs a product search using the search input
    async def search_product(self, query: str):

        await self.search_input.fill(query)
        await self.search_button.click()

    # Wait until the search results page is loaded
        await self.page.wait_for_url("**/sch/i.html**")

    # Wait until product cards appear
        await self.page.locator(self.product_cards).first.wait_for(
        state="visible"
    )

    # Applies the maximum price filter if it exists on the page
    async def apply_max_price_filter(self, max_price: float):

        max_price_filter = self.page.locator(self.max_price_input)

        # Checks whether the maximum price field exists
        if await max_price_filter.count() > 0:

            await max_price_filter.first.fill(str(max_price))

            # Applies the price filter if the apply button exists
            if await self.price_apply_button.count() > 0:

                await self.price_apply_button.click()

                await self.page.wait_for_load_state("networkidle")

    # Extracts and converts the price of a specific product
    async def get_product_price(self, product) -> float | None:

        try:
            price_text = await product.locator(
                self.product_price
            ).inner_text()

            # Removes currency symbols and other non-numeric characters
            clean_price = re.sub(r"[^\d.]", "", price_text)

            if not clean_price:
                return None

            return float(clean_price)

        except Exception:
            return None

    # Extracts the URL of a specific product
    async def get_product_url(self, product) -> str | None:

        return await product.locator(
            self.product_link
        ).get_attribute("href")

    # Collects product URLs that match the maximum price
    # Stops when the requested number of products has been collected
    async def collect_products_under_price(
        self, max_price: float, limit: int
    ) -> list[str]:

        urls = []

        # Continues collecting products until the limit is reached
        while len(urls) < limit:

            products = self.page.locator(self.product_cards)
            count = await products.count()

            # Goes through the product cards on the current page
            for i in range(count):

                if len(urls) >= limit:
                    break

                product = products.nth(i)

                # Gets the product price
                price = await self.get_product_price(product)

                # Skips products without a valid price or above the limit
                if price is None or price > max_price:
                    continue

                # Gets the product URL
                url = await self.get_product_url(product)

                # Adds the URL only if it exists and was not collected before
                if url and url not in urls:
                    urls.append(url)

            # Stops if the requested number of products has been collected
            if len(urls) >= limit:
                break

            # Moves to the next page if available
            if not await self.go_to_next_page():
                break

        return urls

    # Navigates to the next results page if a next-page link exists
    async def go_to_next_page(self) -> bool:

        next_button = self.page.locator(self.next_page_button)

        # Checks whether a next-page link exists
        if await next_button.count() == 0:
            return False

        # Checks whether the next-page button is enabled
        if not await next_button.first.is_enabled():
            return False

        await next_button.first.click()

        await self.page.wait_for_load_state("networkidle")

        return True

    # Main function: searches for products and returns URLs within the price limit
    async def search_items_by_name_under_price(
        self, config: dict
    ) -> list[str]:

        # Reads the search parameters from the YAML configuration
        query, max_price, limit = self.get_search_parameters(config)

        # Searches for the requested product
        await self.search_product(query)

        # Applies the maximum price filter if available
        await self.apply_max_price_filter(max_price)

        # Collects product URLs that match the price condition
        urls = await self.collect_products_under_price(
            max_price, limit
        )

        return urls
