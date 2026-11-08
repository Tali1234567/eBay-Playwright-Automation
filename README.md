# eBay E2E Automation Project

## Project Overview

This project is an end-to-end (E2E) test automation framework built with Python, Playwright, and Pytest.

The project automates an eBay shopping workflow, including product search, price filtering, collecting product URLs, adding selected products to the shopping cart, and validating the cart subtotal against a predefined budget.

The framework uses the Page Object Model (POM) design pattern to separate test logic from page-specific actions and locators.

## Technologies

- **Python** – Programming language
- **Playwright** – Browser automation
- **Pytest** – Test execution and assertions
- **Pytest-Asyncio** – Asynchronous test support
- **PyYAML** – Test configuration and data management
- **Allure** – Test execution reports and attachments
- **Git** – Version control

## Project Structure

```text
project/
│
├── data/
│   └── test_data.yaml
│
├── pages/
│   ├── base_page.py
│   ├── search_page.py
│   ├── product_page.py
│   ├── cart_page.py
│   └── login_page.py
│
├── tests/
│   ├── conftest.py
│   └── test_e2e_cart.py
│
├── utils/
│   └── config_reader.py
│
├── requirements.txt
├── pytest.ini
└── README.md
```

## Framework Architecture

The project follows the Page Object Model (POM) design pattern.

- **BasePage** – Contains shared page functionality and common popup handling.
- **SearchPage** – Handles product searches, price filtering, product information extraction, and navigation between search result pages.
- **ProductPage** – Handles navigation to product pages and adding products to the shopping cart.
- **CartPage** – Handles cart navigation and subtotal validation.
- **LoginPage** – Contains the eBay login flow implementation. It is not currently integrated into the main E2E test due to additional eBay security verification requirements.
- **ConfigReader** – Loads test configuration from the YAML file.
- **conftest.py** – Provides the browser fixture, initializes Playwright, configures the browser context, registers the shared popup handler, and manages screenshots and traces.
- **test_e2e_cart.py** – Contains the main end-to-end test scenario.

## Test Configuration

Test parameters are maintained in `data/test_data.yaml`, allowing test data to be changed without modifying the test implementation.

Example configuration:

```yaml
test:
  name: "eBay product search and cart validation"

  search:
    query: "shoes"
    max_price: 220
    limit: 5

  cart:
    budget_per_item: 220

website:
  base_url: "https://www.ebay.com"

browser:
  headless: false
  timeout: 30000

execution:
  screenshot_on_success: true
  screenshot_on_failure: true
  trace: true
```

## Prerequisites

Before running the project, make sure the following are installed:

- Python 3.10 or higher
- pip
- Playwright-supported browsers
- Allure Commandline (required only for viewing Allure reports)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Tali1234567/eBay-Playwright-Automation.git
   ```

2. Navigate to the project directory:

   ```bash
   cd <PROJECT_DIRECTORY>
   ```

3. Install the required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install the Playwright Chromium browser:

   ```bash
   playwright install chromium
   ```

## Running the Tests

Run the tests using:

```bash
pytest -v
```

To run a specific test:

```bash
pytest -v tests/test_e2e_cart.py
```

The browser runs in headed mode by default. This can be changed in `data/test_data.yaml`.

## Test Scenario

The main E2E test performs the following steps:

1. Launches the Chromium browser.
2. Navigates to eBay.
3. Loads the test parameters from the YAML configuration file.
4. Searches for products using the configured search query.
5. Applies the maximum price filter when available.
6. Collects product URLs that match the configured price limit.
7. Verifies that at least one product was found.
8. Verifies that the number of collected products does not exceed the configured limit.
9. Validates that the collected URLs are valid.
10. Navigates to each selected product page and attempts to add the product to the shopping cart.
11. Opens the shopping cart.
12. Extracts the cart subtotal and validates that it does not exceed the configured budget.

## Test Reports and Execution Artifacts

The project includes support for generating test execution reports in Allure and JUnit XML formats. HTML reporting is also available through the optional pytest-html plugin.

### Allure Report

Run the tests and generate Allure results:

```bash
pytest -v --alluredir=reports/allure-results --clean-alluredir
```

Open the Allure report:

```bash
allure serve reports/allure-results
```

Screenshots and Playwright traces are attached to the Allure report when enabled in the YAML configuration.

**Note:** The Allure Python package and Allure Commandline must be installed separately.

### HTML Report

Install the HTML reporting plugin if it is not already included in `requirements.txt`:

```bash
pip install pytest-html
```

Run:

```bash
pytest --html=reports/report.html --self-contained-html
```

### JUnit XML Report

Run:

```bash
pytest --junitxml=reports/junit.xml
```

JUnit XML can be used by CI/CD systems to collect and display test results.

## Screenshots and Playwright Traces

The framework supports automatic screenshot capture based on the test execution result and configuration.

Playwright tracing can also be enabled to capture browser activity, including:

- Browser actions
- DOM snapshots
- Screenshots
- Source information

Trace files are saved under `reports/traces/`.

These artifacts can help investigate failures and understand the browser's behavior during test execution.

## Authentication – Known Limitation

A dedicated `LoginPage` class contains the eBay login flow implementation.

However, the login flow is not currently integrated into the main E2E test scenario because eBay may require additional security verification, such as email or SMS verification.

This prevents the login process from being reliably automated in the current implementation.

## Known Limitations and Environment Constraints

### eBay Production Website Restrictions

During development, it became apparent that eBay's production website may restrict automated browser activity.

As a result, full and repeatable E2E execution against the production website could not be reliably verified.

These restrictions may affect navigation and other automated actions.

### Locator Validation Status

Not all page elements and locators have been fully validated through successful test execution.

Due to eBay's restrictions on automated browser activity and additional security verification, some locators and interactions could not be verified in a complete end-to-end run.

Further validation is required to ensure compatibility with the current website structure.

### eBay Sandbox Environment

The project was initially developed against eBay's production website.

Only at a later stage of development did I identify that eBay provides a dedicated Sandbox environment for developers and testing.

The Sandbox environment is designed for testing eBay functionalities using separate test accounts and simulated data. However, it also has limitations, and not all Production website features are fully supported. In particular, product search and shopping cart functionality may have limitations.

Therefore, switching to the Sandbox environment would not necessarily resolve all the automation challenges encountered during this project.

Migration to the Sandbox environment was not completed as part of this project.

## Future Improvements

- Migrate the tests to eBay's Sandbox environment.
- Integrate a reliable authentication mechanism where supported.
- Improve product selection to handle different product variations.
- Add validation that confirms each selected product was successfully added to the cart.
- Improve price extraction to support different price formats and currencies.
- Integrate the test suite into a CI/CD pipeline.

## Author

**Tali Bendelac**