from fastapi import APIRouter, Request, Depends
import httpx
import xmltodict

router = APIRouter()

'''
# /api/trends 예시 데이터
{
  "trends": [
    {
      "title": "김재환",
      "ht:approx_traffic": "100+",
      "description": null,
      "link": "https://trends.google.com/trending/rss?geo=KR",
      "pubDate": "Thu, 22 May 2025 00:10:00 -0700",
      "ht:picture": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcTdaHMjwaHV9rV6AM8wz4iI324p2JwZvhExidmzIW07fY8XB3rDl8Jb5O8rbeE",
      "ht:picture_source": "네이트 뉴스",
      "ht:news_item": [
        {
          "ht:news_item_title": "백종원, 결국 개인 재산 내놓나 \"모두 만나고 싶지만…\"",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://news.nate.com/view/20250521n09368",
          "ht:news_item_picture": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcTdaHMjwaHV9rV6AM8wz4iI324p2JwZvhExidmzIW07fY8XB3rDl8Jb5O8rbeE",
          "ht:news_item_source": "네이트 뉴스"
        },
        {
          "ht:news_item_title": "[단독] “왜 우리만 빠졌나”…백종원, 연돈볼카츠 간담회 제외 논란",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://www.mk.co.kr/news/economy/11323878",
          "ht:news_item_picture": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRlfspuVdBm6yVCIbZ7AM2Lk4D-WxBjCF4N923SNdM8ggPtzU2Q3tXJfbyYBjE",
          "ht:news_item_source": "매일경제"
        },
        {
          "ht:news_item_title": "백종원, 결국 개인 재산까지 내놓나…‘점주 상생위’ 승부수",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://www.segye.com/newsView/20250522503200",
          "ht:news_item_picture": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRRK4eA3sDMUlctTcOUEurSk6rJSW250QaS7pXGPssCPy05dNFT11FTPhC58lk",
          "ht:news_item_source": "세계일보"
        }
      ]
    },
    {
      "title": "애슬레틱스 대 에인절스",
      "ht:approx_traffic": "500+",
      "description": null,
      "link": "https://trends.google.com/trending/rss?geo=KR",
      "pubDate": "Wed, 21 May 2025 23:10:00 -0700",
      "ht:picture": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcSr1xJKafR4xvM8T13c0j2SQj3sIbUbgG-PjQKxhiuHPHY-0iy7zP6BngDj7b8",
      "ht:picture_source": "스포츠경향",
      "ht:news_item": [
        {
          "ht:news_item_title": "‘연타석 홈런’ 오하피 ‘오해피’···LAA, 애슬레틱스 10-5 꺾고 ‘6연승 신바람’",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://sports.khan.co.kr/article/202505221446013",
          "ht:news_item_picture": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcSr1xJKafR4xvM8T13c0j2SQj3sIbUbgG-PjQKxhiuHPHY-0iy7zP6BngDj7b8",
          "ht:news_item_source": "스포츠경향"
        },
        {
          "ht:news_item_title": "'다저스전 스윕' 에인절스, 5연승 신바람···애슬레틱스에 7-5 역전승, AL 서부지구 탈꼴찌",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://m.news.nate.com/view/20250521n22118",
          "ht:news_item_picture": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRj8Z8i6pFivlVci6HAk0DOR0RIJu4QY1OT_zjd7k7fHUcP2DfGUt6X4L2XA8w",
          "ht:news_item_source": "네이트 뉴스"
        },
        {
          "ht:news_item_title": "[MLB] 에인절스, 오클랜드 원정서 4연전 싹쓸이…오홉 2홈런 포함 4방 폭발",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "http://www.newsflix.co.kr/news/articleView.html?idxno=20078",
          "ht:news_item_picture": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKm7Vbp892_ybeLvQgwrZEmR5fv1h9im15bGZnsMbgJfjDC45ATH9xJfU00rQ",
          "ht:news_item_source": "뉴스플릭스"
        }
      ]
    },
    {
      "title": "한화솔루션",
      "ht:approx_traffic": "200+",
      "description": null,
      "link": "https://trends.google.com/trending/rss?geo=KR",
      "pubDate": "Wed, 21 May 2025 23:00:00 -0700",
      "ht:picture": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcS2a7sJ0YlCs72RC4G3eQjyF2yKIwQk4kx7Z_F8ME-M2Rws_RiTiuFWqbstu4E",
      "ht:picture_source": "한국무역협회",
      "ht:news_item": [
        {
          "ht:news_item_title": "美, '한화큐셀 청원' 동남아산 태양광 장비에 곧 고율관세",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://www.kita.net/board/totalTradeNews/totalTradeNewsDetail.do;JSESSIONID_KITA=DDB9CE715366FDDB40B81FC06F2F872A.Hyper?no=92064&siteId=2",
          "ht:news_item_picture": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcS2a7sJ0YlCs72RC4G3eQjyF2yKIwQk4kx7Z_F8ME-M2Rws_RiTiuFWqbstu4E",
          "ht:news_item_source": "한국무역협회"
        },
        {
          "ht:news_item_title": "냉탕·온탕 오가는 태양광주...증권가 “최소 내년까지 실적 견고”",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://marketin.edaily.co.kr/News/ReadE?newsId=03778566642171216",
          "ht:news_item_picture": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQSzGQvEKaW5XC0TSiClL-fVb3XM9KoNfavVMVarKBaQMigiLR2CovBZj6q8I0",
          "ht:news_item_source": "마켓인"
        },
        {
          "ht:news_item_title": "한화솔루션 미국서 중국 태양광 공세 극복 기류, 박승덕 사상 최대 영업이익 정조준",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://www.businesspost.co.kr/BP?command=article_view&num=396271",
          "ht:news_item_picture": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEn-UlOB5FqoiB21TlsXHodm_9bL7z5A7xrfTs0rKoG_EQqhjOoRizgoxtL2g",
          "ht:news_item_source": "비즈니스포스트"
        }
      ]
    },
    {
      "title": "ira",
      "ht:approx_traffic": "200+",
      "description": null,
      "link": "https://trends.google.com/trending/rss?geo=KR",
      "pubDate": "Wed, 21 May 2025 23:00:00 -0700",
      "ht:picture": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQ65wA7H4TjB-oqGqd9ABWfBaaJXgzWADK3u42hjNe7u_6Yk4i1-KyfyMXN06Q",
      "ht:picture_source": "Yahoo News UK",
      "ht:news_item": [
        {
          "ht:news_item_title": "Former NI Secretary rejects reports he ‘turned a blind eye’ to IRA crimes",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://uk.news.yahoo.com/former-ni-secretary-rejects-reports-175659845.html",
          "ht:news_item_picture": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQ65wA7H4TjB-oqGqd9ABWfBaaJXgzWADK3u42hjNe7u_6Yk4i1-KyfyMXN06Q",
          "ht:news_item_source": "Yahoo News UK"
        },
        {
          "ht:news_item_title": "Former NI Secretary rejects reports he ‘turned a blind eye’ to IRA crimes",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://www.msn.com/en-gb/news/uknews/former-ni-secretary-rejects-reports-he-turned-a-blind-eye-to-ira-crimes/ar-AA1FdFcr",
          "ht:news_item_picture": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcS9yPJMcBggCNuFG4bUBN11UxNE02yrua1VNfUNbnUNkGojYt3cvWfdDDYINsw",
          "ht:news_item_source": "MSN"
        },
        {
          "ht:news_item_title": "Former NI Secretary rejects reports he ‘turned a blind eye’ to IRA crimes",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://www.limerickleader.ie/news/northern-ireland/1807715/former-ni-secretary-rejects-reports-he-turned-a-blind-eye-to-ira-crimes.html",
          "ht:news_item_picture": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQYrmvLxMTWgwtIYJAKfir4eSV3aTtsaftJg-_ywLJGPfExOiTmcUmzoFEHErA",
          "ht:news_item_source": "Limerick Leader"
        }
      ]
    },
    {
      "title": "미국",
      "ht:approx_traffic": "200+",
      "description": null,
      "link": "https://trends.google.com/trending/rss?geo=KR",
      "pubDate": "Wed, 21 May 2025 22:00:00 -0700",
      "ht:picture": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTG8yoE4y5vwn6vza1aJb-uOLDFzF0bZCmj-QF_XWetXpek-bk3O-nM75SipVM",
      "ht:picture_source": "연합뉴스",
      "ht:news_item": [
        {
          "ht:news_item_title": "요동치는 미국·일본 국채 시장…국가부채 '공포'",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://www.yna.co.kr/view/AKR20250522065400009",
          "ht:news_item_picture": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTG8yoE4y5vwn6vza1aJb-uOLDFzF0bZCmj-QF_XWetXpek-bk3O-nM75SipVM",
          "ht:news_item_source": "연합뉴스"
        },
        {
          "ht:news_item_title": "美이어 日·유럽도 국채금리 급등…안전자산 위상 '흔들'",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://marketin.edaily.co.kr/News/ReadE?newsId=03598166642171544",
          "ht:news_item_picture": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSeUn9XwV5M8ARG3oPGMFd9IUIUph9ir_417I-9bi9zzsTJ3j4VaNwCBeBGJzk",
          "ht:news_item_source": "마켓인"
        },
        {
          "ht:news_item_title": "미 주식·채권값 동반급락···‘트럼프 감세’ 재정적자 확대 우려 여파",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://www.khan.co.kr/article/202505220730001",
          "ht:news_item_picture": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQRto98sRknYmAAaONqhoY7Cbz9qucMQ1l9l544IMn9wFA-9UYyravdIkL2tYE",
          "ht:news_item_source": "경향신문"
        }
      ]
    },
    {
      "title": "엘지트윈스",
      "ht:approx_traffic": "200+",
      "description": null,
      "link": "https://trends.google.com/trending/rss?geo=KR",
      "pubDate": "Wed, 21 May 2025 21:40:00 -0700",
      "ht:picture": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcR1IhU1BDEE-1As8HvjA5yaiEgP4-O0DG53bPAqZBzZP4MYTyOBX24R5OUUS50",
      "ht:picture_source": "연합뉴스",
      "ht:news_item": [
        {
          "ht:news_item_title": "LG 응원팬들의 열정",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://www.yna.co.kr/view/PYH20250520205300051",
          "ht:news_item_picture": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcR1IhU1BDEE-1As8HvjA5yaiEgP4-O0DG53bPAqZBzZP4MYTyOBX24R5OUUS50",
          "ht:news_item_source": "연합뉴스"
        },
        {
          "ht:news_item_title": "\"희생플라이 타점 생각했는데 만루홈런\"…홍창기 빈자리 메운 '매운맛'",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://m.news.nate.com/view/20250522n00496",
          "ht:news_item_picture": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcSvDEaMY-rVx7PQfJRGCPOmXxwk4NpMjYEgH7hZWlD5RXlsOA93WjBCW3z58mE",
          "ht:news_item_source": "네이트 뉴스"
        },
        {
          "ht:news_item_title": "14-2로 앞섰는데 필승조까지 나왔어야 했나…0아웃 4실점+0아웃 2실점, 염경엽 “힘든 경기였는데 야수들이 고생 많았다”",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://news.mt.co.kr/mtview.php?no=202505202251773945O",
          "ht:news_item_picture": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0jFmrZcEOVbZcbcgtd7p696ABwSeeERkUSpiMH6nh_ZBCA8BOeXKZFHKJUEM",
          "ht:news_item_source": "머니투데이"
        }
      ]
    },
    {
      "title": "최정문",
      "ht:approx_traffic": "200+",
      "description": null,
      "link": "https://trends.google.com/trending/rss?geo=KR",
      "pubDate": "Wed, 21 May 2025 21:10:00 -0700",
      "ht:picture": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSuiNL8un901GN7__iIR3_9lzUrglVLg0vzoG0hSHV-bN25OW3td_ugmryQM4g",
      "ht:picture_source": "네이트 뉴스",
      "ht:news_item": [
        {
          "ht:news_item_title": "[사진]정지인, '긴장되는 시사회'",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://news.nate.com/view/20250521n40802?mid=e1200",
          "ht:news_item_picture": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSuiNL8un901GN7__iIR3_9lzUrglVLg0vzoG0hSHV-bN25OW3td_ugmryQM4g",
          "ht:news_item_source": "네이트 뉴스"
        },
        {
          "ht:news_item_title": "\"연기 즐거워했는데\"…故 박보람 출연 '내가 누워있을 때' 베일 벗었다",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://www.edaily.co.kr/News/Read?newsId=01485846642171544&mediaCodeNo=258",
          "ht:news_item_picture": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTf9kTRdOuU6zv-u0x9mw79riPtlXW0D8aQZdIoC0FK97nNSkIyEsRpt0Jc-p0",
          "ht:news_item_source": "이데일리"
        },
        {
          "ht:news_item_title": "[사진]오우리, '내가 누워있을 때'에서 만나요",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://www.chosun.com/entertainments/entertain_photo/2025/05/21/TNBZ7JHISTIZ3P57DRQCEGBZOM/",
          "ht:news_item_picture": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSkfC2m_VQGHD6ls_P5hnxl-NFob8MuCMzGjLBsBvIj228CtqqkNZ1YylgMn4g",
          "ht:news_item_source": "조선일보"
        }
      ]
    },
    {
      "title": "쿠팡 육개장",
      "ht:approx_traffic": "500+",
      "description": null,
      "link": "https://trends.google.com/trending/rss?geo=KR",
      "pubDate": "Wed, 21 May 2025 21:00:00 -0700",
      "ht:picture": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfKmhZ-cBeUlXbaL9kEqnwb55XgIm3WFum-djZ5_RfsADirYUfIq1SvDWBkpQ",
      "ht:picture_source": "한국경제",
      "ht:news_item": [
        {
          "ht:news_item_title": "'육개장 컵라면 36개 5000원' 쿠팡 대란…\"난 왜 몰랐을까\"",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://www.hankyung.com/article/2025052291197",
          "ht:news_item_picture": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfKmhZ-cBeUlXbaL9kEqnwb55XgIm3WFum-djZ5_RfsADirYUfIq1SvDWBkpQ",
          "ht:news_item_source": "한국경제"
        },
        {
          "ht:news_item_title": "“컵라면 36개 5000원” 쿠팡 가격 실수에 한밤중 주문 대란… 900개 배송 인증도",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://www.chosun.com/economy/market_trend/2025/05/22/SLPEQ6WFJJBNFGFKPNDANADONE/",
          "ht:news_item_picture": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTC8bYQ0z16bTMfE6lqKJqtQLxoEGWiUVS6kTYsGnUsnn9XUVPvj6jb4F4aA5o",
          "ht:news_item_source": "조선일보"
        },
        {
          "ht:news_item_title": "육개장 컵라면 36개가 5000원?…쿠팡 배송 대란 '몸살'",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://news.nate.com/view/20250522n17673",
          "ht:news_item_picture": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRB6Rs0kaZ_A7dJeLNhN3l0z-zh0xsoR9MMNWxbYJNVM3Ga_EospvokNrnXi90",
          "ht:news_item_source": "네이트 뉴스"
        }
      ]
    },
    {
      "title": "월드컵",
      "ht:approx_traffic": "100+",
      "description": null,
      "link": "https://trends.google.com/trending/rss?geo=KR",
      "pubDate": "Wed, 21 May 2025 20:40:00 -0700",
      "ht:picture": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoOc7fZXiuwHmeWnJ_X3ibs_ZQWPzv-GXtmFynb5PVq8JRenK1r3EzhaW0mmk",
      "ht:picture_source": "연합뉴스",
      "ht:news_item": [
        {
          "ht:news_item_title": "내달 북중미 월드컵 예선 쿠웨이트전, 서울월드컵경기장서 개최",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://www.yna.co.kr/view/AKR20250522103000007",
          "ht:news_item_picture": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoOc7fZXiuwHmeWnJ_X3ibs_ZQWPzv-GXtmFynb5PVq8JRenK1r3EzhaW0mmk",
          "ht:news_item_source": "연합뉴스"
        },
        {
          "ht:news_item_title": "한국축구는‘긴장의 6월’일본축구는‘여유의 6월’ [이종세의 스포츠 코너]",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://www.mk.co.kr/news/sports/11323608",
          "ht:news_item_picture": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRybkmKCbMNDQedlAaaSEAmyDC2ECEjCDhmkRuQZ01ZYMTd-qrnEtL8c4JjS1g",
          "ht:news_item_source": "매일경제"
        },
        {
          "ht:news_item_title": "홍명보 직관 경기서 보란듯 멀티골…'득점선두' 전진우, A 대표팀 향해 전진",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://news.nate.com/view/20250522n03981",
          "ht:news_item_picture": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQg1LA4cFdC1TH4fvOFoXuRz-atRqJEcdJApM7GeU-c4VMgXppbrwwyiiw96j0",
          "ht:news_item_source": "네이트 뉴스"
        }
      ]
    },
    {
      "title": "박혁권",
      "ht:approx_traffic": "1000+",
      "description": null,
      "link": "https://trends.google.com/trending/rss?geo=KR",
      "pubDate": "Wed, 21 May 2025 20:20:00 -0700",
      "ht:picture": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQlnP0H2A3D2i8XDKlqh-3QO_huqw86jqmLvNPZuLnojyzBIh_0m4a1Koec33A",
      "ht:picture_source": "매일경제",
      "ht:news_item": [
        {
          "ht:news_item_title": "“밥줄 끊겨도 이재명”…은퇴하고 지지 운동 결심했었단 이 배우",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://www.mk.co.kr/news/culture/11323674",
          "ht:news_item_picture": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQlnP0H2A3D2i8XDKlqh-3QO_huqw86jqmLvNPZuLnojyzBIh_0m4a1Koec33A",
          "ht:news_item_source": "매일경제"
        },
        {
          "ht:news_item_title": "배우 박혁권 “밥줄 끊겨도 이재명”…제주서 지지연설 중 울컥",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://www.hani.co.kr/arti/politics/politics_general/1198827.html",
          "ht:news_item_picture": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQHF0Nty0cAhJr5al4dfwQ9VBKw_CKbVpMMhy1rTJEPnXGfmr9ycmnys-Y1pX8",
          "ht:news_item_source": "한겨레"
        },
        {
          "ht:news_item_title": "배우 박혁권이 이재명 유세장에? ...VIP 방불케한 철통경호",
          "ht:news_item_snippet": null,
          "ht:news_item_url": "https://www.jejusori.net/news/articleView.html?idxno=436613",
          "ht:news_item_picture": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRtJxIOl-NNmQiFwDl-eXZouCRBaY2FygXogaThS_TSgxrxqu7_BaD70GKW_ak",
          "ht:news_item_source": "제주의소리"
        }
      ]
    }
  ]
}
'''
# MARK: trends api
@router.get("/api/trends")
async def get_trends(request: Request):
    """Google Trends RSS 피드에서 데이터 가져오기"""
    # lifespan을 통해 관리되는 http_client를 request.app.state를 통해 사용합니다.
    client = request.app.state.http_client
    response = await client.get("https://trends.google.co.kr/trending/rss?geo=KR")
    data = xmltodict.parse(response.text)
    items = data['rss']['channel']['item']
    return {"trends": items}

# MARK: daily trends api
# @router.get("/api/trends/daily")
# async def get_daily_trends(request: Request):
#     """Google Daily Trends RSS 피드에서 데이터 가져오기"""
#     # lifespan을 통해 관리되는 http_client를 request.app.state를 통해 사용합니다.
#     client = request.app.state.http_client
#     response = await client.get("https://trends.google.co.kr/trends/trendingsearches/daily/rss?geo=KR")
#     data = xmltodict.parse(response.text)
#     items = data['rss']['channel']['item']
#     return {"trends": items}
