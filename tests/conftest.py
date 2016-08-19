"""Importing plugin in conftest to gather proper coverage."""
from pytest_mongo.plugin import pytest_addoption, mongo_proc, mongodb

__all__ = ('pytest_addoption', 'mongo_proc', 'mongodb')
