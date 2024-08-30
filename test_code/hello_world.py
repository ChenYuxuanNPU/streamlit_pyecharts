import pyecharts.options as opts
from pyecharts.charts import Pie
import os

if __name__ == '__main__':
    # inner_x_data = ["直达", "营销广告", "搜索引擎"]
    # inner_y_data = [335, 679, 1548]
    # inner_data_pair = [list(z) for z in zip(inner_x_data, inner_y_data)]
    #
    # outer_x_data = ["直达", "营销广告", "搜索引擎", "邮件营销", "联盟广告", "视频广告", "百度", "谷歌", "必应", "其他"]
    # outer_y_data = [335, 310, 234, 135, 1048, 251, 147, 102]
    # outer_data_pair = [list(z) for z in zip(outer_x_data, outer_y_data)]
    #
    # (
    #     Pie()
    #     .add(
    #         series_name="1",
    #         data_pair=inner_data_pair,
    #         radius=["15%", "30%"],
    #         label_opts=opts.LabelOpts(position="outside"),
    #     )
    #     .add(
    #         series_name="2",
    #         radius=["50%", "65%"],
    #         data_pair=outer_data_pair,
    #         label_opts=opts.LabelOpts(
    #             position="outside",
    #         ),
    #     )
    #     .set_global_opts(tooltip_opts=opts.TooltipOpts(is_show=False))
    #     .set_series_opts(
    #         tooltip_opts=opts.TooltipOpts(
    #             trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
    #         )
    #     )
    # )

    # 获取当前文件的绝对路径
    current_file_path = os.path.abspath(__file__)

    # 如果你只需要目录部分
    current_dir = os.path.dirname(os.path.abspath(__file__))

    print("当前文件路径:", current_file_path)
    print("当前文件所在目录:", current_dir)

