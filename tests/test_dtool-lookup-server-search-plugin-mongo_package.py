"""Test the dtool_lookup_server_search_plugin_mongo package."""


def test_version_is_string():
    import dtool_lookup_server_search_plugin_mongo
    assert isinstance(dtool_lookup_server_search_plugin_mongo.__version__, str)
