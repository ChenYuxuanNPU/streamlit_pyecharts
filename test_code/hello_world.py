import json
import copy

# 读取现有json文件
with open(r"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\result\output.json",
          "r", encoding="UTF-8") as file:
    json_data = json.load(file)

dict1 = {
    "abd": 2,
    "adc": 3
}
print(dict1)

print(dict1.items())

print("")
a = copy.deepcopy(json_data["在编"]["全区"]["所有学段"]["最高学历"])


print(a.items())

for i in a.items():
    print(i)