"""Button entities for Enixcoda SIP integration."""

import logging
import os
import socket
import textwrap
from typing import Final

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

_LOGGER = logging.getLogger(__name__)


class Host:
    """Class representing a SIP host."""

    def __init__(self, id: str, ip: str, port: int) -> None:
        """Initialize the SIP host."""
        self.id = id
        self.ip = ip
        self.port = port

    def host(self) -> str:
        """Return the host address in the format 'ip:port'."""
        return f"{self.ip}:{self.port}"

    def href(self) -> str:
        """Return the host address in the format 'sip:id@ip:port'."""
        return f"sip:{self.id}@{self.host()}"


async def send_sip(server: Host, client: Host, sip_payload: str) -> None:
    """Send a SIP message to the specified server."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            sip_header = make_sip_header(
                server=server,
                client=client,
                content=sip_payload,
            )
            sip_message = sip_header + "\n\n" + sip_payload
            _LOGGER.info(
                "Sending SIP message to %s:\n%s",
                server.href(),
                sip_message,
            )
            s.sendto(sip_message.encode(), (server.ip, server.port))
    except OSError as e:
        _LOGGER.error("Socket error while sending SIP message", exc_info=e)


def make_sip_header(
    server: Host,
    client: Host,
    content: str,
) -> str:
    """Create the SIP header for the message."""
    return textwrap.dedent(
        f"""
            MESSAGE {server.href()} SIP/2.0
            Via: SIP/2.0/UDP {client.host()};rport;branch=z9hG4bK{int.from_bytes(os.urandom(4), "big")}
            From: <{client.href()}>;tag={int.from_bytes(os.urandom(4), "big")}
            To: <{server.href()}>
            Call-ID: {int.from_bytes(os.urandom(4), "big")}
            CSeq: {int.from_bytes(os.urandom(2), "big")} MESSAGE
            Content-Type: text/plain
            Max-Forwards: 70
            User-Agent: DnakeVoip v1.0
            Content-Length: {str(len(content)).rjust(5, " ")}
        """
    ).strip()


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


# async def async_setup_platform(
#     hass: HomeAssistant,
#     config: ConfigType,
#     async_add_entities,
#     discovery_info: DiscoveryInfoType = None,
# ):
#     async_add_entities([ElevatorButton()])


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


ELEVATOR_DIRECTION_UP: Final = 3
ELEVATOR_DIRECTION_DOWN: Final = 4


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


server1 = Host(id="14009901", ip="192.168.24.2", port=5060)

server2 = Host(id="14009902", ip="192.168.24.3", port=5060)

server3 = Host(id="14009903", ip="192.168.24.4", port=5060)

client1 = Host(id="14002502", ip="192.168.24.57", port=5060)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Enixcoda button entities from a config entry."""
    async_add_entities(
        [
            ElevatorButton(
                "1 UP",
                client=client1,
                server=server2,
                family=2,
                floor=1,
                direction=ELEVATOR_DIRECTION_UP,
            ),
            ElevatorButton(
                "25 DOWN",
                client=client1,
                server=server2,
                family=2,
                floor=25,
                direction=ELEVATOR_DIRECTION_DOWN,
            ),
            UnlockGatewayButton(
                "1", client=client1, server=server1, build=14, family=2, floor=1
            ),
            UnlockGatewayButton(
                "2", client=client1, server=server2, build=14, family=2, floor=2
            ),
            UnlockGatewayButton(
                "3", client=client1, server=server3, build=14, family=2, floor=3
            ),
        ]
    )
