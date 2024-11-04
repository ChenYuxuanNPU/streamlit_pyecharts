from datetime import datetime

from dateutil.relativedelta import relativedelta

from teacher_data_processing.tool import func as tch_proc_func


def get_age_from_citizen_id(citizen_id: str, year: str = None, month: int = 9, day: int = 1) -> int:
    """
    通过身份证号计算当前年龄或截止某一年某一月某一日（默认某一年的9月1日）\n
    get_age_from_citizen_id(citizen_id = "440105200102220000") -> 23
    :param citizen_id: 身份证号
    :param year: 截止年份
    :param month: 截止月份
    :param day: 截止日期
    :return: 年龄,两位数int
    """

    if len(citizen_id) != 18:
        return -1

    try:
        if year is None:
            return max(
                relativedelta(
                    dt1=datetime.today(),
                    dt2=datetime(
                        year=int(citizen_id[6:10]),
                        month=int(citizen_id[10:12]),
                        day=int(citizen_id[12:14])
                    )
                ).years,
                0
            )

        elif 2000 <= int(year) <= 3000:
            return max(
                relativedelta(
                    dt1=datetime(year=int(year), month=month, day=day),
                    dt2=datetime(
                        year=int(citizen_id[6:10]),
                        month=int(citizen_id[10:12]),
                        day=int(citizen_id[12:14])
                    )

                ).years,
                0
            )

        else:
            return -2

    except Exception as e:
        tch_proc_func.print_color_text(text=f"{e}:{citizen_id}")
        return -3


if __name__ == '__main__':
    str1 = "440000200102220000"

    print(get_age_from_citizen_id(citizen_id=str1, year="2002"))
