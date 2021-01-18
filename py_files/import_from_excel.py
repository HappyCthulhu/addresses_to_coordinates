import sys

from pathlib import Path
from loguru import logger
from openpyxl import load_workbook
from logging_dir.logging import set_logger, my_exception_hook
from all_functions import get_data_from_xlsx_file, export_in_json

set_logger()
sys.excepthook = my_exception_hook

work_book = load_workbook(Path('..', 'txt_files', 'Volhov.xlsx'))
sheet_ranges = work_book['Volhov']


addresses_dict = get_data_from_xlsx_file(sheet_ranges)

export_in_json(addresses_dict, Path('..', 'txt_files', 'import_addresses_from_excel.json'))
logger.debug('Экспорт завершен: Volhov.xlsx --> import_addresses_from_excel.json')
