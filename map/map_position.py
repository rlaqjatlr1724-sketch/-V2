import requests
from bs4 import BeautifulSoup
import json

# 1. 사이트에서 HTML 가져오기 (헤더 추가로 차단 방지)
url = "https://www.ksponco.or.kr/map?gnbOpen=Y"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=headers)
response.encoding = 'utf-8' # 한글 깨짐 방지
html_content = response.text

# 2. BeautifulSoup으로 파싱
soup = BeautifulSoup(html_content, 'html.parser')

# 3. 데이터 추출
facilities = []

# 'data-x' 속성을 가진 모든 <a> 태그를 찾습니다.
# (화장실 뿐만 아니라 주차장, 경기장 등 모든 시설이 이 방식으로 되어 있을 겁니다)
for tag in soup.find_all('a', attrs={'data-x': True}):
    try:
        facility = {
            "id": tag.get('id'),                # 예: facility_5_1
            "name": tag.get_text(strip=True),   # 예: 화장실1
            "x": int(tag.get('data-x')),        # 예: 492 (픽셀좌표 X)
            "y": int(tag.get('data-y')),        # 예: 62 (픽셀좌표 Y)
            "desc": tag.get('data-info'),       # 예: 북2문으로 들어와...
            "category": "toilet" if "화장실" in tag.get_text() else "others" # 이름으로 카테고리 임시 분류
        }
        facilities.append(facility)
    except ValueError:
        continue # 좌표가 숫자가 아닌 경우 건너뜀

# 4. 결과 확인 및 저장
print(f"총 {len(facilities)}개의 시설물을 찾았습니다!")
print(json.dumps(facilities[:3], indent=4, ensure_ascii=False)) # 상위 3개만 미리보기

# 파일로 저장 (백엔드에서 바로 쓸 수 있게)
with open('olympic_facilities.json', 'w', encoding='utf-8') as f:
    json.dump(facilities, f, ensure_ascii=False, indent=4)

print("저장 완료: olympic_facilities.json")