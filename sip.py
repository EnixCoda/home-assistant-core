"""The implementation of the SIP message sending functionality."""

import logging
import os
import socket
import textwrap

from .host import Host

_LOGGER = logging.getLogger(__name__)


async def send_sip(server: Host, client: Host, sip_payload: str) -> None:
    """Send a SIP message to the specified server."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
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
            s.connect((server.ip, server.port))
            s.sendall(sip_message.encode())
            data = s.recv(4096)
            _LOGGER.debug(
                "Received response from %s: %s",
                server.href(),
                data.decode(),
            )
        except TimeoutError:
            _LOGGER.error("Timeout while sending SIP message to %s", server.href())
        except ConnectionRefusedError:
            _LOGGER.error("Connection refused by %s", server.href())
        except ConnectionResetError:
            _LOGGER.error("Connection reset by %s", server.href())
        except BrokenPipeError:
            _LOGGER.error(
                "Broken pipe error while sending SIP message to %s", server.href()
            )
        except ValueError as e:
            _LOGGER.error("Invalid SIP message format: %s", e)
        except OSError as e:
            _LOGGER.error("Failed to send SIP message", exc_info=e)
        except OSError as e:
            _LOGGER.error("Socket error while sending SIP message", exc_info=e)
        except Exception as e:
            _LOGGER.error("Unexpected error while sending SIP message: %s", e)
        finally:
            s.close()


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
