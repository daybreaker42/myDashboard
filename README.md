# myDashboard

- 크롬 창을 열자마자 내가 필요한 유용한 정보들이 보기 쉽게 보였으면 좋겠어서 제작함.
- 대시보드 형태로 보였으면 좋겠음.

## 구성

### 공통

- 새로고침이 필요한 부분 - google trends, 주식 등등은 5분마다 새로고침
  - 이때 다음 새로고침까지 남은 시간 표시.
- fetch시 로딩중 표시, 실패시 error 표시
- 좌우 padding을 넉넉하게
- image를 가져올 경우 cover를 사용해 이미지가 잘리지 않고 전체가 다 보이되 부모 element의 크기는 벗어나지 않게 설정

### 기능들

- 현재 시각 및 관심있는 국가 세계시각
  - 아래 있는 예시 데이터의 형식을 따르되, 보다 좋은 형식이 있으면 그렇게 진행
  - user가 나중에 추가/삭제/검색할 수 있도록 (local storage에 저장)
  - 실제 시각을 가져와 표시
  - [서울, GMT+9] 2025년 1월 1일 11:11:11 [오전]
  - [뉴욕, GMT-5] 2025년 1월 1일 11:11:11 [오전]
  - [영국, GMT] 2025년 1월 1일 11:11:11 [오전]
- 실시간 google trends (GET / <https://trends.google.co.kr/trending/rss?geo=KR>)
  - 예시 데이터 - [example-data.xml](./example-data.xml)
  - 새로고침 버튼 있었으면 좋겠음
  - 격자 형식으로 이미지/내용을보여줬으면 좋겠음
- daily google trends
  - <https://trends.google.co.kr/trends/trendingsearches/daily/rss?geo=KR>
  - 해당 데이터도 위에 데이터랑 형식 동일
  - 단, 실시간이 아닌 하루 동안의 실시간 데이터인점이 차이가 있음.
- 주요 주식 지표들 (나스닥, snp 500, 다우존스, VIX, 미국 5년물 국채, 미국 10년물 국채, 미국 30년물 국채)
  - 해당 지표들은 가능하면 그래프를 가져와 보여줬으면 좋겠음. (최근 3개월 변동 및 오늘 등락)
- about page
  - 제작일자: 250114
  - 제작자: HanSeongJun
  - 사용된 기술: (아래 있는것들)

## 사용된 주요 기술들

- fastapi, uvicorn
- tailwindcss
- local storage

## 디자인 특징

- 다크모드로 제작됨
- 미니멀리즘
- 반응형 웹 지원 (모바일, 데스크톱)

## 보안 설계 특징

- CORS 화이트리스트 정책 적용
  - 허용된 출처: localhost:30000, 127.0.0.1:30000
  - 허용된 HTTP 메서드: GET만 허용
- 정적 파일 접근 제한
- API 요청 속도 제한 적용

## 서버 실행 명령어

```bash
uvicorn main:app --reload --port 30000
```

## 기타 (해당 부분은 개발에 반영 X, 추후 참고용)

- google trends RSS 피드가 하나 더 있음 - <https://trends.google.co.kr/trends/trendingsearches/daily/rss?geo=KR>
  - daily인걸로 보아 1일간의 이슈들을 모아 보여주는듯
