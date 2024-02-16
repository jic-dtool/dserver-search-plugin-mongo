import os
from setuptools import setup
from setuptools_scm import get_version
version = get_version(root='.', relative_to=__file__)


def local_scheme(version):
    """Skip the local version (eg. +xyz of 0.6.1.dev4+gdf99fe2)
    to be able to upload to Test PyPI"""
    return ""


url = "https://github.com/jic-dtool/dserver-search-plugin-mongo"
readme = open('README.rst').read()

setup(
    name="dserver-search-plugin-mongo",
    packages=["dserver_search_plugin_mongo"],
    description="Search plugin for dserver using mongodb",
    long_description=readme,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    author="Tjelvar Olsson",
    author_email="tjelvar.olsson@gmail.com",
    use_scm_version={
        "local_scheme": local_scheme,
        "root": '.',
        "relative_to": __file__,
        "write_to": os.path.join(
            "dserver_search_plugin_mongo", "version.py"),
    },
    url=url,
    setup_requires=['setuptools_scm'],
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
