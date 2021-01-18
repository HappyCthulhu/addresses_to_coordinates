from pathlib import Path
from all_functions import json_file_unpack, export_in_geo_json

PATH_TO_JSON_FILE = Path('..', 'txt_files', 'geo_addresses.json')
PATH_TO_GEOJSON_FILE = Path('..', 'txt_files', 'geo_json_structure.geojson')

geo_addresses_dict = json_file_unpack(PATH_TO_JSON_FILE)
geo_addresses_geo_addresses_dict = export_in_geo_json(geo_addresses_dict)
export_in_geojson(geo_addresses_geo_addresses_dict, PATH_TO_GEOJSON_FILE)