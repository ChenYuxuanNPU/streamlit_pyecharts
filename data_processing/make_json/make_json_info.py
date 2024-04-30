from data_processing.make_json.district_and_area_data import update_data as general_data
from data_processing.make_json.school_data import update_data as school_data

if __name__ == '__main__':
    general_data.update()


def make_school_json(kind: str, school_name: str, period=None):
    school_data.update(kind=kind, school_name=school_name, period=period)
