from datetime import datetime

from dateutil.relativedelta import relativedelta

# 定义两个日期
date1 = datetime(2019, 4, 2)
date2 = datetime(2023, 4, 3)

# 计算两个日期之间的间隔
delta = abs(relativedelta(date1, date2).years)

# 输出间隔的天数
print(f"{delta}")

