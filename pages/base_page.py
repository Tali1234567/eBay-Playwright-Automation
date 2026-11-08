
import re
from playwright.async_api import Page


class BasePage:

    def __init__(self, page: Page):
        self.page = page

        # Shipping popup ("Are you shipping to ...?")
        self.shipping_popup = self.page.get_by_role(
            "dialog",
            name=re.compile("Are you shipping to")
        )

        self.shipping_popup_close = self.shipping_popup.get_by_role(
            "button",
            name="Dismiss"
        )

    # Registers an automatic handler to close the shipping popup
    async def register_popup_handler(self):

        await self.page.add_locator_handler(
            self.shipping_popup,
            self._dismiss_shipping_popup
        )

    # Closes the shipping popup automatically when it appears
    async def _dismiss_shipping_popup(self):

        await self.shipping_popup_close.click()

        await self.shipping_popup.wait_for(state="hidden")
