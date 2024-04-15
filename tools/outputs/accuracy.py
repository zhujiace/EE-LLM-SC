import json
import matplotlib.pyplot as plt
from collections import Counter

jsonl_file_path = "/data/projects/ee-llm/EE-LLM/tools/outputs/gsm_sub/gsm_text_368/gsm_sub/gsm_text_368_COT_1.0_20_baseline.jsonl"

scores = 0
re_scores = 0
count = 0


def find_most_common_elements(lst):
    if not lst:  # 列表为空
        return None  # 返回None或其他自定义值
    counter = Counter(lst)
    most_common = counter.most_common(1)
    return most_common[0][0]

# 打开 JSONL 文件
with open(jsonl_file_path, "r") as file:
    # 逐行读取文件内容
    for line in file:
        # 解析 JSON 行
        # print(line[:-2])
        # json_data = json.loads(line[:-2])
        json_data = json.loads(line)
        
        # 统计不同长度的 "answers" 列表出现次数
        answers = json_data["answers"]
        answer = find_most_common_elements(answers)
        target = json_data["target"]
        if target == answer:
            re_scores += 1
        scores += json_data["score"]
        count += 1
        
print(scores/count)
print(re_scores/count)