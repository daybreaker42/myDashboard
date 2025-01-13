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
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙을 위한 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/api/trends")
async def get_trends():
    # Google Trends RSS 피드에서 데이터 가져오기
    async with httpx.AsyncClient() as client:
        response = await client.get("https://trends.google.co.kr/trending/rss?geo=KR")
        data = xmltodict.parse(response.text)
        items = data['rss']['channel']['item']
        return {"trends": items}

@app.get("/api/stocks")
async def get_stocks(request: Request):
    symbols = ['^IXIC', '^GSPC', '^DJI', '^VIX', '^FVX', '^TNX', '^TYX']
    
    stock_data = {}
    try:
        for symbol in symbols:
            ticker = yf.Ticker(symbol)
            # 메인 페이지용 1주일 데이터
            hist_week = ticker.history(period="5d")
            if hist_week.empty:
                continue
                
            # 상세 페이지용 3개월 데이터
            is_full = "full=true" in request.url.query
            hist = ticker.history(period="3mo") if is_full else hist_week
            
            if not hist.empty and len(hist) >= 2:
                stock_data[symbol] = {
                    "current_price": float(hist['Close'].iloc[-1]),
                    "change_percent": float((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2] * 100),
                    "history": hist['Close'].tolist()
                }
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return {"error": "Failed to fetch stock data"}
    
    return stock_data

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about")
async def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/markets")
async def markets_page(request: Request):
    return templates.TemplateResponse("markets.html", {"request": request})
