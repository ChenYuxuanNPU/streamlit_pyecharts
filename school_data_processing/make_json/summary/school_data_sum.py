from school_data_processing.read_database import update_database_data as sch_ud
from school_data_processing.tool import func as sch_proc_func


def update():

    json_data = sch_proc_func.load_json_data(folder="result", file_name="school_info")

    json_data = sch_ud.get_school_data_sum(json_data=json_data)

    sch_proc_func.save_json_data(json_data=json_data, folder="result", file_name="school_info")


if __name__ == '__main__':
    update()
