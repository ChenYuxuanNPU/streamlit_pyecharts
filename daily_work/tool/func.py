import json
import sqlite3
from datetime import datetime
from pathlib import Path


def get_database_name() -> str:
    """
    根据database_basic_info.json获取数据库名
    :return: 数据库名
    """

    with open(fr"{Path(__file__).resolve().parent.parent.parent}\json_file\database\database_basic_info.json",
              "r", encoding='UTF-8') as file:  # ISO-8859-1
        loaded_data = json.load(file)

    database_name = loaded_data["database_name"]

    return database_name


# kind:"在编","编外"
def connect_database() -> tuple[sqlite3.Cursor, sqlite3.Connection]:
    """
    用于连接数据库
    :return:
    """

    conn = sqlite3.connect(
        fr"{Path(__file__).resolve().parent.parent.parent}\database\{get_database_name()}"
    )
    c = conn.cursor()

    return c, conn


def disconnect_database(conn) -> None:
    """
    用于断开数据库
    :param conn:
    :return:
    """

    conn.close()

    return None


def print_color_text(text: str | int | float, color_code='\033[1;91m', reset_code='\033[0m') -> None:
    """
    输出带颜色的字符串，可以用于控制台警告
    :param text: 输出的文本
    :param color_code: 颜色起始代码
    :param reset_code: 颜色结束代码
    :return: 无
    """

    print(f"{color_code}{str(text)}{reset_code}")

    return None


def execute_sql_sentence(sentence: str, ) -> list:
    """
    执行数据库语句并返回列表
    :param sentence: 需要执行的语句
    :return:
    """

    print("")
    start_time = datetime.now()
    # print(f'执行前时间：{start_time.strftime("%H:%M:%S")}')

    c, conn = connect_database()

    try:
        print_color_text(text=f'正在执行：{sentence}', color_code='\033[1;96m')
        c.execute(sentence)

        conn.commit()

    except Exception as e:
        conn.rollback()

        print_color_text(text=str(e))
        print_color_text(text=sentence)

    finally:
        result = c.fetchall()

        disconnect_database(conn=conn)

        end_time = datetime.now()

        # print(f'执行后时间：{end_time.strftime("%H:%M:%S")}')
        print(f'耗时：{(end_time - start_time).total_seconds()}')

    return result


def load_json_data(folder: str, file_name: str) -> dict:
    """
    根据文件夹名和json文件名读取json文件中的数据
    :param folder: json_file下的文件夹名
    :param file_name: 文件夹内的json文件名（不带json后缀）
    :return: dict型数据
    """

    json_data = {}

    try:
        with open(fr"{Path(__file__).resolve().parent.parent.parent}\json_file\{folder}\{file_name}.json",
                  "r", encoding="UTF-8") as f:
            json_data = json.load(f)

    except Exception as e:
        print(f"{e}")

    finally:
        return json_data


def del_tuple_in_list(data: list) -> list:
    """
    将形如[('1',), ('2',), ('3',),]的数据转化为[1, 2, 3,]
    :param data:带有元组的列表
    :return: 清洗后的列表
    """

    if not data or not data[0]:
        return []

    if not isinstance(data[0], tuple):
        return data

    output = []

    output.extend(single_data[0] for single_data in data)

    return output
