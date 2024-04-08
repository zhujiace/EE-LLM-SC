import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

jsonl_file_path = "/data/projects/ee-llm/EE-LLM/tools/outputs/gsm_sub/gsm_text_368/gsm_sub/gsm_text_368_COT_1.0_20_llama.jsonl"

confidence_list = []
data = []

# 打开 JSONL 文件
with open(jsonl_file_path, "r") as file:
    # 逐行读取文件内容
    for line in file:
        # 解析 JSON 行
        # print(line[:-2])
        json_data = json.loads(line)
        
        # 统计不同长度的 "answers" 列表出现次数
        score = json_data["score"]
        target = json_data["target"]
        answers = json_data["answers"]
        target_count = answers.count(target)
        confidence = json_data["confidence"]
        if score == 1 and target_count > 5:
            for num in confidence:
                data.append(num)
                print("{:.2f}".format(num), end=' ')
            print("")
        confidence_list.append(confidence)

sns.kdeplot(data, fill=True)
# 找到最高点的位置
max_density = np.max(sns.kdeplot(data).get_lines()[0].get_data()[1])
max_index = np.argmax(sns.kdeplot(data).get_lines()[0].get_data()[1])
max_x = sns.kdeplot(data).get_lines()[0].get_data()[0][max_index]
max_y = max_density

# 在图中标注最高点
plt.annotate(f"Max: {max_x:.4f}", xy=(max_x, max_y), xytext=(max_x - 1.0, max_y - 0.05),
             arrowprops=dict(facecolor='black', arrowstyle='->'))
plt.savefig('density.png')
plt.show()


    