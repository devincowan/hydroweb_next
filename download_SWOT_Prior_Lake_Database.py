help_message = """
Download products from your Hydroweb.next project (https://hydroweb.next.theia-land.fr) using EODAG (https://github.com/CS-SI/eodag)
This script is an example tuned for your last Hydroweb.next project but feel free to adapt it for future requests.
Follow these steps:
1. If not already done, install EODAG and packaging latest version using `pip install -U eodag packaging` or `conda update eodag packaging`
2a. Generate an API-Key from Hydroweb.next portal in your user settings
2b. Carefully store your API-Key
- either in your eodag configuration file (usually ~/.config/eodag/eodag.yml, automatically generated the first time you use eodag) in auth/credentials/apikey="PLEASE_CHANGE_ME"
- or in an environment variable `export EODAG__HYDROWEB_NEXT__AUTH__CREDENTIALS__APIKEY="PLEASE_CHANGE_ME"`
3. You can change download directory by modifying the variable path_out. By default, current path is used.
4. You are all set, run this script `python download_SWOT_Prior_Lake_Database.py`

For more information, please refer to EODAG Documentation https://eodag.readthedocs.io
"""
try:
    import os
    from eodag import EODataAccessGateway, SearchResult
    from eodag import __version__ as eodag_version
    from eodag import setup_logging
    from packaging import version

    assert version.parse(eodag_version) >= version.parse("2.10.0"), help_message
except ImportError:
    print(help_message)
    exit(1)

setup_logging(1)  # 0: nothing, 1: only progress bars, 2: INFO, 3: DEBUG

dag = EODataAccessGateway()

# --------------------------------------------------
# Declare the path where the file will be downloaded
# Set to /tmp if path is incorrect
path_out = os.getcwd()

if not os.path.isdir(path_out):
    path_out = "/tmp"

# ---------------------------------------------------------------------------------------------------------------------
# Use this code-block to define your search criteria. It defines a list of query-arguments dictionaries.
# Each query-arguments dictionary will be used to perform a distinct search, whose results will then be concatenated.
#   - add/remove collections using the `productType` key (one per query-arguments dictionary)
#   - add time restrictions using the `start` and `end` keys (e.g. "start": "2020-05-01" , "end": "2020-05-10T00:00:00Z",
#     UTC ISO8601 format)(one per collection/dictionary)
#   - add spatial restrictions using the "geom" key (e.g. "geom": "POLYGON ((1 43, 2 43, 2 44, 1 44, 1 43))" WKT string,
#       a bounding-box list [lonmin, latmin, lonmax, latmax] can also be passed )(one per collection/dictionary)
#   - more query arguments can be used, see
#     https://eodag.readthedocs.io/en/stable/notebooks/api_user_guide/4_search.html?#Search-parameters
#     project_query_args = [
#         {"productType":"SWOT_L2_HR_RASTER_250M_SAMPLE_V1_2","geom":"POLYGON ((-4.17 43.10,12.70 43.10,12.70 49.64,-4.17 49.64,-4.17 43.10))"}]
#
# This code-block searches for matching products in Hydroweb.next STAC API catalog. No need to modify.
#     project_search_results = SearchResult([])
#     for query_args in project_query_args:
#         project_search_results.extend(dag.search_all(**query_args))
# This command will perform a search using provided query arguments.
# - specify a collection using the `productType` key
# - add time restrictions using the `start` and `end` keys (e.g. "start": "2020-05-01" , "end": "2020-05-10T00:00:00Z",
#   UTC ISO8601 format)
# - add spatial restrictions using the "geom" key (e.g. "geom": "POLYGON ((1 43, 2 43, 2 44, 1 44, 1 43))" WKT string,
#   a bounding-box list [lonmin, latmin, lonmax, latmax] can also be passed )
# - more query arguments can be used, see
#   https://eodag.readthedocs.io/en/stable/notebooks/api_user_guide/4_search.html?#Search-parameters
search_results = dag.search_all(
    productType="SWOT_PRIOR_LAKE_DATABASE",
    start="2024-01-01T00:00:00Z",
    end="2024-02-07T23:59:59.999Z",
)
# This command actually downloads the matching products
downloaded_paths = dag.download_all(search_results, outputs_prefix=path_out)
if downloaded_paths:
    print(f"files successfully downloaded in {downloaded_paths}")
else:
    print(f"No files downloaded! Verify API-KEY and/or product search configuration.")
