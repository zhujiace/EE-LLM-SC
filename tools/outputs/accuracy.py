import json
import matplotlib.pyplot as plt

jsonl_file_path = "/data/projects/ee-llm/EE-LLM/tools/outputs/gsm_text/gsm_text_0.9_20_llama_0404.jsonl"

scores = 0
count = 0

# 打开 JSONL 文件
with open(jsonl_file_path, "r") as file:
    # 逐行读取文件内容
    for line in file:
        # 解析 JSON 行
        # print(line[:-2])
        json_data = json.loads(line[:-2])
        
        # 统计不同长度的 "answers" 列表出现次数
        scores += json_data["score"]
        count += 1
        
print(scores/count)