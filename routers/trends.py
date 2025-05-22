from fastapi import APIRouter, Request, Depends
import httpx
import xmltodict

router = APIRouter()

@router.get("/api/trends")
async def get_trends(request: Request):
    """Google Trends RSS 피드에서 데이터 가져오기"""
    # lifespan을 통해 관리되는 http_client를 request.app.state를 통해 사용합니다.
    client = request.app.state.http_client
    response = await client.get("https://trends.google.co.kr/trending/rss?geo=KR")
    data = xmltodict.parse(response.text)
    items = data['rss']['channel']['item']
    return {"trends": items}

@router.get("/api/trends/daily")
async def get_daily_trends(request: Request):
    """Google Daily Trends RSS 피드에서 데이터 가져오기"""
    # lifespan을 통해 관리되는 http_client를 request.app.state를 통해 사용합니다.
    client = request.app.state.http_client
    response = await client.get("https://trends.google.co.kr/trends/trendingsearches/daily/rss?geo=KR")
    data = xmltodict.parse(response.text)
    items = data['rss']['channel']['item']
    return {"trends": items}
