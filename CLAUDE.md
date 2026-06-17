# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A search plugin for **dserver** (the dtool lookup server, package `dservercore`). It implements
MongoDB-backed dataset registration and search. The plugin is discovered by dserver at runtime
through the `dservercore.search` entry point declared in `pyproject.toml`:

```
[project.entry-points."dservercore.search"]
"MongoSearch" = "dserver_search_plugin_mongo.utils_search:MongoSearch"
```

This package is a *companion* to `dserver-retrieve-plugin-mongo`; search and retrieve are separate
plugins that, in the common deployment, point at the *same* MongoDB collection (see test config
where `SEARCH_MONGO_*` and `RETRIEVE_MONGO_*` use the same db name).

## Architecture

The entire plugin is one class, `MongoSearch(SearchABC)` in `dserver_search_plugin_mongo/utils_search.py`,
implementing the abstract interface from `dservercore.SearchABC`:

- `init_app(app)` — pulls `SEARCH_MONGO_URI`/`_DB`/`_COLLECTION` from Flask `app.config`, opens the
  `MongoClient`, and creates a wildcard text index (`[("$**", pymongo.TEXT)]`) so free-text search
  works across all fields. Re-running is safe; Mongo skips index recreation.
- `register_dataset(dataset_info)` — upserts a dataset record keyed on `(uuid, uri)`. Converts
  `frozen_at`/`created_at` to datetimes via `dservercore.date_utils`. Wraps
  `pymongo.errors.DocumentTooLarge` into `dservercore.ValidationError`. Also stores a parsed copy of
  the README under `readme_parsed` (see below).
- `set_tags(uri, tags)` / `set_annotations(uri, annotations)` / `set_readme(uri, readme)` —
  in-place mutators that `$set` the respective field on the matching record, raising
  `dservercore.UnknownURIError` when no record matches the `uri`. `set_readme` also re-parses and
  updates `readme_parsed`.
- `search(query, pagination_parameters, sort_parameters)` — translates the query dict to a Mongo
  query, runs `find` with a fixed projection that *excludes* `_id`, `readme`, `manifest`,
  `annotations`. Returns `[]` early when `query["base_uris"]` is empty (a user with access to no
  base URIs). Pagination sets `pagination_parameters.item_count` from `count_documents` and applies
  skip/limit; sorting maps `sort_parameters.order` items directly to pymongo sort tuples.
- `get_config` / `get_config_secrets_to_obfuscate` — expose `config.Config` and the secret list to
  dserver's `/config` route.

### Query translation (the core logic)

`_dict_to_mongo_query(query_dict)` is the heart of the plugin. Only keys in `VALID_MONGO_QUERY_KEYS`
(`free_text`, `creator_usernames`, `base_uris`, `uuids`, `tags`, `uploaded_by`) survive sanitisation;
everything else is dropped, and empty list-valued keys are removed. Semantics:

- `free_text` → `{"$text": {"$search": ...}}`
- `creator_usernames`, `base_uris`, `uuids`, `uploaded_by` → single value matches directly; multiple
  values become an `$or`.
- `tags` → single tag matches directly; multiple tags become `$all` (AND semantics).
- Multiple sub-queries are joined with `$and`; zero sub-queries returns `{}` (match all).

When changing query behavior, update both `_dict_to_mongo_query` and the corresponding standalone
tests in `tests/test_utils_search_standalone.py` (the `test_*` functions at the bottom assert exact
Mongo query dicts).

### README parsing (`readme_parsed`)

The README is stored verbatim as a string under `readme`. `_parse_readme(readme)` additionally
YAML-parses it (returning the dict, or `None` on failure / non-dict) and the result is stored under
`readme_parsed`. This enables structured queries over README content by *co-installed* plugins —
e.g. the dependency-graph plugin's `readme_parsed.derived_from.uuid` dependency key. `readme_parsed`
is written by `register_dataset` and refreshed by `set_readme`. Requires `PyYAML`.

### Configuration

`config.py` defines `Config` (env-var-backed defaults) and `CONFIG_SECRETS_TO_OBFUSCATE`. Note the
default `SEARCH_MONGO_DB` in `Config` is `"dtool_info"`, while the README example uses `"dserver"`.

## Commands

```bash
# Install for development (with test deps)
pip install .[test]

# The test extras also need the server core + retrieve plugin:
pip install dservercore dserver-retrieve-plugin-mongo

# Run the full test suite (pytest config + coverage live in pyproject.toml)
pytest

# Run a single test file / single test
pytest tests/test_utils_search_standalone.py
pytest tests/test_utils_search_standalone.py::test_combinations

# Lint (matches CI)
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 .   # full run
```

### A running MongoDB is required for most tests

Tests connect to `mongodb://localhost:27017` by default, overridable via the `MONGO_URI` env var
(used in `tests/test_utils_search_standalone.py`, `tests/conftest.py` and `tests/test_config_route.py`,
e.g. for an authenticated MongoDB). They create a randomly-named temp database per test and drop it
(and close the client) on teardown.
The pure `_dict_to_mongo_query` unit tests (`test_empty_dict`, `test_free_text`, etc.) do *not* need
Mongo, but the registration/search tests do.

The test app config also sets bare `MONGO_URI`/`MONGO_DB`/`MONGO_COLLECTION` keys (in addition to the
`SEARCH_MONGO_*` / `RETRIEVE_MONGO_*` ones) so co-installed plugins like the dependency-graph plugin
can initialise against the same temp database.

## Testing structure

- `tests/test_utils_search_standalone.py` — exercises `MongoSearch` directly via a `_MockApp` holding
  a `config` dict (no Flask). Builds real dtool datasets with `DataSetCreator` and registers them.
  This is the file to extend when changing search/registration logic.
- `tests/test_config_route.py` and `tests/conftest.py` — full Flask-app integration via
  `dservercore.create_app`. `tmp_app_with_users` builds an in-memory SQLite app with JWT users and
  permissions, wiring both retrieve and search plugins to the same temp Mongo db. Use this for
  route-level behavior (e.g. `/config/info`, `/config/versions`).
- `tests/utils.py` — `compare_nested` does partial/marked dict comparison; `make_marker` builds the
  comparison mask.

## Versioning & packaging

The build backend is **flit** (`flit_scm:buildapi`, configured in `pyproject.toml`); there is no
`setup.cfg`/`setup.py`. pytest and coverage config also live in `pyproject.toml` under
`[tool.pytest.ini_options]`.

Version is managed by `setuptools_scm` (via `flit_scm`) from git tags (`guess-next-dev`,
`no-local-version`), written to `dserver_search_plugin_mongo/version.py` (generated, not committed).
`__init__.py` resolves the version at runtime first via `importlib.metadata`, falling back to the
generated `version.py`.
Releases are tag-driven: pushing a tag triggers `.github/workflows/publish.yml` (trusted publishing
to PyPI + GitHub release + Zenodo). Update `CHANGELOG.rst` (keep-a-changelog format, semver) when
preparing a release.

## CI

`.github/workflows/test.yml` runs a matrix of Python 3.10–3.13 × MongoDB 5.0/6.0/7.0/8.0, installing
`dservercore` and `dserver-retrieve-plugin-mongo` from their `main` branches. Keep the plugin
compatible with that whole range; `pyproject.toml` declares `requires-python = ">=3.10"` to match.
