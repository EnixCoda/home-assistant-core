"""Config flow for the freemax integration."""

from __future__ import annotations

import logging
from random import randint
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow as HAConfigFlow, ConfigFlowResult
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


def get_default_title(hass: HomeAssistant) -> str:
    """Get a default title for the integration."""
    entities = hass.states.async_all(domain_filter=DOMAIN)
    return f"{DOMAIN} Gateway ({len(entities) + 1})"


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""

    # find entities from same domain
    title = data.get("title", "").strip()
    if not title or not isinstance(title, str):
        title = get_default_title(hass)

    return {
        "title": title,
    }


class ConfigFlow(HAConfigFlow, domain=DOMAIN):
    """Handle a config flow for freemax."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                identifier = DOMAIN + "_config_flow_" + str(randint(1000, 9999))
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

        STEP_USER_DATA_SCHEMA = vol.Schema(
            {
                vol.Optional("title", default=get_default_title(self.hass)): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
