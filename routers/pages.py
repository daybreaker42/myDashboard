from fastapi import APIRouter, Request
import asyncio
from .stocks import fetch_stock_data

router = APIRouter()

@router.get("/markets")
async def markets_page(request: Request):
    """시장 지표 페이지를 위한 초기 데이터를 서버사이드에서 렌더링"""
    symbols = ['^IXIC', '^GSPC', '^DJI', '^VIX', '^FVX', '^TNX', '^TYX']
    
    # 모든 심볼의 데이터를 병렬로 가져오기
    tasks = [fetch_stock_data(request, symbol) for symbol in symbols]
    results = await asyncio.gather(*tasks)
    
    # 결과를 딕셔너리로 변환
    stock_data = {symbol: data for symbol, data in results if data is not None}

    return request.app.state.templates.TemplateResponse(
        "markets.html", 
        {"request": request, "stock_data": stock_data}
    )

@router.get("/")
async def read_root(request: Request):
    return request.app.state.templates.TemplateResponse("index.html", {"request": request})

@router.get("/about")
async def about_page(request: Request):
    return request.app.state.templates.TemplateResponse("about.html", {"request": request})
