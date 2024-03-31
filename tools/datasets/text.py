import json

# 读取JSONL文件
with open('gsm.jsonl', 'r') as file:
    lines = file.readlines()

# 修改数据
data = []
for line in lines:
    item = json.loads(line)
    item['target'] = str(item['target'])
    data.append(item)

# 保存修改后的JSONL文件
with open('gsm.jsonl', 'w') as file:
    for item in data:
        file.write(json.dumps(item) + '\n')