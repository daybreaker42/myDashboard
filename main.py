from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import httpx
import asyncio
from fastapi.templating import Jinja2Templates
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
import os

# 라우터 임포트
from routers import trends, stocks, pages

# 프로젝트의 기본 디렉토리 경로를 설정합니다. __file__은 현재 파일(main.py)의 경로를 나타냅니다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # main.py 파일이 위치한 디렉토리의 절대 경로
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")  # templates 디렉토리의 절대 경로
STATIC_DIR = os.path.join(BASE_DIR, "static")  # static 디렉토리의 절대 경로

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작 시 HTTP 클라이언트 초기화"""
    app.state.http_client = httpx.AsyncClient()  # app.state에 http_client 저장
    print('starting http client...')
    yield
    """애플리케이션 종료 시 리소스 정리"""
    print('closing http client...')
    await app.state.http_client.aclose()  # app.state에 저장된 http_client 종료
    if hasattr(app.state, 'thread_pool') and app.state.thread_pool is not None:  # thread_pool 종료 로직 추가 및 확인
        app.state.thread_pool.shutdown(wait=True)  # 스레드 풀 종료 시 대기

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory=TEMPLATE_DIR)  # 절대 경로 사용

# app.state에 templates와 thread_pool 저장
app.state.templates = templates
app.state.thread_pool = ThreadPoolExecutor(max_workers=4)  # app.state에 직접 초기화 및 할당

# CORS 설정 부분 수정
PORT = 3000
ALLOWED_ORIGINS = [
    f"http://localhost:{PORT}",  # 로컬 개발 환경
    f"http://127.0.0.1:{PORT}",  # 로컬 대체 주소
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # 화이트리스트 방식으로 변경
    allow_credentials=True,
    allow_methods=["GET"],  # 필요한 HTTP 메서드만 허용
    allow_headers=["*"],
)

# 정적 파일 서빙을 위한 설정
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")  # 절대 경로 사용

# 라우터 등록
app.include_router(trends.router)
app.include_router(stocks.router)
app.include_router(pages.router)
