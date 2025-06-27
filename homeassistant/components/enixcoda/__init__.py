"""The itg1 integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

_PLATFORMS: list[Platform] = [Platform.BUTTON]


class MyApi:
    """Placeholder for your API class."""

    # Define your API methods and properties here


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up itg1 from a config entry."""

    api = MyApi()

    entry.runtime_data = api

    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)
