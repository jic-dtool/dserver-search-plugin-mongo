README
======

Search plugin for dserver using mongodb

To install the dserver-search-plugin-mongo package.

.. code-block:: bash

    cd dserver-search-plugin-mongo
    python setup.py install

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

    pip install dserver
    pip install dserver-retrieve-plugin-mongo

Run tests from within repository root with ``pytest``.