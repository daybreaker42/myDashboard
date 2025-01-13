from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import httpx
import xmltodict
import asyncio
import yfinance as yf
from fastapi.templating import Jinja2Templates
from functools import partial
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 전역 HTTP 클라이언트 설정
http_client = httpx.AsyncClient()
thread_pool = ThreadPoolExecutor(max_workers=4)  # yfinance 작업을 위한 스레드 풀

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
    async with http_client as client:
        response = await client.get("https://trends.google.co.kr/trending/rss?geo=KR")
        data = xmltodict.parse(response.text)
        items = data['rss']['channel']['item']
        return {"trends": items}

@app.get("/api/trends/daily")
async def get_daily_trends():
    # Google Daily Trends RSS 피드에서 데이터 가져오기
    async with http_client as client:
        response = await client.get("https://trends.google.co.kr/trends/trendingsearches/daily/rss?geo=KR")
        data = xmltodict.parse(response.text)
        items = data['rss']['channel']['item']
        return {"trends": items}

async def fetch_stock_data(symbol: str, period: str = "1d"):
    """비동기적으로 주식 데이터를 가져오는 함수"""
    try:
        # yfinance 작업을 스레드 풀에서 실행
        loop = asyncio.get_event_loop()
        ticker = yf.Ticker(symbol)
        hist = await loop.run_in_executor(
            thread_pool,
            lambda: ticker.history(period=period)
        )
        
        if not hist.empty:
            return symbol, {
                "current_price": float(hist['Close'].iloc[-1]),
                "change_percent": float((hist['Close'].iloc[-1] - hist['Open'].iloc[0]) / hist['Open'].iloc[0] * 100),
                "name": {
                    '^IXIC': '나스닥',
                    '^GSPC': 'S&P 500',
                    '^DJI': '다우존스',
                    '^VIX': 'VIX',
                    '^FVX': '미국 5년물',
                    '^TNX': '미국 10년물',
                    '^TYX': '미국 30년물'
                }.get(symbol, symbol),
                "history": hist['Close'].tolist() if period != "1d" else None
            }
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return symbol, None

@app.get("/api/stocks")
async def get_stocks(request: Request):
    symbols = ['^IXIC', '^GSPC', '^DJI', '^VIX', '^FVX', '^TNX', '^TYX']
    period = "3mo" if "full=true" in request.url.query else "5d"
    
    # 모든 심볼의 데이터를 병렬로 가져오기
    tasks = [fetch_stock_data(symbol, period) for symbol in symbols]
    results = await asyncio.gather(*tasks)
    
    # 결과를 딕셔너리로 변환
    stock_data = {symbol: data for symbol, data in results if data is not None}
    
    if not stock_data:
        return {"error": "Failed to fetch stock data"}
    
    return stock_data

@app.get("/markets")
async def markets_page(request: Request):
    """시장 지표 페이지를 위한 초기 데이터를 서버사이드에서 렌더링"""
    symbols = ['^IXIC', '^GSPC', '^DJI', '^VIX', '^FVX', '^TNX', '^TYX']
    
    # 모든 심볼의 데이터를 병렬로 가져오기
    tasks = [fetch_stock_data(symbol) for symbol in symbols]
    results = await asyncio.gather(*tasks)
    
    # 결과를 딕셔너리로 변환
    stock_data = {symbol: data for symbol, data in results if data is not None}

    return templates.TemplateResponse(
        "markets.html", 
        {"request": request, "stock_data": stock_data}
    )

@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 HTTP 클라이언트 초기화"""
    global http_client
    http_client = httpx.AsyncClient()

@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 리소스 정리"""
    await http_client.aclose()
    thread_pool.shutdown()

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about")
async def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
