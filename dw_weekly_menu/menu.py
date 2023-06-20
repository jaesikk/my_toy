import os
import requests
from io import BytesIO
from PIL import Image
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def set_wallpaper_from_url(image_url):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    # 이미지 저장 경로
    today = datetime.now().strftime("%y%m%d")
    image_path = os.path.join(os.path.expanduser('~'), 'Desktop', f'wallpaper_{today}.jpg')

    # 이미지 저장
    image.save(image_path, 'JPEG')

    # 윈도우 바탕화면으로 설정
    command = 'REG ADD "HKEY_CURRENT_USER\\Control Panel\\Desktop" /v Wallpaper /t REG_SZ /d "{}" /f'.format(image_path)
    os.system(command)

    # 설정 적용
    os.system('RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters')


def get_image_src(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    print(html_content)
    # id='dext_body'인 span 태그 찾기
    # 로그인 정보
    login_id = 'jasic0627'
    login_pw = '@wotlr5414'

    # 세션 생성
    session = requests.Session()

    # 로그인 페이지 가져오기
    response = session.get(url)
    html_content = response.text

    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(html_content, 'html.parser')

    # 로그인 필드 값 설정
    input_id = soup.find('input', {'name': 'txtPC_LoginID'})
    input_pw = soup.find('input', {'name': 'txtPC_LoginPWTemp'})
    input_id['value'] = login_id
    input_pw['value'] = login_pw

    # 로그인 버튼 클릭
    button = soup.find('em', {'class': 'btn_bs_l'})
    submit_form = button.find_parent('form')
    action_url = submit_form.get('action')

    print('------------- 로그인 완료 -----------------')
    session.post(action_url, data=submit_form)
    #######################

    span_tag = soup.find('span', id='dext_body')
    print(span_tag)
    if span_tag:
        # span 태그 내의 img 태그 찾기
        img_tag = span_tag.find('img')

        if img_tag:
            # img 태그의 src 속성 값 가져오기
            image_src = img_tag.get('src')

            # 상대 경로를 절대 경로로 변환
            if image_src and not image_src.startswith('http'):
                parsed_url = urlparse(url)
                base_url = parsed_url.scheme + '://' + parsed_url.netloc
                image_src = base_url + '/' + image_src

            return image_src

    return None

########################
# 로그인 시도할 URL
# url = 'https://www.example.com/login'
#
# # 로그인 정보
# login_id = 'jasic0627'
# login_pw = '@wotlr5414'
#
# # 세션 생성
# session = requests.Session()
#
# # 로그인 페이지 가져오기
# response = session.get(url)
# html_content = response.text
#
# # BeautifulSoup으로 HTML 파싱
# soup = BeautifulSoup(html_content, 'html.parser')
#
# # 로그인 필드 값 설정
# input_id = soup.find('input', {'name': 'txtPC_LoginID'})
# input_pw = soup.find('input', {'name': 'txtPC_LoginPWTemp'})
# input_id['value'] = login_id
# input_pw['value'] = login_pw
#
# # 로그인 버튼 클릭
# button = soup.find('em', {'class': 'btn_bs_l'})
# submit_form = button.find_parent('form')
# action_url = submit_form.get('action')
#
# response = session.post(action_url, data=submit_form)
# # 이후 작업 수행


# 웹 페이지 URL
url = "https://direct.dongwon.com/WebSite/Basic/Board/BoardView.aspx?system=Board&BoardType=Normal&FromOuterYN=N&fdid=1298&MsgId=212757&DateBarYN=Y&BoardGubun=Normal&PageSize=15&PageCurrent=1&SortField=RegistDate&SortDirection=DESC&Cate=0&CateGubunYN=N&CateNm=&SearchGubun=All&SearchKeyword=&SelectedDay=All&SDate=&EDate=&LinkID="

print('--------------------------- 1 ----------------')
# 웹 페이지 내용 가져오기
response = requests.get(url)
print('--------------------------- 2 ----------------')
html_content = response.text
print('--------------------------- 3 ----------------')
# 이미지 src 추출
image_src = get_image_src(html_content)
print('--------------------------- 4 ----------------',image_src)
# 바탕화면으로 지정
set_wallpaper_from_url(image_src)
