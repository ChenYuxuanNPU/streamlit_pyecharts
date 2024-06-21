#
# 这个文件获取表格中的数据并验证长度
# 不需要单独跑，被data_insert调用
#

import openpyxl


def read_input_data(kind):
    result = []

    # 确定收集的数据表
    if kind == "在编教师信息":
        wb = openpyxl.load_workbook('C:\\Users\\1012986131\\Desktop\\python\\streamlit_pyecharts\\update_database'
                                    '\\data_source\\teacher_data_0.xlsx', data_only=True)
        sheet = wb["Sheet1"]

        # 获取表格数据
        for row in sheet.iter_rows(values_only=True):
            # 不读取第一行列标
            if not str(row[0]).isnumeric():
                result.append(row)
                # print(row)

    elif kind == "编外教师信息":
        wb = openpyxl.load_workbook('C:\\Users\\1012986131\\Desktop\\python\\streamlit_pyecharts\\update_database'
                                    '\\data_source\\teacher_data_1.xlsx', data_only=True)
        sheet = wb["Sheet1"]

        # 获取表格数据
        for row in sheet.iter_rows(values_only=True):
            # 不读取第一行列标
            if not str(row[0]).isnumeric():
                result.append(row)
                # print(row)

    elif kind == "2023年学校情况一览表":
        wb = openpyxl.load_workbook('C:\\Users\\1012986131\\Desktop\\python\\streamlit_pyecharts\\update_database'
                                    '\\data_source\\2023年教育事业统计报表对账表.xlsx', data_only=True)
        sheet = wb["一览表"]

        # 取行
        for row in range(5, 15):
            result.append([])

            # 取列
            for col in range(65, 87):

                if sheet[str(chr(col)) + str(row)].value is not None:
                    result[-1].append(sheet[str(chr(col)) + str(row)].value)

                else:
                    result[-1].append(result[-2][col - 65])

                if col == 86:
                    result[-1] = tuple(result[-1])

    else:
        print(fr"{kind}kind参数错误 (make_input_data.py)")
        return -1

    # 判断一下result是否为空值
    if len(result) == 0:
        print("读取的数据为空值 (make_input_data.py)")
        return -1

    # 用来验证所有数据是否等长
    flag = 0
    for i in range(1, len(result)):
        if len(result[i]) != len(result[0]):
            flag = 1

    if flag == 0:
        print(fr"{kind}单条数据长度:{str(len(result[0]))} (make_input_data.py)")
        print(fr"{kind}总数据量:{str(len(result))} (make_input_data.py)")

        return result

    else:
        print(fr"{kind}数据长度不相同 (make_input_data.py)")

        return -1


if __name__ == '__main__':
    print(read_input_data(kind="2023年学校情况一览表"))
