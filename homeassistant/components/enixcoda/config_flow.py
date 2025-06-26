"""Config flow for the itg1 integration."""

from __future__ import annotations

import logging
from random import randint
from typing import Any, TypedDict

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow as HAConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_SELECTOR
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        # user can input multiple strings for his client devices
        vol.Required(CONF_HOST): vol.All(
            str, vol.Length(min=1)
        ),  # Hostname or IP address of the device
        vol.Required(CONF_SELECTOR): vol.All(
            str, vol.Length(min=1)
        ),  # Selector for the client device
    }
)


class ConfigFlowData(TypedDict):
    """TypedDict for config flow data."""

    title: str
    clients: list[str]
    servers: list[str]


class PlaceholderHub:
    """Placeholder class to make tests pass."""

    def __init__(self, clients: list[str], servers: list[str]) -> None:
        """Initialize."""
        self.clients = clients
        self.servers = servers

    async def authenticate(self, username: str, password: str) -> bool:
        """Test if we can authenticate with the host."""
        return True


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> ConfigFlowData:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    # await hass.async_add_executor_job(
    #     your_validate_func, data[CONF_USERNAME], data[CONF_PASSWORD]
    # )

    # Return info that you want to store in the config entry.
    return {
        "title": "EnixCoda ITG1",
        "clients": data[CONF_SELECTOR],
        "servers": data[CONF_HOST],
    }


class ConfigFlow(HAConfigFlow, domain=DOMAIN):
    """Handle a config flow for itg1."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                identifier = "id" + str(randint(0, 999999))
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(identifier)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
