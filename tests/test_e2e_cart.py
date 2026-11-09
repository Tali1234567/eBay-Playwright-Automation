import os
import pytest

from pages.login_page import LoginPage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utils.config_reader import ConfigReader


# E2E test: searches for products, adds them to the cart and validates the total
@pytest.mark.asyncio
async def test_search_products_and_validate_cart(browser_page):

    # Load test data from YAML
    config = ConfigReader.load_test_data()

    # Navigate to eBay Sandbox
    await browser_page.goto(config["website"]["base_url"])

    # Load Sandbox credentials from environment variables
    username = os.getenv("EBAY_SANDBOX_USERNAME")
    password = os.getenv("EBAY_SANDBOX_PASSWORD")

    assert username, "EBAY_SANDBOX_USERNAME is missing"
    assert password, "EBAY_SANDBOX_PASSWORD is missing"

    # Create LoginPage object
    login_page = LoginPage(browser_page)

    # Sign in with Sandbox test user
    await login_page.login(username, password)

    # Create SearchPage object
    search_page = SearchPage(browser_page)

    # Search for products and collect matching URLs
    product_urls = await search_page.search_items_by_name_under_price(config)

    # Get the expected maximum number of products
    limit = config["test"]["search"].get("limit", 5)

    # Verify that at least one product was found
    assert len(product_urls) > 0, "No products were found"

    # Verify that the number of products does not exceed the limit
    assert len(product_urls) <= limit, (
        f"Expected up to {limit} products, but got {len(product_urls)}"
    )

    # Verify that all collected URLs are valid HTTPS URLs
    assert all(
        url.startswith("https://") for url in product_urls
    ), "One or more product URLs are invalid"

    # Create ProductPage object
    product_page = ProductPage(browser_page)

    # Add the selected products to the shopping cart
    await product_page.add_items_to_cart(product_urls)

    # Create CartPage object
    cart_page = CartPage(browser_page)

    # Verify that the cart total does not exceed the allowed budget
    await cart_page.assert_cart_total_not_exceeds(
        float(config["test"]["cart"]["budget_per_item"]),
        len(product_urls)
    )
