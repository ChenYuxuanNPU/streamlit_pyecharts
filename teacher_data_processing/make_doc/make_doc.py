from pathlib import Path

# 常用常量
doc_path = fr"{Path(__file__).resolve().parent.parent.parent}\doc\data.txt"


def write_doc(label, data, kind, content):

    with open(doc_path, mode="w", encoding="utf-8") as f:

        print("", file=f)
        print(f"{kind}{content}数据如下：", file=f)

        for i in range(0, len(label) - 1):
            print(str(label[i]) + "人数：" + str(data[i]) + "，占比" + str(round(100 * data[i] / sum(data), 1)) + "%",
                  file=f)

        print("", file=f)
