"""The implementation of the UnlockGatewayButton class, which is used to unlock a gateway in a building system."""

import textwrap

from .host import Host
from .sip_button import SIPButton


def make_unlock_sip_message(
    host_id: str,
    build: int,
    floor: int,
    family: int,
    app: str,
    event: str,
    event_url: str,
    index: int = 0,
    unit: int = 0,
) -> str:
    """Create the SIP message for unlocking the gateway."""
    return textwrap.dedent(
        f"""
            <params>
              <app>{app}</app>
              <event>{event}</event>
              <event_url>{event_url}</event_url>
              <index>{index}</index>
              <host>{host_id}</host>
              <build>{build}</build>
              <unit>{unit}</unit>
              <floor>{floor}</floor>
              <family>{family}</family>
            </params>
        """
    ).strip()


# pylint: disable=hass-enforce-class-module
class UnlockGatewayButton(SIPButton):
    """Button to unlock the gateway."""

    def __init__(
        self, name: str, client: Host, server: Host, build: int, family: int, floor: int
    ) -> None:
        """Initialize the Unlock Gateway button."""
        super().__init__(
            name="Unlock Gateway Button " + name,
            id="unlock_gateway_button" + name,
            client=client,
            server=server,
        )
        self.build = build
        self.family = family
        self.floor = floor

    def make_sip_message(self) -> str:
        """Create the SIP message for unlocking the gateway."""
        return make_unlock_sip_message(
            host_id=self.client.id,
            build=self.build,
            floor=self.floor,
            family=self.family,
            app="talk",
            event="unlock",
            event_url="/talk/unlock",
        )
