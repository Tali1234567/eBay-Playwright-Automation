import re
import os
from pathlib import Path

import allure
import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv

from utils.config_reader import ConfigReader
from pages.base_page import BasePage

# Load environment variables from .env
load_dotenv()

# Verify that eBay credentials were loaded
assert os.getenv("EBAY_APP_ID"), "EBAY_APP_ID is missing"
assert os.getenv("EBAY_CERT_ID"), "EBAY_CERT_ID is missing"
assert os.getenv("EBAY_DEV_ID"), "EBAY_DEV_ID is missing"

print("eBay credentials loaded successfully")

# Save the result of each test phase.
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


# Provides an asynchronous browser page fixture.
@pytest_asyncio.fixture
async def browser_page(request):

    # Load configuration from YAML
    config = ConfigReader.load_test_data()
    execution_config = config.get("execution", {})

    # Create report directories if they do not exist
    reports_dir = Path("reports")
    screenshots_dir = reports_dir / "screenshots"
    traces_dir = reports_dir / "traces"

    screenshots_dir.mkdir(parents=True, exist_ok=True)
    traces_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as playwright:

        # Launch Chromium browser
        browser = await playwright.chromium.launch(
            headless=config["browser"]["headless"]
        )

        try:
            # Create browser context and page
            context = await browser.new_context()
            page = await context.new_page()

            # Set the default timeout
            page.set_default_timeout(config["browser"]["timeout"])

            # Register the shipping popup handler
            base_page = BasePage(page)
            await base_page.register_popup_handler()

            # Start tracing if enabled in YAML
            if execution_config.get("trace", False):
                await context.tracing.start(
                    screenshots=True,
                    snapshots=True,
                    sources=True
                )

            # Provide the page to the test
            yield page

        finally:
            # Get the test execution result
            report = getattr(request.node, "rep_call", None)

            # Determine whether a screenshot should be captured
            should_take_screenshot = (
                report is not None
                and (
                    (report.passed and execution_config.get("screenshot_on_success", False))
                    or
                    (report.failed and execution_config.get("screenshot_on_failure", False))
                )
            )

            test_name = re.sub(
                r"[^a-zA-Z0-9_-]", "_", request.node.name
            )

            # Capture and attach screenshot to Allure
            if should_take_screenshot:
                screenshot_path = screenshots_dir / f"{test_name}.png"

                screenshot_bytes = await page.screenshot(
                    path=str(screenshot_path),
                    full_page=True
                )

                allure.attach(
                    screenshot_bytes,
                    name=f"{test_name} screenshot",
                    attachment_type=allure.attachment_type.PNG
                )

            # Stop tracing and attach the trace file to Allure
            if execution_config.get("trace", False):
                trace_path = traces_dir / f"{test_name}.zip"

                await context.tracing.stop(path=str(trace_path))

                allure.attach.file(
                    str(trace_path),
                    name=f"{test_name} trace",
                    attachment_type=allure.attachment_type.ZIP
                )

            # Close browser context and browser
            await context.close()
            await browser.close()
