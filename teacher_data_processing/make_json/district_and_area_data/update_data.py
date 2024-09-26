import json
from pathlib import Path

from teacher_data_processing.make_json.district_and_area_data import district, area, custom_data

with open(fr"{Path(__file__).resolve().parent.parent.parent}\json_file\database\database_basic_info.json",
          "r", encoding='UTF-8') as file:  # ISO-8859-1
    loaded_data = json.load(file)


def update():

    for (kind, year) in loaded_data["list_for_update_teacher_info"]:

        district.update(kind=kind, year=year)

        area.update(kind=kind, year=year)

    custom_data.update()
