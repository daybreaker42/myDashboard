from fastapi import APIRouter, Request
import yfinance as yf
import asyncio

async def fetch_stock_data(request: Request, symbol: str, period: str = "1d"):
    """비동기적으로 주식 데이터를 가져오는 함수"""
    try:
        # yfinance 작업을 스레드 풀에서 실행
        loop = asyncio.get_event_loop()
        ticker = yf.Ticker(symbol)
        # request.app.state를 통해 main.py에 정의된 thread_pool을 사용합니다.
        hist = await loop.run_in_executor(
            request.app.state.thread_pool,
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