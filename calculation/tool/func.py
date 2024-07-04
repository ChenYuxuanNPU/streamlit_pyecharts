import json


def load_json_data(folder: str, file_name: str) -> dict:
    # 读取现有json文件
    with open(fr"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\{folder}\{file_name}.json",
              "r", encoding="UTF-8") as f:
        json_data = json.load(f)

    return json_data


def save_json_data(json_data: dict, folder: str, file_name: str) -> None:
    with open(fr"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\{folder}\{file_name}.json",
              "w", encoding="UTF-8") as f:
        # 将生成的数据保存至json文件中
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    return None
