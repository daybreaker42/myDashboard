from fastapi import APIRouter, Request
import asyncio
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor

from apis import stocks

router = APIRouter()

@router.get("/api/stocks")
async def get_stocks(request: Request):
    symbols = ['^IXIC', '^GSPC', '^DJI', '^VIX', '^FVX', '^TNX', '^TYX']
    period = "3mo" if "full=true" in request.url.query else "5d"
    
    # 모든 심볼의 데이터를 병렬로 가져오기
    tasks = [stocks.fetch_stock_data(request, symbol, period) for symbol in symbols]
    results = await asyncio.gather(*tasks)
    
    # 결과를 딕셔너리로 변환
    stock_data = {symbol: data for symbol, data in results if data is not None}
    
    if not stock_data:
        return {"error": "Failed to fetch stock data"}
    
    return stock_data
