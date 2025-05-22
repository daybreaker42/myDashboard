from . import pages  # 수정: 'pages' 모듈을 상대 경로('.pages')로 임포트하여 명시적으로 패키지 내 모듈임을 나타냅니다. 기존 'from pages import pages'는 pages 모듈 내의 'pages' 객체를 가져오려는 의도였을 수 있으나, main.py의 사용 방식(routers.pages.router)과 더 잘 부합하도록 모듈 자체를 가져옵니다.
from . import stocks # 수정: 'stocks' 모듈을 상대 경로('.stocks')로 임포트합니다.
from . import trends # 수정: 'trends' 모듈을 상대 경로('.trends')로 임포트합니다.
