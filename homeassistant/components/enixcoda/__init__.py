"""The itg1 integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryError, ConfigEntryNotReady

# For your initial PR, limit it to 1 platform.
_PLATFORMS: list[Platform] = [Platform.BUTTON]


class MyApi:
    """Placeholder for your API class."""

    # Define your API methods and properties here


type New_NameConfigEntry = ConfigEntry[MyApi]


async def async_setup_entry(hass: HomeAssistant, entry: New_NameConfigEntry) -> bool:
    """Set up itg1 from a config entry."""

    def _raise_config_entry_error() -> None:
        """Raise ConfigEntryError for failed API validation."""
        raise ConfigEntryError("Failed to validate API connection")

    # 1. Create API instance
    api = MyApi()

    # 2. Validate the API connection (and authentication)
    try:
        # Replace with actual async validation call, e.g. await api.async_validate()
        # For now, simulate success/failure:
        validated = True  # Set to False to simulate failure
        if not validated:
            _raise_config_entry_error()
    except Exception as err:
        raise ConfigEntryNotReady(f"Could not connect to API: {err}") from err

    # 3. Store an API object for your platforms to access
    entry.runtime_data = api

    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: New_NameConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)
