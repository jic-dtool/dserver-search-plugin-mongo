dserver Search Plugin Mongo
===========================

.. |dtool| image:: https://github.com/livMatS/dserver-search-plugin-mongo/blob/main/icons/22x22/dtool_logo.png?raw=True
    :height: 20px
    :target: https://github.com/livMatS/dserver-search-plugin-mongo
.. |pypi| image:: https://img.shields.io/pypi/v/dserver-search-plugin-mongo
    :target: https://pypi.org/project/dserver-search-plugin-mongo/
.. |tag| image:: https://img.shields.io/github/v/tag/livMatS/dserver-search-plugin-mongo
    :target: https://github.com/livMatS/dserver-search-plugin-mongo/tags
.. |test| image:: https://img.shields.io/github/actions/workflow/status/livMatS/dserver-search-plugin-mongo/test.yml?branch=main&label=tests
    :target: https://github.com/livMatS/dserver-search-plugin-mongo/actions/workflows/test.yml

|dtool| |pypi| |tag| |test|

Search plugin for *dserver* using mongodb

To install the ``dserver-search-plugin-mongo`` package.

.. code-block:: bash

    cd dserver-search-plugin-mongo
    pip install .

To configure the connection to the mongo database.

.. code-block:: bash

    export SEARCH_MONGO_URI="mongodb://localhost:27017/"
    export SEARCH_MONGO_DB="dserver"
    export SEARCH_MONGO_COLLECTION="datasets"

Testing
^^^^^^^

Testing requires a minimal ``dserver`` installation including a
functional retrieve plugin, i.e.

.. code-block:: bash

    pip install dtool-lookup-server
    pip install dserver-retrieve-plugin-mongo

Installation with the ``[test]`` extension

.. code-block:: bash

    pip install .[test]

installs these essential testing dependencies as well.

Run tests from within repository root with ``pytest``.