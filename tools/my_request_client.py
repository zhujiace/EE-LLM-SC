import requests
import json
import time
import tqdm
import copy
from collections import Counter
import os
import sys
import func_timeout
from scipy import integrate, stats
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

URL = "http://localhost:5000/api"
HEADER = {
    "Content-Type": "application/json; charset=UTF-8",
}

class TqdmPrintWrapper:
    def __init__(self, iterable, total=None):
        self.iterable = iterable
        self.total = total
        self.iter_obj = iter(iterable)
        self.pbar = tqdm.tqdm(total=total, file=sys.stdout)
        
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            value = next(self.iter_obj)
            self.pbar.update(1)
            return value
        except StopIteration:
            self.pbar.close()
            raise
    
    def write(self, message):
        self.pbar.write(message)
        sys.stdout.flush()

def extract_answer(gen: str):
    
    # Search for "ans = " in the generated text
    start_idx = gen.find("ans = ")
    if start_idx == -1:
        return ""
    
    # Find the end of the number (before the next newline character)
    end_idx = gen.find("\n", start_idx)
    if end_idx == -1:
        return ""
    
    # Extract the number
    answer = gen[start_idx + len("ans = "):end_idx].strip()
    return answer

def extract_code(gen: str):
    return gen.split("\n\n\n\n")[0]

def floatify_ans(ans):
    if ans is None:
        return None
    elif type(ans) == dict:
        ans = list(ans.values())[0] if len(ans) else None
    elif type(ans) == bool:
        ans = ans
    elif type(ans) in [list, tuple]:
        if not ans:
            return None
        else:
            try:
                ans = float(ans[0])
            except Exception:
                ans = str(ans[0])
    else:
        try:
            ans = float(ans)
        except Exception:
            ans = str(ans)
    return ans

def floats_equal(a, b, prompt_type, tolerance=1e-4):
    try:
        if prompt_type=="PAL":
            return abs(a - b) < tolerance
        return a == b
    except:
        return False

def safe_execute(code_string: str, keys=None, use_pot=False, maxtime=5):
    def execute(x):
        try:
            exec(f'from math import *\n{x}')
            locals_ = locals()
            if keys is not None:
                return [locals_.get(k, None) for k in keys]
            # PoT
            if use_pot:
                return locals_.get('ans', None)
            # PAL
            solution = locals_.get('solution', None)
            if solution is not None: 
                return solution()
            else:
                exec('\n'.join([xx[4:] for xx in x.strip().split('\n')[1:-1]]))
                locals_ = locals()
                return locals_.get('result', None)
        except Exception as e:
            return None
    try:
        ans = func_timeout.func_timeout(maxtime, execute, args=(code_string,))
    except func_timeout.FunctionTimedOut:
        ans = None
    
    return ans

def confidence_criteria(answers : list, conf_thresh : int = None):
    if len(answers) == 0:
        return {
        'most_common' : None,
        'prob' : -1,
        'stop' : False,
        }
    most_common = Counter(answers).most_common(2)
    if len(most_common) == 1:
        a, b = most_common[0][1], 0
    else:
        a, b= most_common[0][1], most_common[1][1]
    a = float(a)
    b = float(b)
    return_dict = {
        'most_common' : most_common[0][0],
        'prob' : -1,
        'stop' : False,
    }
        
    try:
        prob =  integrate.quad(lambda x : x**(a) * (1-x)**(b), 0.5, 1)[0] / integrate.quad(lambda x : x**(a) * (1-x)**(b), 0, 1)[0]
    except Exception as e:
        # print error message
        print(f"Error during numerical integration: {e}")
        return_dict['stop'] = False
        return_dict['prob'] = -1
        return return_dict
    return_dict['prob'] = prob
    return_dict['stop'] = prob >= conf_thresh
    return return_dict

def request(
    prompts,
    prompt_type="COT",
    tokens_to_generate=100,
    use_early_exit=True,
    early_exit_thres=0.8,
    print_max_prob=False,
    exit_layers=[],
    no_log=False,
    max_gens=1,
    target=""
):
    results = {}
    gens = []
    answers = []
    token_num = []
    length = len(prompts)
    for i in range(length):
        for gen_id in range(max_gens):
            print(f"\nstart_{gen_id}")      
            data = {
                "prompts": [prompts[i]],
                "tokens_to_generate": tokens_to_generate,
                # "top_k": 1,
                "temperature": 0.9,
                "top_p": 0.6,
                "logprobs": True,
                "random_seed": int(time.time_ns()) % 16384,
                "echo_prompts": False,
                "early_exit_thres": early_exit_thres,
                "exit_layers": exit_layers,
                "no_log": no_log
            }
            if use_early_exit:
                data["use_early_exit"] = True
            if print_max_prob:
                data["print_max_prob"] = True
            start_time = time.time()
            # print(json.dumps(data))
            response = requests.put(URL, headers=HEADER, data=json.dumps(data))
            end_time = time.time()
            # print("Request:-------------------------------------------------")
            # print(f"{prompts[i]}")
            print(
                f"Response tme:{end_time - start_time:.4f}s"
            )
            result = response.json()
            try:
                # print(result)
                text = result['text'][0]
                token_num.append(result['token'])
                if prompt_type=="COT":
                    answer = extract_answer(text)
                elif prompt_type=="PAL":
                    code = extract_code(text)
                    answer = safe_execute(code)
                    answer = floatify_ans(answer)
                print(f"ans = {answer}, target = {target}")
                # result['answer'] = answer
                if answer != None and answer != "":
                    answers.append(answer)
                #confidence = confidence_criteria(answers,1)
                #print(confidence)
            except Exception as e:
                print(response)
            # gens.append(result)
            print(f"end_{gen_id}")
        score = 0  
        if len(answer) > 0:
            counter = Counter(answers)
            most_common = counter.most_common(1)[0]
            score = 1 if floats_equal(most_common[0],target,prompt_type) else 0
            answer = most_common[0]
            results['answer'] = answer
        else:
            answer = None
            results['answer'] = None
        results['score'] = score
        results['target'] = target
        results['answers'] = answers
        results['token'] = sum(token_num) / len(token_num)
        # results['gens'] = gens
        print(f'answer = {answer}, score = {score}')
    return results


def main(
    dataset, 
    tokens_to_generate, 
    use_early_exit, 
    early_exit_thres, 
    print_max_prob, 
    exit_layers, 
    no_log,
    prompt_file,
    prompt_type,
    max_gens,
    label,
):
    import importlib
    math_prompts = importlib.import_module(f'prompt.{prompt_file}')    # prompting
    DATA_PATH = f'tools/datasets/{dataset}.jsonl'
    if not os.path.exists(DATA_PATH):
        DATA_PATH = f'tools/datasets/{dataset}.json'
    if DATA_PATH.endswith('.jsonl'):
        examples = list(map(json.loads, open(DATA_PATH)))
    elif DATA_PATH.endswith('.json'):
        examples = json.load(open(DATA_PATH))['examples']

    OUTPUT_PATH = f'tools/outputs/{dataset}/{dataset}_{prompt_type}_{early_exit_thres}_{max_gens}_{label}.jsonl'
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    scores = []

    print("start")
    with open(OUTPUT_PATH, 'w') as f:
        # pbar = tqdm.tqdm(examples[0:2], initial=0, total=len(examples))
        pbar = TqdmPrintWrapper(examples[:], total=len(examples))
        for x in pbar:
            prompts = []
            question = x['input']
            target = x['target']
            prompts.append(math_prompts.MATH_PROMPT.format(question=question))
            try:
                result = request(prompts,
                        prompt_type,
                        tokens_to_generate, 
                        use_early_exit, 
                        early_exit_thres, 
                        print_max_prob, 
                        exit_layers,
                        no_log,
                        max_gens,
                        target
                        )
                f.write(json.dumps(result) + ",\n")
                score = result['score']
            except Exception as e:
                score = 0
                print('Error',e)
            scores.append(score)
            print(f'Accuracy - {sum(scores) / len(scores)}')
            # dm.write(f'Accuracy - {sum(scores) / len(scores)}')
        
    



if __name__ == "__main__":
    main(
        dataset="gsm_text",
        prompt_file="gsm_prompts",
        prompt_type="COT",
        # dataset="gsm",
        # prompt_file="gsm_pal",
        # prompt_type="PAL",
        tokens_to_generate=150,
        use_early_exit=True,
        early_exit_thres=0.9,
        print_max_prob=False,
        exit_layers=[],
        no_log=True,
        max_gens = 20,
        label = "llama"
    )
