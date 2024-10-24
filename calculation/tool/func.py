import json
from pathlib import Path

from teacher_data_processing.tool.func import print_color_text


def load_json_data(folder: str, file_name: str) -> dict | None:
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
    将dict文件覆盖至json_file下某个文件夹的某个json文件中
    :param json_data: 需要保存的dict数据
    :param folder: json_file下的文件夹名
    :param file_name: 文件夹内的json文件名（不带json后缀）
    :return:
    """
    with open(fr"{Path(__file__).resolve().parent.parent.parent}\json_file\{folder}\{file_name}.json",
              "w", encoding="UTF-8") as f:
        # 将生成的数据保存至json文件中
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    return None
