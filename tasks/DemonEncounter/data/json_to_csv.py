import csv
import json
import re

def run():
    # 定义一个正则表达式模式，用于匹配所有的标点符号和特殊符号
    pattern = r'[^\w\s]'

    # 创建一个集合来存储唯一的(问题, 答案)对
    unique_entries = set()

    # 读取现有的CSV文件，并将内容加载到集合中
    try:
        with open('data.csv', mode='r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if len(row) == 2:  # 确保行中有两个元素
                    question, answer = row
                    unique_entries.add((question, answer))
    except FileNotFoundError:
        # 如果文件不存在，则跳过此步骤
        print("data.csv not found, a new file will be created.")

    # 读取JSON文件
    with open('tiku.json', 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    # 遍历JSON数组，提取每个问题的question和answer，并去除标点符号和特殊符号
    for item in json_data:
        question = str(item.get('question', ''))
        answer = str(item.get('answer', ''))
        clean_question = re.sub(pattern, '', question)
        clean_answer = re.sub(pattern, '', answer)

        # 添加新的(问题, 答案)对到集合中
        unique_entries.add((clean_question, clean_answer))

    # 将集合中的所有(问题, 答案)对写入CSV文件
    with open('data.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for entry in unique_entries:
            writer.writerow(entry)


if __name__ == "__main__":
    run()