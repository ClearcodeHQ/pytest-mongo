"""Tests main conftest file."""
from pytest_mongo import factories

# pylint:disable=invalid-name
mongo_params = "--nojournal --noauth"

mongo_proc2 = factories.mongo_proc(port=27070, params=mongo_params)
mongodb2 = factories.mongodb("mongo_proc2")

mongo_proc3 = factories.mongo_proc(port=27071, params=mongo_params)
mongodb3 = factories.mongodb("mongo_proc3")

mongo_proc_rand = factories.mongo_proc(port=None, params=mongo_params)
mongodb_rand = factories.mongodb("mongo_proc_rand")
# pylint:enable=invalid-name
