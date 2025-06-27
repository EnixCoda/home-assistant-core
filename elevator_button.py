"""The ElevatorButton class, which is used to call an elevator in a building system."""

import textwrap
from typing import Final

from .host import Host
from .sip_button import SIPButton


def make_elevator_sip_message(
    to: str,
    elev: int,
    direct: int,
    floor: int,
    family: int,
    app: str,
    event: str,
    event_url: str,
) -> str:
    """Create the SIP message for calling the elevator."""
    return textwrap.dedent(
        f"""
            <?xml version="1.0" encoding="UTF-8" ?>
            <params>
              <to>{to}</to>
              <elev>{elev}</elev>
              <direct>{direct}</direct>
              <floor>{floor}</floor>
              <family>{family}</family>
              <app>{app}</app>
              <event>{event}</event>
              <event_url>{event_url}</event_url>
            </params>
        """
    ).strip()


ELEVATOR_DIRECTION_UP: Final = 3
ELEVATOR_DIRECTION_DOWN: Final = 4


# pylint: disable=hass-enforce-class-module
class ElevatorButton(SIPButton):
    """Button to call the elevator."""

    def __init__(
        self,
        name: str,
        client: Host,
        server: Host,
        family: int,
        floor: int,
        direction: int,
    ) -> None:
        """Initialize the Elevator button."""
        super().__init__(
            name="Elevator Button " + name,
            id="elevator_button" + name,
            client=client,
            server=server,
        )
        self.family = family
        self.floor = floor
        self.direction = direction

    def make_sip_message(self) -> str:
        """Create the SIP message for calling the elevator."""
        return make_elevator_sip_message(
            to=self.server.href(),
            elev=0,
            direct=self.direction,
            floor=self.floor,
            family=self.family,
            app="elev",
            event="appoint",
            event_url="/elev/appoint",
        )
