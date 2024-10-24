from datetime import datetime
from dateutil.relativedelta import relativedelta

from teacher_data_processing.tool import func as tch_proc_func


def get_age_from_citizen_id(citizen_id: str) -> int:
    """
    通过身份证号计算当前年龄
    :param citizen_id: 身份证号
    :return: 年龄
    """

    if len(citizen_id) != 18:
        return 0

    try:
        return abs(
            relativedelta(
                datetime(
                    year=int(citizen_id[6:10]),
                    month=int(citizen_id[10:12]),
                    day=int(citizen_id[12:14])
                ),
                datetime.today()
            ).years
        )

    except Exception as e:
        tch_proc_func.print_color_text(text=f"{e}:{citizen_id}")
        return -1


if __name__ == '__main__':

    str1 = "440000200102220000"

    print(get_age_from_citizen_id(citizen_id=str1))
