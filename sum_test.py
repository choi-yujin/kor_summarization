import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", message="You passed along `num_labels=3`.*")


import torch
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration

# 모델과 토크나이저의 로컬 경로 설정
model_path = 'C:/Users/1914039/Desktop/졸프/KoBART-summarization-main/KoBART-summarization-main/kobart_summary'
tokenizer_path = 'gogamza/kobart-base-v2'

# 모델과 토크나이저 로드
model = BartForConditionalGeneration.from_pretrained(model_path, num_labels=2)
tokenizer = PreTrainedTokenizerFast.from_pretrained(tokenizer_path)

print("input")
text = input()

if text:
    input_ids = tokenizer.encode(text)
    input_ids = torch.tensor(input_ids)
    input_ids = input_ids.unsqueeze(0)
    output = model.generate(input_ids, eos_token_id=1, max_length=512, num_beams=5)
    output = tokenizer.decode(output[0], skip_special_tokens=True)
    print(output)

