"""Tests main conftest file."""
import sys
import warnings

from pytest_mongo import factories

if not sys.version_info >= (3, 5):
    warnings.simplefilter("error", category=DeprecationWarning)

# pylint:disable=invalid-name
mongo_params = '--nojournal --noauth --nohttpinterface --noprealloc'

mongo_proc2 = factories.mongo_proc(port=27070, params=mongo_params)
mongodb2 = factories.mongodb('mongo_proc2')

mongo_proc3 = factories.mongo_proc(port=27071, params=mongo_params)
mongodb3 = factories.mongodb('mongo_proc3')

mongo_proc_rand = factories.mongo_proc(port=None, params=mongo_params)
mongodb_rand = factories.mongodb('mongo_proc_rand')
# pylint:enable=invalid-name
