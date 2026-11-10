# eBay E2E Automation Project

## Project Overview

This project is an End-to-End (E2E) test automation framework developed using Python, Playwright, and Pytest.

The project automates an eBay shopping workflow, including user authentication, product search, price filtering, collecting product URLs, adding selected products to the shopping cart, and validating the cart subtotal against a predefined budget.

The framework follows the Page Object Model (POM) design pattern, separating test scenarios, page-specific actions, locators, and test configuration.

The project was developed as a practical automation exercise, including implementation, debugging, troubleshooting, and investigation of eBay Production and Sandbox environments.

## Technologies

- **Python** – Programming language
- **Playwright** – Browser automation
- **Pytest** – Test execution and assertions
- **Pytest-Asyncio** – Asynchronous test support
- **PyYAML** – Test configuration and data management
- **Allure** – Test execution reporting
- **Git** – Version control

## Project Structure

```text

Ebay-Automation/
├── data/
│   └── test_data.yaml
├── pages/
│   ├── base_page.py
│   ├── cart_page.py
│   ├── login_page.py
│   ├── product_page.py
│   └── search_page.py
├── tests/
│   ├── conftest.py
│   └── test_e2e_cart.py
├── utils/
│   └── config_reader.py
├── reports/
│   ├── screenshots/
│   ├── traces/
│   └── allure-results/
├── allure-report.zip
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md
├── ReadMeAIBugs.md
└── requirements.txt
```

## Framework Architecture

The project follows the Page Object Model (POM) design pattern.

- **BasePage** – Provides shared page functionality and common popup handling.
- **LoginPage** – Implements the eBay login flow, including entering user credentials and handling additional authentication-related dialogs where applicable.
- **SearchPage** – Handles product searches, price filtering, product information extraction, and navigation between search result pages.
- **ProductPage** – Handles product page navigation and adding products to the shopping cart.
- **CartPage** – Handles cart navigation and subtotal extraction and validation.
- **ConfigReader** – Loads test configuration and test data from the YAML file.
- **conftest.py** – Provides the browser fixture, initializes Playwright, configures the browser context, registers shared popup handling, and manages screenshots and traces.
- **test_e2e_cart.py** – Contains the main E2E test scenario and coordinates the different Page Objects.

## Test Configuration

Test parameters are maintained in `data/test_data.yaml`, allowing test data to be modified without changing the test implementation.

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
  base_url: "https://sandbox.ebay.com/"

browser:
  headless: false
  timeout: 30000

execution:
  screenshot_on_success: true
  screenshot_on_failure: true
  trace: true
```

## Setup and Execution

### Requirements

- Python 3.10 or higher
- Git
- pip
- Playwright
- Chromium browser
- Java (required by Allure Commandline)
- Node.js (used to install Allure Commandline)
- Allure Commandline: `npm install -g allure-commandline`
- An eBay Sandbox account (if authentication is required)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/Tali1234567/eBay-Playwright-Automation.git
cd Ebay-Automation
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Install the Chromium browser:

```bash
playwright install chromium
```

5. Create a `.env` file in the project root using `.env.example` as a template, and fill in the values listed there. [Describe in one sentence what each variable is and where to get it.]

6. Configure the required environment variables and test settings.

### Running the Tests

Run the complete test suite:

```bash
pytest -v
```

Run the main E2E test:

```bash
pytest -v tests/test_e2e_cart.py
```

**Note:** Full end-to-end execution has not yet been successfully verified due to an issue encountered during the eBay Sandbox login stage. Results may vary depending on the availability and behavior of the eBay testing environment.

## Test Scenario

The main E2E test is designed to perform the following steps:

1. Launches the Chromium browser.
2. Navigates to the configured eBay environment.
3. Loads test parameters and credentials.
4. Initializes the login process.
5. Handles the account selection screen when applicable.
6. Enters the username and password.
7. Handles additional authentication dialogs when applicable.
8. Searches for products using the configured search query.
9. Applies the maximum price filter when available.
10. Collects product URLs matching the configured price limit.
11. Verifies that at least one product was found.
12. Verifies that the number of collected products does not exceed the configured limit.
13. Validates the collected product URLs.
14. Navigates to each selected product page and attempts to add the product to the shopping cart.
15. Opens the shopping cart.
16. Extracts the cart subtotal and validates it against the configured budget.

**Execution status:** The scenario and its individual components have been implemented, but a complete successful execution of the entire workflow has not yet been verified.

## Test Reports and Execution Artifacts

The framework is configured to support test execution reports and debugging artifacts.

### Allure Report

Run the tests (results are saved to `reports/allure-results/`):

```bash
pytest -v
```

View the report:

```bash
allure serve reports/allure-results
```
### How to View the Allure Report

1. Download `allure-report.zip` from the GitHub repository.
2. Extract the ZIP file.
3. Open PowerShell in the extracted `allure-report` folder.
4. Run the following command:

```powershell
allure open .
```

5. The Allure report will open automatically in your default web browser.

The report displays the actual test execution results, including test status and available attachments.

### Screenshots and Playwright Traces

The framework includes configurable screenshot capture and Playwright tracing for debugging purposes.

Tracing can capture:

- Browser actions
- DOM snapshots
- Screenshots
- Source information

Trace files are configured to be saved under `reports/traces/`.

These artifacts can help investigate failures and analyze browser behavior during test execution.

## Authentication – Implementation Status

A dedicated `LoginPage` class implements the eBay authentication flow.

Unlike the initial implementation, the login process has been integrated into the main E2E test scenario.

However, successful authentication has not yet been verified.

During the latest execution against the eBay Sandbox environment, the browser displayed an error page instead of the expected login form.

As a result, Playwright timed out while attempting to locate the username input field.

Although the eBay credentials were successfully loaded by the project, the execution did not reach the stage of entering the username or password.

Therefore, the current failure does not establish whether the credentials themselves are valid.

## Known Limitations and Environment Constraints

### eBay Production Website

During development, automation against eBay's Production website presented challenges, including restrictions on automated browser activity.

These restrictions affected the ability to achieve a reliable and repeatable end-to-end execution.

### eBay Sandbox Environment

During development, I identified eBay's dedicated Sandbox environment for developers and testing.

The project was subsequently configured to attempt execution against the Sandbox environment.

However, the latest execution encountered an error page during the login stage, preventing the test from proceeding.

The Sandbox environment is designed for testing eBay functionalities using separate test accounts and simulated data. It may also have limitations compared with the Production website, particularly regarding product search and shopping cart functionality.

Further investigation is required to establish a reliable execution environment.

### Locator and End-to-End Validation

Not all page elements, locators, and interactions have been fully validated through successful execution.

The latest execution stopped at the login stage, before the product search and shopping cart steps could be tested as part of a complete E2E run.

Further validation is required to confirm compatibility with the current website structure and behavior.

## Future Improvements

- Investigate and resolve the Sandbox login issue.
- Establish a reliable and repeatable test environment.
- Complete a successful end-to-end execution.
- Validate all page locators and browser interactions.
- Improve product selection to handle different product variations.
- Add explicit validation that each selected product was successfully added to the cart.
- Improve price extraction to support different price formats and currencies.
- Integrate the test suite into a CI/CD pipeline.

## Author

**Tali Bendelac**