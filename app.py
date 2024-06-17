import warnings
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
from typing import Optional
import os
import uuid  # 고유한 파일명을 위한 UUID 모듈 추가

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64
from fastapi.responses import FileResponse
from konlpy.tag import Okt

# 경고 메시지 무시 설정
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", message="You passed along `num_labels=3`.*")

# FastAPI 앱 인스턴스 생성
app = FastAPI()

# 현재 파일의 디렉토리를 기준으로 상대 경로 설정해 model_path에 kobart_summary 폴더의 경로 전달
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'kobart_summary')
tokenizer_path = 'gogamza/kobart-base-v2'

# 모델과 토크나이저 로드
model = BartForConditionalGeneration.from_pretrained(model_path, num_labels=2)
tokenizer = PreTrainedTokenizerFast.from_pretrained(tokenizer_path)

# Okt 형태소 분석기 로드
okt = Okt()

# 백엔드 서버 URL (환경변수에서 읽어오기)
BACKEND_URL = os.getenv("BACKEND_URL", "http://52.79.243.59:3000")

# 요청 데이터 모델
class Item(BaseModel):
    text: Optional[str] = None

# 자주 사용되는 조사 목록
particles = ['은', '는', '이', '가', '을', '를', '의', '에', '에서', '와', '과', '로', '으로', '도', '만', '하고', '고', '이며', '로서', '이면서', '때로는', '위해', '못']

async def send_result_to_backend(summary: str):
    # 백엔드로 요약 결과를 POST
    async with httpx.AsyncClient() as client:
        data = {"summary": summary}
        print(summary)
        try:
            response = await client.post(f"{BACKEND_URL}/api/summary-result", json=data)
            return response.status_code
        except Exception as e:
            print(f"Failed to send result to backend: {e}")
            return None

def create_wordcloud(text: str, filepath: str) -> str:
    # 워드클라우드 생성
    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path='SeoulNamsanvert.ttf').generate(text)
    
    # 이미지 저장
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(filepath, format='png')
    plt.close()
    
    return filepath

def filter_particles(words):
    return [word for word in words if word not in particles]

def tokenize_and_combine(text: str, summary: str) -> str:
    combined_text = text + " " + summary

    # Okt를 사용하여 명사와 형용사 추출
    pos_tags = okt.pos(combined_text)
    nouns_and_adjectives = [word for word, pos in pos_tags if pos in ['Noun', 'Adjective']]
    
    # 조사 제거
    filtered_words = filter_particles(nouns_and_adjectives)
    
    # 중복 단어 제거 및 상위 중요 단어만 선택
    unique_words = list(set(filtered_words))
    top_n = 40
    top_words = unique_words[:top_n]
    
    filtered_text = ' '.join(top_words)
    print(filtered_text)
    return filtered_text

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

    # 텍스트와 요약 결과를 토큰화하여 결합
    combined_text = tokenize_and_combine(text, summary)
    
    # 고유한 워드클라우드 이미지 파일 경로 설정
    wordcloud_filename = f"wordcloud_{uuid.uuid4().hex}.png"
    wordcloud_filepath = os.path.join(base_dir, wordcloud_filename)
    
    # 워드클라우드 생성 및 파일 저장
    create_wordcloud(combined_text, wordcloud_filepath)
     # URL 생성 (백엔드에서 접근 가능하도록)
    wordcloud_url = f"{BACKEND_URL}/uploads/{wordcloud_filename}"

    return {"result": summary, "wordcloud_url": wordcloud_url}

# Uvicorn을 사용하여 서버 실행을 위한 메인 가드
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
