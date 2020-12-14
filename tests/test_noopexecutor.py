"""Test for NoopExecutor."""

from pytest_mongo.executor_noop import NoopExecutor

def test_nooproc_version(mongodb):
    """Test the way mongo version is being read."""
    mongo_nooproc = NoopExecutor(
        mongodb.HOST,
        mongodb.PORT
    )
    assert mongodb.server_info()['version'] == mongo_nooproc.version


def test_nooproc_cached_version(mongodb):
    """Test that the version is being cached."""
    mongo_nooproc = NoopExecutor(
        mongodb.HOST,
        mongodb.PORT
    )
    ver = mongo_nooproc.version
    mongodb.close()
    assert ver == mongo_nooproc.version
