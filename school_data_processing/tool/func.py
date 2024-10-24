import copy
import json
import sqlite3

from pathlib import Path
from typing import Tuple

from teacher_data_processing.tool.func import print_color_text


def connect_database() -> Tuple[sqlite3.Cursor, sqlite3.Connection]:
    conn = sqlite3.connect(
        fr"{Path(__file__).resolve().parent.parent.parent}\database\{get_database_name()}"
    )
    c = conn.cursor()

    return c, conn


def disconnect_database(conn: sqlite3.Connection) -> None:
    conn.close()


def dict_assignment(route: str, value: str | int | list | dict | bool, json_data: dict) -> dict:
    """
    在不知道字典是否有对应路径的情况下插入数据（以尝试json_data["年份"]["全区"][“总人数”] = 100为示范）
    :param route: 数据在字典中的位置，每一层的key使用斜杠"/"分开，如f"年份/全区/总人数"
    :param value: 需要插入的数据，如100
    :param json_data: 原字典
    :return: 插入后字典
    """

    route_list = route.split("/")
    temp = json_data

    for item in route_list:
        if item is not route_list[-1]:
            if item in temp:
                temp = temp[item]

            else:
                temp[item] = {}
                temp = temp[item]

    try:
        temp[route_list[-1]] = copy.deepcopy(value)

    except Exception as e:
        print('\033[1;91m' + f"module.dict_assignment:{e}" + '\033[0m')
        print('\033[1;91m' + f"{route}路径上有奇怪的原始值" + '\033[0m')

    return json_data


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
        print_color_text(text=f"{e}")

    finally:
        return json_data


def save_json_data(json_data: dict, folder: str, file_name: str) -> None:
    """
    将dict保存到json文件中
    :param json_data: 需要保存的字典
    :param folder: 保存在json_file下的文件夹名称
    :param file_name: 保存的json文件名，不需要.json后缀
    :return: 无
    """

    with open(fr"{Path(__file__).resolve().parent.parent.parent}\json_file\{folder}\{file_name}.json",
              "w", encoding="UTF-8") as f:
        # 将生成的数据保存至json文件中
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    return None


def get_database_name() -> str:
    """
    获取数据库名
    :return:
    """
    with open(fr"{Path(__file__).resolve().parent.parent.parent}\json_file\database\database_basic_info.json",
              "r", encoding='UTF-8') as file:  # ISO-8859-1
        loaded_data = json.load(file)

    database_name = loaded_data["database_name"]

    return database_name


if __name__ == '__main__':
    pass
