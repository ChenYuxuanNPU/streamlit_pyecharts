from school_data_processing.make_json.summary import school_data_sum
from school_data_processing.tool import func as sch_proc_func


def get_year_list():
    return sch_proc_func.load_json_data(folder="database", file_name="database_basic_info")["list_for_update_school_info"]


if __name__ == '__main__':

    for year in get_year_list():
        school_data_sum.update(year)
