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

# CORS 설정 부분 수정
allowed_origins = [
    "http://localhost:30000",  # 로컬 개발 환경
    "http://127.0.0.1:30000",  # 로컬 대체 주소
]

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # 화이트리스트 방식으로 변경
    allow_credentials=True,
    allow_methods=["GET"],  # 필요한 HTTP 메서드만 허용
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

@app.get("/api/trends/daily")
async def get_daily_trends():
    # Google Daily Trends RSS 피드에서 데이터 가져오기
    async with httpx.AsyncClient() as client:
        response = await client.get("https://trends.google.co.kr/trends/trendingsearches/daily/rss?geo=KR")
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
    """시장 지표 페이지를 위한 초기 데이터를 서버사이드에서 렌더링"""
    symbols = ['^IXIC', '^GSPC', '^DJI', '^VIX', '^FVX', '^TNX', '^TYX']
    stock_data = {}
    
    try:
        # 각 심볼별로 현재 데이터만 가져옴
        for symbol in symbols:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")  # 오늘 데이터만 가져옴
            
            if not hist.empty:
                stock_data[symbol] = {
                    "current_price": float(hist['Close'].iloc[-1]),
                    "change_percent": float((hist['Close'].iloc[-1] - hist['Open'].iloc[0]) / hist['Open'].iloc[0] * 100),
                    "name": {  # 심볼별 한글 이름 매핑
                        '^IXIC': '나스닥',
                        '^GSPC': 'S&P 500',
                        '^DJI': '다우존스',
                        '^VIX': 'VIX',
                        '^FVX': '미국 5년물',
                        '^TNX': '미국 10년물',
                        '^TYX': '미국 30년물'
                    }.get(symbol, symbol)
                }
    except Exception as e:
        print(f"Error fetching initial stock data: {e}")
        stock_data = {}  # 에러 발생 시 빈 데이터 전달

    return templates.TemplateResponse(
        "markets.html", 
        {"request": request, "stock_data": stock_data}
    )
