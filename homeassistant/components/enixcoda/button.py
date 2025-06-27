"""Button entities for sending SIP request."""

from typing import Final

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .elevator_button import ELEVATOR_DIRECTION_DOWN, ElevatorButton
from .host import Host
from .unlock_gateway_button import UnlockGatewayButton


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up button entities from a config entry."""

    server1: Final = Host(id="14009901", ip="192.168.24.2")
    server2: Final = Host(id="14009902", ip="192.168.24.3")
    server3: Final = Host(id="14009903", ip="192.168.24.4")
    client1: Final = Host(id="14002502", ip="192.168.24.57")

    async_add_entities(
        [
            ElevatorButton(
                name="1 UP",
                client=client1,
                server=server1,
                family=2,
                floor=1,
                direction=ELEVATOR_DIRECTION_DOWN,
            ),
            ElevatorButton(
                name="25 DOWN",
                client=client1,
                server=server1,
                family=2,
                floor=25,
                direction=ELEVATOR_DIRECTION_DOWN,
            ),
            UnlockGatewayButton(
                name="1", client=client1, server=server1, build=14, family=2, floor=1
            ),
            UnlockGatewayButton(
                name="2", client=client1, server=server2, build=14, family=2, floor=2
            ),
            UnlockGatewayButton(
                name="3", client=client1, server=server3, build=14, family=2, floor=3
            ),
        ]
    )
