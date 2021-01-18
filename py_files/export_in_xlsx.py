from pathlib import Path
from all_functions import json_file_unpack, export_in_xlsx_file
from openpyxl import load_workbook


# TODO: Переделать JSON в geojson
PATH_TO_JSON_FILE = Path('..', 'txt_files', 'geo_addresses.json')
PATH_TO_EXCEL_FILE = Path('..', 'txt_files', 'Volhov.xlsx')

work_book = load_workbook(PATH_TO_EXCEL_FILE)
sheet_ranges = work_book['Volhov']
geo_addresses_dict = json_file_unpack(PATH_TO_JSON_FILE)
export_in_xlsx_file(geo_addresses_dict, PATH_TO_EXCEL_FILE, work_book, sheet_ranges)
