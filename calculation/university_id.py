from calculation.tool.func import load_json_data


def convert_university_id_to_university_name(uni_id: str | int | list | set) -> str | list:
    """
    将院校代码转换为院校名
    :param uni_id: 需要转换的院校代码，字符型/int型或列表均可
    :return: 字符型和int型返回str，列表返回列表
    """

    convert_dict = load_json_data(folder="source", file_name="院校代码")
    # convert_dict格式为：{
    # "10699": [
    #         "西北工业大学",
    #         "工业和信息化部",
    #         "本科",
    #         "西安市",
    #         "4161010699"
    #     ],
    # }
    # 因此要取出第一项([0])作为校名

    if isinstance(uni_id, str):
        return convert_dict.get(uni_id, "无")[0]

    if isinstance(uni_id, int):
        return convert_dict.get(str(uni_id), "无")[0]

    if isinstance(uni_id, (list, set)):

        uni_name_list = []

        for item in uni_id:
            uni_name_list.append(convert_dict.get(str(item), "无")[0])

        return uni_name_list

    return "无"


if __name__ == '__main__':
    print(convert_university_id_to_university_name(uni_id={"10699", 10558}))
