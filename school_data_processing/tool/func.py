import sqlite3
import json
import copy

with open(r"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\database\database_basic_info.json",
          "r", encoding='UTF-8') as file:  # ISO-8859-1
    loaded_data = json.load(file)

database_name = loaded_data["database_name"]


def connect_database():
    conn = sqlite3.connect(
        f"C:\\Users\\1012986131\\Desktop\\python\\streamlit_pyecharts\\database\\{database_name}"
    )
    c = conn.cursor()

    return c, conn


def disconnect_database(conn):
    conn.close()


def dict_assignment(route: str, value, json_data: dict):
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


def load_json_data(file_name: str):

    # 读取现有json文件
    with open(fr"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\result\{file_name}.json",
              "r", encoding="UTF-8") as f:
        json_data = json.load(f)

    return json_data


def save_json_data(json_data: dict, file_name: str):

    with open(fr"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\result\{file_name}.json",
              "w", encoding="UTF-8") as f:
        # 将生成的数据保存至json文件中
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    return 0


if __name__ == '__main__':
    pass