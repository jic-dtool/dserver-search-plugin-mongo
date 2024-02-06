"""Test the dserver_search_plugin_mongo package."""


def test_version_is_string():
    import dserver_search_plugin_mongo
    assert isinstance(dserver_search_plugin_mongo.__version__, str)
