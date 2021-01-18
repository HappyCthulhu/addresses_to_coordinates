import json

import geojson
from loguru import logger
import geocoder


# очищает от null и кладет в JSON
def get_data_from_xlsx_file(sheet_data):
    addresses_dict = {}
    for cell in sheet_data['F']:
        addresses_dict[cell.value] = ''
    return addresses_dict


def json_file_unpack(path_to_file):
    with open(path_to_file, encoding='utf-8') as geo_addresses_file:
        geo_addresses_dict = json.load(geo_addresses_file)
        return geo_addresses_dict


def export_in_json(data, file_name):
    with open(file_name, 'w', encoding='UTF-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


def export_in_geojson(data, fp):
    with open(fp, 'w', encoding='UTF-8') as geo_addresses_file:
        geojson.dump(data, geo_addresses_file, indent=2, ensure_ascii=False)


def get_geo(addresses_geo_dict):
    count_of_addresses = 0
    not_found_count = 0

    for address, geos in addresses_geo_dict.items():
        count_of_addresses += 1
        logger.info(f'Обработано адресов: {count_of_addresses}/{len(addresses_geo_dict.keys())}')

        if geos:
            logger.info('Гео есть:')
            logger.debug(f'Гео: {geos}')
            logger.debug(f'Адрес: {address}')
            continue

        request = geocoder.mapbox(address,
                                  key='pk.eyJ1IjoidmFsZXJpeWciLCJhIjoiY2trMDU4bzAxMGUyczJxdGdhMm1jM3MzdyJ9.dAjtACf9FA2eyRdFGk9cNQ')
        geo = request.latlng

        logger.info('Нет гео')

        if geo:

            addresses_geo_dict[address] = geo

            logger.debug(f'Гео: {geo}')
            logger.debug(f'Адрес: {address}')

        else:
            not_found_count += 1

    logger.info(f'Не найдено адресов: {not_found_count}')
    return addresses_geo_dict


def export_in_xlsx_file(data_dict, fp, work_book, sheet_ranges):
    logger.info('Начинаем сохранение координат')

    count_of_saved_coord = 0
    not_found_coord = 0

    length = len(data_dict.keys())

    for cell in sheet_ranges['F']:

        address_from_F_column = cell.value
        count_of_saved_coord += 1

        if count_of_saved_coord > 3510:
            break

        if address_from_F_column in data_dict:
            coord_list = data_dict[address_from_F_column]

            if coord_list:
                latitude = str(coord_list[0])
                longitude = str(coord_list[1])

            else:
                not_found_coord += 1
                logger.critical(f'У этого адреса нет координат: {cell.value}')
                continue

            sheet_ranges[f'T{cell.row}'] = latitude
            sheet_ranges[f'U{cell.row}'] = longitude
        else:
            logger.critical(f'Этого адреса нет в json-файле: {cell.value}')
            not_found_coord += 1

        logger.debug(f'Сохранено координат: {count_of_saved_coord}/{length}')
        logger.info(f'Не найдено значений: {not_found_coord}')
    work_book.save(fp)


def export_in_geo_json(geo_dict):
    dict_for_geo_json = {
        "type": "FeatureCollection",
        "features": [
        ]
    }

    for value, keys in geo_dict.items():
        if value and keys:
            temporary_dict = {
                "type": "Feature",
                "properties": {
                    'address': value
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        keys[0],
                        keys[1]
                    ]
                }
            }

            dict_for_geo_json['features'].append(temporary_dict)

    return dict_for_geo_json
