import warnings
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
from typing import Optional
import os

# 경고 메시지 무시 설정
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", message="You passed along `num_labels=3`.*")

# FastAPI 앱 인스턴스 생성
app = FastAPI()

# 모델과 토크나이저의 로컬 경로 설정
# 모델 경로 수정하기!
model_path = 'C:/Users/1914039/Desktop/졸프/KoBART-summarization-main/KoBART-summarization-main/kobart_summary'
tokenizer_path = 'gogamza/kobart-base-v2'

# 모델과 토크나이저 로드
model = BartForConditionalGeneration.from_pretrained(model_path, num_labels=2)
tokenizer = PreTrainedTokenizerFast.from_pretrained(tokenizer_path)

# 백엔드 서버 URL (환경변수에서 읽어오기)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:3000")

# 요청 데이터 모델
class Item(BaseModel):
    text: Optional[str] = None

async def send_result_to_backend(summary: str):
    # 백엔드로 요약 결과를 POST
    async with httpx.AsyncClient() as client:
        data = {"summary": summary}
        try:
            response = await client.post(f"{BACKEND_URL}/api/summary-result", json=data)
            return response.status_code
        except Exception as e:
            print(f"Failed to send result to backend: {e}")
            return None

@app.post("/answer")
async def receive_answer(item: Item):
    text = item.text
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    # 텍스트를 모델에 입력하고 요약 생성
    input_ids = tokenizer.encode(text)
    input_ids = torch.tensor(input_ids)
    input_ids = input_ids.unsqueeze(0)
    output = model.generate(input_ids, eos_token_id=1, max_length=512, num_beams=5)
    summary = tokenizer.decode(output[0], skip_special_tokens=True)

    # 요약 결과를 백엔드로 전송
    status_code = await send_result_to_backend(summary)
    if status_code == 200:
        return {"result": summary, "status": "Summary sent to backend successfully"}
    else:
        return {"result": summary, "status": "Failed to send summary to backend"}

# Uvicorn을 사용하여 서버 실행을 위한 메인 가드
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
