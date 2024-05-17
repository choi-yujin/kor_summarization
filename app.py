from fastapi import FastAPI, Request
from pydantic import BaseModel
import torch
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration

class TextRequest(BaseModel):
    text: str

app = FastAPI()

model_path = 'C:/Users/1914039/Desktop/졸프/KoBART-summarization-main/KoBART-summarization-main/kobart_summary'
tokenizer_path = 'gogamza/kobart-base-v2'

model = BartForConditionalGeneration.from_pretrained(model_path)
tokenizer = PreTrainedTokenizerFast.from_pretrained(tokenizer_path)

@app.post("/summarize")
async def summarize(request: TextRequest):
    input_text = request.text

    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    output = model.generate(input_ids, eos_token_id=1, max_length=512, num_beams=5)
    summary = tokenizer.decode(output[0], skip_special_tokens=True)

    return {"summary": summary}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='', port=8000)
