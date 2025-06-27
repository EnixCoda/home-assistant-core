"""The API."""

from homeassistant.config_entries import ConfigEntry

type MyConfigEntry = ConfigEntry[MyApi]


class MyApi:
    """Placeholder for your API class."""

    def __init__(self, config_entry: MyConfigEntry) -> None:
        """Initialize the API with the config entry."""
        self._config_entry = config_entry
