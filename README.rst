README
======

Search plugin for dtool-lookup-server using mongodb

To install the dtool-lookup-server-search-plugin-mongo package.

.. code-block:: bash

    cd dtool-lookup-server-search-plugin-mongo
    python setup.py install

To configure the connection to the mongo database.

.. code-block:: bash

    export SEARCH_MONGO_URI="mongodb://localhost:27017/"
    export SEARCH_MONGO_DB="dtool_lookup_server"
    export SEARCH_MONGO_COLLECTION="datasets"
