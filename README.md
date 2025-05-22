# myDashboard

개인화된 정보 대시보드 - 필요한 정보를 한눈에 볼 수 있는 웹 애플리케이션

## 프로젝트 개요

- 목적: 크롬 시작 페이지로 활용할 수 있는 개인화된 대시보드 제작
- 특징: 실시간 정보 업데이트, 반응형 디자인, 다크모드 지원

## 주요 기능

### 1. 세계 시계

- 다중 시간대 동시 표시
- 24시간 형식 지원
- Local Storage 기반 사용자 설정 저장
- 기본 시간대: 뉴욕(GMT-5), 런던(GMT+0), 서울(GMT+9)

### 2. Google Trends

- 실시간/일간 트렌드 토글 기능
- 각 트렌드 항목별 상세 뉴스 확장/축소
- 전체 뉴스 동시 확장/축소 기능
- 5분 주기 자동 업데이트
- 남은 시간 카운트다운 표시

### 3. 시장 지표

- 주요 지표 실시간 모니터링
  - 나스닥, S&P 500, 다우존스
  - VIX (변동성 지수)
  - 미국 국채 수익률 (5년, 10년, 30년)
- 차트 시각화 (Line Chart)
- 등락률 색상 구분 표시
- 5분 주기 자동 업데이트

## 기술 스택

### 백엔드

- FastAPI - Python 웹 프레임워크
- Uvicorn - ASGI 서버
- yfinance - 주식 데이터 API
- httpx - 비동기 HTTP 클라이언트

### 프론트엔드

- TailwindCSS - 유틸리티 우선 CSS 프레임워크
- Chart.js - 데이터 시각화
- Local Storage - 클라이언트 측 데이터 저장

## 보안 설계

### CORS 정책

- 화이트리스트 기반 출처 제한
  - localhost:30000
  - 127.0.0.1:30000
- HTTP 메서드 제한 (GET only)
- 정적 파일 접근 제한

## 실행 방법

### 개발 환경

```bash
fastapi dev main.py
```

### 운영 환경 및 배포 계획

#### 운영 환경

- Docker Container 기반 운영
- 멀티 플랫폼 지원: Windows, Linux
- 컨테이너 자동 재시작 정책 적용

#### Docker 배포 구성

```bash
# 컨테이너 실행
docker run -d \
  --name mydashboard \
  --restart unless-stopped \
  -p 30000:30000 \
  -v /app/data:/data \
  siejwkaodj/mydashboard:latest

# 또는 한줄 명령어
docker run -d --name mydashboard --restart unless-stopped -p 30000:30000 -v /app/data:/data siejwkaodj/mydashboard:latest
```

### 시스템 요구사항 및 리소스 사용량

- 하드웨어 요구사항:
  - CPU: 2 cores (평균 사용률 10-15%)
  - RAM: 2GB (피크 시 최대 500MB 사용)
  - Storage: 1GB (로그 및 캐시 포함)
- 네트워크:
  - 대역폭: 최소 10Mbps
  - 월간 예상 트래픽: 5GB 이하

### 트래픽 예측

- 일일 예상 사용자: 10명
- 피크 시간대 동시 접속: 최대 5명
- API 호출 빈도:
  - Google Trends API: 5분당 1회
  - 주식 데이터 API: 5분당 1회
  - 총 일일 API 호출: 약 576회 (2개 API × 12회/시간 × 24시간)

### 확장 계획

1. **유익한 정보 추가 (대시보드 기능 확장)**
   - **오늘의 날씨 정보**: OpenWeatherMap API 또는 기상청 API를 활용하여 현재 날씨, 예보 표시
   - **오늘의 주요 일정**: Google Calendar API, Microsoft Outlook Calendar API 등과 연동하여 일정 표시
   - **주요 환율 정보**: ExchangeRate-API 등을 활용하여 주요 통화 환율 변동 표시
   - **개인화된 할 일 목록 (To-do List)**: 사용자가 직접 할 일을 추가하고 관리할 수 있는 기능

2. 인증 및 권한
   - JWT 기반 사용자 인증
   - Role 기반 접근 제어 (RBAC)
   - OAuth2.0 소셜 로그인 지원

3. 데이터 저장
   - **MariaDB 도입**: To-do List 등 사용자 데이터 저장 및 관리
   - 사용자별 설정 저장
   - 즐겨찾기 기능
   - 개인화된 대시보드 레이아웃 저장

4. 성능 최적화
   - CDN 적용 (정적 자원)

5. 모니터링
   - Prometheus + Grafana 도입
   - API 성능 모니터링
   - 리소스 사용량 추적

## 기타 (해당 부분은 개발에 반영 X, 추후 참고용)

- google trends RSS 피드가 하나 더 있음 - <https://trends.google.co.kr/trends/trendingsearches/daily/rss?geo=KR>
  - daily인걸로 보아 1일간의 이슈들을 모아 보여주는듯
- **추가 개발 고려 사항:**
  - Redis 캐시 도입 (API 응답 캐싱, 세션 관리)

### 리펙토링 고려사항

- 기능 관련해서 수정해야 하는 특정 부분은 주석에 `#feat`으로 표시해놓음
