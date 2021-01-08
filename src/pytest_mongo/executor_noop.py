"""MongoDB Noop executor providing connection details for mongodb client."""
import pymongo


class NoopExecutor:  # pylint: disable=too-few-public-methods
    """
    Nooperator executor.

    This executor actually does nothing more than provide connection details
    for existing MongoDB server. I.E. one already started either on machine
    or with the use of containerisation like kubernetes or docker compose.
    """

    def __init__(self, host, port):
        """
        Initialize nooperator executor mock.

        :param str host: MongoDB hostname
        :param str|int port: MongoDB port
        """
        self.host = host
        self.port = int(port)
        self._version = None

    @property
    def version(self):
        """Get MongoDB's version."""
        if not self._version:
            client = pymongo.MongoClient(host=self.host, port=self.port)
            server_info = client.server_info()
            self._version = server_info["version"]
        return self._version
