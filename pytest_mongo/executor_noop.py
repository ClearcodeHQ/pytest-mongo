"""MongoDB Noop executor providing connection details for mongodb client."""

from typing import Optional

from pymongo import MongoClient


class NoopExecutor:  # pylint: disable=too-few-public-methods
    """Nooperator executor.

    This executor actually does nothing more than provide connection details
    for existing MongoDB server. I.E. one already started either on machine
    or with the use of containerisation like kubernetes or docker compose.
    """

    def __init__(self, host: str, port: int) -> None:
        """Initialize nooperator executor mock.

        :param host: MongoDB hostname
        :param port: MongoDB port
        """
        self.host = host
        self.port = port
        self._version: Optional[str] = None

    @property
    def version(self) -> str:
        """Get MongoDB's version."""
        if not self._version:
            client: MongoClient = MongoClient(host=self.host, port=self.port)
            server_info = client.server_info()
            self._version = server_info["version"]
        assert self._version
        return self._version
