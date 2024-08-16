import csv
import json
import re

def run():
    # 读取JSON文件
    with open('tiku.json', 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    # 定义一个正则表达式模式，用于匹配所有的标点符号和特殊符号
    pattern = r'[^\w\s]'

    # 创建一个集合来存储唯一的(问题, 答案)对
    unique_entries = set()

    # 打开一个CSV文件准备写入数据
    with open('data.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        # 遍历JSON数组，提取每个问题的question和answer，并去除标点符号和特殊符号
        for item in json_data:
            question = str(item.get('question', ''))
            answer = str(item.get('answer', ''))
            clean_question = re.sub(pattern, '', question)
            clean_answer = re.sub(pattern, '', answer)

            # 使用一个集合来去除重复项
            if (clean_question, clean_answer) not in unique_entries:
                unique_entries.add((clean_question, clean_answer))
                writer.writerow([clean_question, clean_answer])
if __name__ == "__main__":
    run()