# Copyright (C) 2013 by Clearcode <http://clearcode.cc>
# and associates (see AUTHORS).

# This file is part of pytest-mongo.

# pytest-mongo is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pytest-mongo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with pytest-mongo.  If not, see <http://www.gnu.org/licenses/>.
"""Fixture factories."""
from tempfile import gettempdir

import pytest
import pymongo
from path import Path
from mirakuru import TCPExecutor

from pytest_mongo.port import get_port


def get_config(request):
    """Return a dictionary with config options."""
    config = {}
    options = ['exec', 'host', 'port', 'params', 'logsdir']
    for option in options:
        option_name = 'mongo_' + option
        conf = request.config.getoption(option_name) or \
            request.config.getini(option_name)
        config[option] = conf
    return config


def mongo_proc(
        executable=None, params=None,
        host=None, port=-1,
        logsdir=None
):
    """
    Mongo process fixture factory.

    .. note::
        `mongod <http://docs.mongodb.org/v2.2/reference/mongod/>`_

    :param str executable: path to mongod
    :param str params: params
    :param str host: hostname
    :param str|int|tuple|set|list port:
        exact port (e.g. '8000', 8000)
        randomly selected port (None) - any random available port
        [(2000,3000)] or (2000,3000) - random available port from a given range
        [{4002,4003}] or {4002,4003} - random of 4002 or 4003 ports
        [(2000,3000), {4002,4003}] -random of given range and set
    :param str logsdir: path to store log files.
    :rtype: func
    :returns: function which makes a mongo process
    """
    @pytest.fixture(scope='session')
    def mongo_proc_fixture(request):
        """
        Mongodb process fixture.

        :param FixtureRequest request: fixture request object
        :rtype: mirakuru.TCPExecutor
        :returns: tcp executor
        """
        config = get_config(request)
        tmpdir = Path(gettempdir())

        mongo_exec = executable or config['exec']
        mongo_params = params or config['params']

        mongo_host = host or config['host']
        mongo_port = get_port(port) or get_port(config['port'])

        mongo_logsdir = Path(logsdir or config['logsdir'])
        mongo_logpath = Path(mongo_logsdir) / 'mongo.{port}.log'.format(
            port=mongo_port
        )
        mongo_db_path = tmpdir / 'mongo.{port}'.format(
            port=mongo_port
        )
        mongo_db_path.mkdir()
        request.addfinalizer(
            lambda: mongo_db_path.exists() and mongo_db_path.rmtree()
        )

        mongo_executor = TCPExecutor(
            (
                '{mongo_exec} --bind_ip {host} --port {port}'
                ' --dbpath {dbpath} --logpath {logpath} {params}'
            ).format(
                mongo_exec=mongo_exec,
                params=mongo_params,
                host=mongo_host,
                port=mongo_port,
                dbpath=mongo_db_path,
                logpath=mongo_logpath,
            ),
            host=mongo_host,
            port=mongo_port,
        )
        mongo_executor.start()

        request.addfinalizer(mongo_executor.stop)

        return mongo_executor

    return mongo_proc_fixture


def mongodb(process_fixture_name):
    """
    Mongo database factory.

    :param str process_fixture_name: name of the process fixture
    :rtype: func
    :returns: function which makes a connection to mongo
    """
    @pytest.fixture
    def mongodb_factory(request):
        """
        Client fixture for MongoDB.

        :param FixtureRequest request: fixture request object
        :rtype: pymongo.connection.Connection
        :returns: connection to mongo database
        """
        mongodb_process = request.getfixturevalue(process_fixture_name)
        if not mongodb_process.running():
            mongodb_process.start()

        mongo_host = mongodb_process.host
        mongo_port = mongodb_process.port

        try:
            client = pymongo.MongoClient
        except AttributeError:
            client = pymongo.Connection

        mongo_conn = client(mongo_host, mongo_port)

        def drop():
            for db in mongo_conn.database_names():
                for collection_name in mongo_conn[db].collection_names():
                    # Do not delete any of Mongo "system" collections
                    if not collection_name.startswith('system.'):
                        mongo_conn[db][collection_name].drop()

        drop()

        request.addfinalizer(drop)

        return mongo_conn

    return mongodb_factory


__all__ = ('mongodb', 'mongo_proc')
