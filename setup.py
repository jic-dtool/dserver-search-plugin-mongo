from setuptools import setup

url = "https://github.com/jic-dtool/dserver-search-plugin-mongo"
version = "0.2.0"
readme = open('README.rst').read()

setup(
    name="dserver-search-plugin-mongo",
    packages=["dserver_search_plugin_mongo"],
    version=version,
    description="Search plugin for dserver using mongodb",
    long_description=readme,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    author="Tjelvar Olsson",
    author_email="tjelvar.olsson@gmail.com",
    url=url,
    install_requires=[
        "pymongo",
        "dtoolcore>=3.18.0",
        "dserver",   # Add version constraints once v1 of dserver-has been released  # NOQA
    ],
    entry_points={
        "dserver.search": [
            "MongoSearch=dserver_search_plugin_mongo.utils_search:MongoSearch",  # NOQA
        ],
    },
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
