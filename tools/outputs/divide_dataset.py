import json
import matplotlib.pyplot as plt

jsonl_file_path = "/data/projects/ee-llm/EE-LLM/tools/outputs/gsm_text/gsm_text_0.9_20_llama_0404.jsonl"

answers_length_count = {}  # 用于统计不同长度的 "answers" 列表出现次数
answers_target_count = {}

# 打开 JSONL 文件
with open(jsonl_file_path, "r") as file:
    # 逐行读取文件内容
    for line in file:
        # 解析 JSON 行
        # print(line[:-2])
        json_data = json.loads(line[:-2])
        
        # 统计不同长度的 "answers" 列表出现次数
        target = json_data["target"]
        answers = json_data["answers"]
        answers_length = len(answers)
        if answers_length in answers_length_count:
            answers_length_count[answers_length] += 1
        else:
            answers_length_count[answers_length] = 1

        target_count = answers.count(target)
        if target_count in answers_target_count:
            answers_target_count[target_count] += 1
        else:
            answers_target_count[target_count] = 1


    # keys = answers_length_count.keys()
    # values = answers_length_count.values()
    # # 绘制条形图
    # plt.bar(keys, values)

    # # 添加标签和标题
    # plt.xlabel('Answer')
    # plt.ylabel('Example')
    # # plt.title('Dictionary Data')
    # plt.savefig('answers_length_count.png')
    # plt.show()

    keys = answers_target_count.keys()
    values = answers_target_count.values()
    # 绘制条形图
    plt.bar(keys, values)

    # 添加标签和标题
    plt.xlabel('Answer')
    plt.ylabel('Example')
    # plt.title('Dictionary Data')
    plt.savefig('answers_target_count.png')
    plt.show()
    print(answers_length_count)
    print(answers_target_count)