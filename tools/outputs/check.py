import json
import matplotlib.pyplot as plt
import math
import numpy as np

jsonl_file_path = "/data/projects/ee-llm/EE-LLM/tools/outputs/gsm_sub/gsm_text_368/gsm_sub/gsm_text_368_COT_1.0_20_llama.jsonl"

latency_list = [0]*20
count = 0

# 打开 JSONL 文件
with open(jsonl_file_path, "r") as file:
    # 逐行读取文件内容
    for line in file:
        # 解析 JSON 行
        # print(line[:-2])
        json_data = json.loads(line)
        
        # 统计不同长度的 "answers" 列表出现次数
        thres = json_data['thres']
        for t in thres:
            if not math.isclose(t, 0.0):
                latency = json_data['latency']
                for i,l in enumerate(latency):
                    latency_list[i] += l
                count += 1
                break
        # latency = json_data['latency']
        # for i,l in enumerate(latency):
        #     latency_list[i] += l
        # count += 1
        

avg_latency_list = [l / count for l in latency_list]
print(avg_latency_list)

x = range(1,21)
y1 = [12.745300180238226, 12.718216008466223, 12.5769749659559, 12.673987119742062, 12.68188988061055, 12.570628225155499, 12.57112074157466, 12.574326769813247, 12.519612690676814, 12.448633598244708, 12.627822301310042, 12.726019144058228, 12.523783708396165, 12.504763757405074, 12.715948354290878, 12.852194576159768, 12.787101584932078, 12.537525230127832, 12.534102153518926, 12.47132113835086]
y2 = [16.17001335128494, 16.337906927518222, 16.116583104366843, 15.88017575054065, 16.003058228803717, 16.097536141457766, 16.236831795262255, 16.08956787119741, 16.10110550082248, 15.97424213717813, 16.449908675059028, 15.77304963119652, 16.044816482974134, 15.662107025799545, 16.061725245869678, 16.583058418787044, 16.701178537114806, 16.182308529382166, 16.052981813964635, 16.22984849564407]
# 创建折线图
plt.xticks(np.arange(1, 21, 1))
# plt.xlim(1, 21)
plt.plot(x, y1, label='baseline1')
plt.plot(x, y2, label='baseline2')

# 设置图例
plt.legend()

# 设置坐标轴标签
plt.xlabel('branch')
plt.ylabel('avg latency')

# 设置标题
# plt.title('Line Chart')
plt.savefig('avg_latency.png')
# 显示图形
plt.show()