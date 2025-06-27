"""Base class for SIP buttons."""

import logging

from homeassistant.components.button import ButtonEntity

from .host import Host
from .sip import send_sip

_LOGGER = logging.getLogger(__name__)


# pylint: disable=hass-enforce-class-module
class SIPButton(ButtonEntity):
    """Base class for SIP buttons."""

    def __init__(self, name: str, id: str, client: Host, server: Host) -> None:
        """Initialize the SIP button."""
        self._attr_name = name
        self._attr_unique_id = id
        self.client = client
        self.server = server

    def make_sip_message(self) -> str:
        """Create the SIP message to be sent when the button is pressed."""
        raise NotImplementedError("Subclasses must implement this method")

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.info("SIP button pressed")
        await send_sip(self.server, self.client, self.make_sip_message())
        _LOGGER.info("SIP button action completed")
