"""Module for representing a SIP host."""


class Host:
    """Class representing a SIP host."""

    def __init__(self, id: str, ip: str, port: int = 5060) -> None:
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
