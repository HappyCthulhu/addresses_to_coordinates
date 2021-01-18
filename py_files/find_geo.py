import sys

from pathlib import Path
from logging_dir.logging import set_logger, my_exception_hook
from all_functions import export_in_json, json_file_unpack, get_geo

set_logger()
sys.excepthook = my_exception_hook

PATH_TO_FILE = Path('..', 'txt_files', 'geo_addresses.json')
file_geo_addresses_dict = json_file_unpack(PATH_TO_FILE)

new_geo_addresses_geo_dict = get_geo(file_geo_addresses_dict)
export_in_json(new_geo_addresses_geo_dict, PATH_TO_FILE)