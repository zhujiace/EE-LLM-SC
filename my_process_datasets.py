import subprocess

BASE_PATH='/workspace'

datasets = [
    {
        'input': '/workspace/data/the-pile-freelaw/the-pile-freelaw-refine-result.jsonl',
        'output_prefix': '/workspace/data/the-pile-freelaw/the-pile-freelaw-meg-llama',
        'tokenizer_type': 'Llama2Tokenizer',
        'tokenizer_model': '/workspace/tokenizers/Llama2Tokenizer/tokenizer.model',
        'workers': '2',
        'append_eod': ''
    },
    # Add more datasets here
    {
        'input': '/workspace/data/the-pile-pubmed-abstract/the-pile-pubmed-abstract-refine-result.jsonl',
        'output_prefix': '/workspace/data/the-pile-pubmed-abstract/the-pile-pubmed-abstract-meg-llama',
        'tokenizer_type': 'Llama2Tokenizer',
        'tokenizer_model': '/workspace/tokenizers/Llama2Tokenizer/tokenizer.model',
        'workers': '2',
        'append_eod': ''
    },
    {
        'input': '/workspace/data/the-pile-pubmed-central/the-pile-pubmed-central-refine-result.jsonl',
        'output_prefix': '/workspace/data/the-pile-pubmed-central/the-pile-pubmed-central-meg-llama',
        'tokenizer_type': 'Llama2Tokenizer',
        'tokenizer_model': '/workspace/tokenizers/Llama2Tokenizer/tokenizer.model',
        'workers': '2',
        'append_eod': ''
    },
    {
        'input': '/workspace/data/the-pile-uspto/the-pile-uspto-refine-result.jsonl',
        'output_prefix': '/workspace/data/the-pile-uspto/the-pile-uspto-meg-llama',
        'tokenizer_type': 'Llama2Tokenizer',
        'tokenizer_model': '/workspace/tokenizers/Llama2Tokenizer/tokenizer.model',
        'workers': '2',
        'append_eod': ''
    },
]

for dataset in datasets:
    command = [
        'python',
        'tools/preprocess_data.py',
        '--input', dataset['input'],
        '--output-prefix', dataset['output_prefix'],
        '--tokenizer-type', dataset['tokenizer_type'],
        '--tokenizer-model', dataset['tokenizer_model'],
        '--workers', dataset['workers'],
        '--append-eod'
    ]

    command_str = ' '.join(command)
    subprocess.Popen(f'nohup {command_str} > pd.log 2>&1 &', shell=True)

print("Processing started in the background.")