from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import httpx
import xmltodict
import json
from datetime import datetime
import yfinance as yf
from pathlib import Path

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙을 위한 설정
app.mount("/static", StaticFiles(directory="src"), name="static")

@app.get("/api/trends")
async def get_trends():
    # Google Trends RSS 피드에서 데이터 가져오기
    async with httpx.AsyncClient() as client:
        response = await client.get("https://trends.google.co.kr/trends/trendingsearches/daily/rss?geo=KR")
        data = xmltodict.parse(response.text)
        items = data['rss']['channel']['item']
        return {"trends": items}

@app.get("/api/stocks")
async def get_stocks():
    # 관심 있는 주식 심볼 리스트
    symbols = ['^IXIC', '^GSPC', '^DJI', '^VIX', '^FVX', '^TNX', '^TYX']
    
    stock_data = {}
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="3mo")
        stock_data[symbol] = {
            "current_price": float(hist['Close'].iloc[-1]),  # 변경: [-1] -> .iloc[-1]
            "change_percent": float((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2] * 100),  # 변경: 모든 인덱싱을 .iloc 사용
            "history": hist['Close'].tolist()[-90:]
        }
    
    return stock_data

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # index.html 파일 읽기
    html_file = Path("src/index.html").read_text(encoding="utf-8")
    return html_file
