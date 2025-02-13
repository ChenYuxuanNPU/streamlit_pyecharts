import sqlite3
from datetime import datetime
from pathlib import Path


def get_database_name() -> str:
    return "educational_data.db"


# todo:插入新表时在这里要加新的数据表名
def get_table_name_dict() -> dict:
    """
    获取数据表中文解释和数据源excel文件名对应的字典
    :return: {数据表中文解释：data_source表格名}
    """

    return {
        "2023年在编教师信息": "teacher_data_0",
        "2023年编外教师信息": "teacher_data_1",
        "学校信息总览": "school_data_sum",
        "2024年在编教师信息": "teacher_data_0",
        "2024年编外教师信息": "teacher_data_1",
    }


def get_kind_list() -> list:
    """
    table_name_dict.keys()
    :return: 数据表中文解释
    """
    return list(get_table_name_dict().keys())


# todo:插入新表时在这里要加表格名
def get_xlsx_file_and_sheet_name() -> dict:
    """
    获取数据表中文解释和数据源文件名、表格表名
    :return: {中文解释:[表格名, 表格表名]}
    """

    return {
        "2023年在编教师信息": ["teacher_data_0_2023.xlsx", "Sheet1"],
        "2023年编外教师信息": ["teacher_data_1_2023.xlsx", "Sheet1"],
        "学校信息总览": ["school_data.xlsx", "Sheet1"],
        "2024年在编教师信息": ["teacher_data_0_2024.xlsx", "Sheet1"],
        "2024年编外教师信息": ["teacher_data_1_2024.xlsx", "Sheet1"],
    }


# todo:插入新表时在这里要加数据库字段名
def get_words_dict() -> dict:
    """
    获取不同数据表的字段
    :return: {数据表名: (字段)}
    """

    return {
        "2023年在编教师信息": ['采集年份', '校名', '学校类型', '统一社会信用代码', '姓名', '身份证号', '性别', '民族',
                               '籍贯', '婚姻状况', '政治面貌', '入党（团）时间', '参加工作前学历', '参加工作前学位',
                               '参加工作前毕业院校', '参加工作前毕业院校代码', '参加工作前毕业时间',
                               '参加工作前所学专业', '最高学历', '最高学位', '最高学历毕业院校',
                               '最高学历毕业时间', '最高学历所学专业', '参加工作时间', '进入白云教育系统时间',
                               '入编时间', '入现单位时间', '行政职务', '行政职务任职时间', '任教年级', '主教学科',
                               '兼教学科', '最高职称', '职称证专业', '职称认定时间', '现聘职称', '专业技术岗位',
                               '专业技术岗位聘用时间', '普通话水平', '教师资格学段', '教师资格学科', '骨干教师',
                               '四名工作室主持人', '四名工作室主持人确定时间', '市级以上荣誉', '市级以上人才项目',
                               '支教单位名称', '支教地域', '支教开始时间', '支教结束时间', '交流单位名称',
                               '交流开始时间', '交流结束时间', '常住地址', '手机号', '教育网短号', '紧急联系人',
                               '与紧急联系人的关系', '紧急联系方式', '备注', '年龄', '区域', '任教学段',
                               '是否音体美专任教师'],

        "2023年编外教师信息": ['采集年份', '校名', '学校类型', '统一社会信用代码', '姓名', '身份证号', '性别', '民族',
                               '籍贯', '婚姻状况', '政治面貌', '入党（团）时间', '参加工作前学历', '参加工作前学位',
                               '参加工作前毕业院校', '参加工作前毕业时间', '参加工作前所学专业', '最高学历',
                               '最高学位', '最高学历毕业院校', '最高学历毕业时间', '最高学历所学专业',
                               '参加工作时间', '进入白云教育系统时间', '入现单位时间', '行政职务',
                               '行政职务任职时间', '任教年级', '主教学科', '最高职称', '职称证专业',
                               '职称认定时间', '普通话水平', '教师资格学段', '教师资格学科', '骨干教师',
                               '四名工作室主持人', '四名工作室主持人确定时间', '市级以上荣誉', '市级以上人才项目',
                               '常住地址', '手机号', '紧急联系人', '与紧急联系人的关系', '紧急联系方式', '备注',
                               '区域', '任教学段', '是否音体美专任教师', '年龄'],

        "学校信息总览": ['采集年份', '学段', '合计学校数', '公办学校数', '民办学校数', '合计学生数',
                               '公办学校学生数', '公办学校非白云区户籍学生数', '公办学校白云区户籍学生数',
                               '公办学校非广州市户籍学生数', '公办学校广州市户籍学生数', '民办学校学生数',
                               '民办学校非白云区户籍学生数', '民办学校白云区户籍学生数',
                               '民办学校非广州市户籍学生数', '民办学校广州市户籍学生数', '合计教职工数',
                               '公办学校教职工数', '民办学校教职工数', '合计专任教师数', '公办学校专任教师数',
                               '民办学校专任教师数', '合计班额数'],

        "2023年学校详细信息": ['采集年份', '学段', '机构代码', '单位名称', '性质', '办学地址',
                               '学校班额数合计', '幼儿园班额数合计', '小班班额数', '中班班额数', '大班班额数',
                               '小学班额数合计', '一年级班额数', '二年级班额数', '三年级班额数',
                               '四年级班额数', '五年级班额数', '六年级班额数', '初中班额数合计', '初一班额数',
                               '初二班额数', '初三班额数', '高中班额数合计', '高一班额数', '高二班额数',
                               '高三班额数', '学校在校生数合计', '幼儿园在校生数合计', '小班在校生数',
                               '中班在校生数', '大班在校生数', '小学在校生数合计', '一年级在校生数',
                               '二年级在校生数', '三年级在校生数', '四年级在校生数', '五年级在校生数',
                               '六年级在校生数', '初中在校生数合计', '初一在校生数', '初二在校生数',
                               '初三在校生数', '高中在校生数合计', '高一在校生数', '高二在校生数',
                               '高三在校生数', '教职工数', '专任教师数'],

        "2024年在编教师信息": ['采集年份', '校名', '学校类型', '统一社会信用代码', '姓名', '身份证号', '性别', '民族',
                               '籍贯', '婚姻状况', '政治面貌', '入党（团）时间', '参加工作前学历', '参加工作前学位',
                               '参加工作前毕业院校', '参加工作前毕业院校代码', '参加工作前毕业时间',
                               '参加工作前所学专业', '最高学历', '最高学位', '最高学历毕业院校',
                               '最高学历毕业时间', '最高学历所学专业', '参加工作时间', '进入白云教育系统时间',
                               '入编时间', '入现单位时间', '行政职务', '行政职务任职时间', '任教年级', '主教学科',
                               '兼教学科', '最高职称', '职称证专业', '职称证发证时间', '职称认定时间', '现聘职称',
                               '现聘职称聘用时间', '专业技术岗位', '专业技术岗位聘用时间', '普通话水平',
                               '教师资格学段', '教师资格学科', '骨干教师', '四名工作室主持人',
                               '四名工作室主持人确定时间', '市级以上荣誉', '市级以上人才项目', '支教单位名称',
                               '支教地域', '支教开始时间', '支教结束时间', '交流单位名称', '交流开始时间',
                               '交流结束时间', '常住地址', '手机号', '教育网短号', '紧急联系人',
                               '与紧急联系人的关系', '紧急联系方式', '备注', '年龄', '区域', '任教学段',
                               '2024年9月编制所在学段', '2024年9月在岗状态', '是否音体美专任教师', '党内职务级别',
                               '校内其他职务'],

        "2024年编外教师信息": ['采集年份', '校名', '学校类型', '统一社会信用代码', '姓名', '身份证号', '性别', '民族',
                               '籍贯', '婚姻状况', '政治面貌', '入党（团）时间', '参加工作前学历', '参加工作前学位',
                               '参加工作前毕业院校', '参加工作前毕业时间', '参加工作前所学专业', '最高学历',
                               '最高学位', '最高学历毕业院校', '最高学历毕业时间', '最高学历所学专业',
                               '参加工作时间', '进入白云教育系统时间', '入现单位时间', '行政职务',
                               '行政职务任职时间', '任教年级', '主教学科', '最高职称', '职称证专业',
                               '职称认定时间', '普通话水平', '教师资格学段', '教师资格学科', '骨干教师',
                               '四名工作室主持人', '四名工作室主持人确定时间', '市级以上荣誉', '市级以上人才项目',
                               '常住地址', '手机号', '紧急联系人', '与紧急联系人的关系', '紧急联系方式', '备注',
                               '区域', '任教学段', '是否音体美专任教师', '年龄', '教师身份'],

        "2024年学校详细信息": ['采集年份', '学段', '机构代码', '单位名称', '性质', '办学地址',
                               '学校班额数合计', '幼儿园班额数合计', '小班班额数', '中班班额数', '大班班额数',
                               '小学班额数合计', '一年级班额数', '二年级班额数', '三年级班额数',
                               '四年级班额数', '五年级班额数', '六年级班额数', '初中班额数合计', '初一班额数',
                               '初二班额数', '初三班额数', '高中班额数合计', '高一班额数', '高二班额数',
                               '高三班额数', '学校在校生数合计', '幼儿园在校生数合计', '小班在校生数',
                               '中班在校生数', '大班在校生数', '小学在校生数合计', '一年级在校生数',
                               '二年级在校生数', '三年级在校生数', '四年级在校生数', '五年级在校生数',
                               '六年级在校生数', '初中在校生数合计', '初一在校生数', '初二在校生数',
                               '初三在校生数', '高中在校生数合计', '高一在校生数', '高二在校生数',
                               '高三在校生数', '教职工数', '专任教师数'],
    }


# todo:插入新表时在这里要加新的表格名
def get_teacher_table_list() -> dict:
    """
    建立在编与否、年份与教师信息表名的逻辑关系，供其他模块查询json文件时获取
    :return: {在编/编外: 年份: 数据表名}
    """

    return {
        '在编': {
            '2023': 'teacher_data_0',
            '2024': 'teacher_data_0',
        },
        '编外': {
            '2023': 'teacher_data_1',
            '2024': 'teacher_data_1',
        },
    }


def get_school_table_list() -> dict:
    """
    用于获取某一年份学校报表数据的数据表名
    :return: {年份: 数据表名}
    """

    return {
        '2023': 'school_data_sum',
        '2024': 'school_data_sum',
    }


# todo:插入新教师数据表时在这里要加新的年份和类型组合
def get_list_for_update_teacher_info() -> list:
    """
    获取现在数据库有的年份及是否在编的组合构成的列表
    :return: [(年份, 在编/编外)]
    """

    return [('2023', "在编"), ('2023', "编外"), ('2024', "在编"), ('2024', "编外")]


# todo:插入新学校数据表时在这里要加新的年份和类型组合
def get_list_for_update_school_info() -> list:
    """
    获取现在数据库有的年份及是否在编的组合构成的列表
    :return: [(年份, 在编/编外)]
    """

    return ['2023', '2024']


def get_database_basic_info() -> dict:
    """
    返回database_basic_info.json中的信息
    :return:
    """
    return {
        "database_name": get_database_name(),
        "kind_list": get_kind_list(),
        "table_name_dict": get_table_name_dict(),
        "xlsx_file_and_sheet_name": get_xlsx_file_and_sheet_name(),
        "words_dict": get_words_dict(),
        "teacher_table_list": get_teacher_table_list(),
        "school_table_list": get_school_table_list(),
        "list_for_update_teacher_info": get_list_for_update_teacher_info(),
        "list_for_update_school_info": get_list_for_update_school_info()
    }


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


def del_tuple_in_list(data: list) -> list:
    """
    将形如[('1',), ('2',), ('3',),]的数据转化为[1, 2, 3,]
    :param data: 带有元组的列表
    :return: 清洗后的列表
    """

    if not data or not data[0]:
        return []

    if not isinstance(data[0], tuple):
        return data

    output = []

    output.extend(single_data[0] for single_data in data)

    return output


def is_chinese_char(char: str) -> bool:
    """
    用于判断输入的字符是否为汉字
    :param char:
    :return:
    """
    # 中文字符的 Unicode 范围
    # 这里列出了常见的中文字符范围，但可能不完整
    chinese_unicode_ranges = (
        (0x4E00, 0x9FFF),  # 基本汉字
        (0x3400, 0x4DBF),
        (0x20000, 0x2a6df),
        (0x2a700, 0x2b73f),
        (0x2b740, 0x2b81f),
        (0x2b820, 0x2ceaf),
        (0xf900, 0xfaff),
        (0x2f800, 0x2fa1f)
    )

    if len(char) != 1:
        return False

    # 获取字符的 Unicode 码点
    char_code = ord(char)

    # 检查字符的 Unicode 码点是否在中文范围内
    for start, end in chinese_unicode_ranges:
        if start <= char_code <= end:
            return True

    return False


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


def connect_database() -> tuple[sqlite3.Cursor, sqlite3.Connection]:
    """
    用于连接数据库
    :return:
    """

    conn = sqlite3.connect(
        fr"{Path(__file__).resolve().parent.parent}\database\{get_database_name()}"
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


if __name__ == '__main__':
    # print(get_words_dict()["teacher_info_1_2024_word"].split())

    print(is_chinese_char(char=""))
