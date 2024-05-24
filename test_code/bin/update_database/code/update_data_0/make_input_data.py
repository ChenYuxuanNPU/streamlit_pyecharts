#
# 这个文件获取表格中的数据并验证长度
# 不需要单独跑，被data_insert调用
#

import openpyxl


def read_input_data():
    # 确定收集的数据表
    wb = openpyxl.load_workbook('/update_database/data_source/data_0.xlsx', data_only=True)
    sheet = wb["Sheet1"]

    # 获取表格数据
    result = []
    for row in sheet.iter_rows(values_only=True):
        # 不读取第一行列标
        if not str(row[0]).isnumeric():
            result.append(row)
            # print(row)

    # 用来验证所有数据是否等长
    flag = 0
    for i in range(1, len(result)):
        if len(result[i]) != len(result[0]):
            flag = 1

    if flag == 0:
        print(f"单条数据长度：{str(len(result[0]))}（update_data_0.make_input_data.py）")
        print(f"总数据量：{str(len(result))}（update_data_0.make_input_data.py）")

        return result

    else:
        print("数据长度不相同（update_data_0.make_input_data.py）")

        return []

