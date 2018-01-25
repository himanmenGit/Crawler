import requests
import re
from bs4 import BeautifulSoup
import os.path

__all__ = (
    'get_top100_list',
)

def get_top100_list(refresh_html=False):
    '''
    실시간 차트 1~100위의 리스트 반환
    :파일위치:
        현재 파일(모듈)의 위치를 사용한 상위 디렉토리 경로(crawler디렉토리):
            os.path.dirname(os.path.abspath(__name__))
        os.path.join()
        data/chart_realtile_100.html
    :param refresh_html: True일 경우, 무조건 새 HTML을 받아와 저장
    :return: 100위 까지의 dict list를 반환
    '''

    #프로젝트 컨테이너 폴더 경로
    path_module = os.path.abspath(__name__)
    print(f'path_module: {path_module}')

    root_dir = os.path.dirname(path_module)
    print(f'root_dir: {root_dir}')

    # data/폴더 경로
    path_data_dir = os.path.join(root_dir, 'data')
    print(f'path_data_dir: {path_data_dir}')

    # 만약에 path_data_dir에 해당하는 폴더가 없을 경우 생성해 준다.
    # 실행시 crawler/data폴더가 생성되어야 함.

    os.makedirs(path_data_dir, exist_ok=True)

    # 1-100위 주소
    url_chart_realtime = 'https://www.melon.com/chart/index.htm'

    # 1~100위에 해당하는 웹페이지 HTML을
    # data/chart_realtime_html에 저장
    source = ''

    file_path = os.path.join(path_data_dir, 'chart_realtime.html')
    try:
        file_mode = 'wt' if refresh_html else 'xt'
        with open(file_path, file_mode) as f:
            response = requests.get(url_chart_realtime)
            source = response.text
            f.write(source)
    except FileExistsError as e:
        print(f'"{file_path}" file is already exists!')
        source = open('melon.html', 'rt').read()

    soup = BeautifulSoup(source, 'lxml')

    result = list()

    for tr in soup.find_all('tr', class_=['lst50','lst100']):
        rank = tr.find('span', class_='rank').text
        title = tr.find('div', class_='rank01').find('a').text
        artist = tr.find('div', class_='rank02').find('a').text
        album = tr.find('div', class_='rank03').find('a').text
        url_img_cover = tr.find('a', class_='image_typeAll').find('img').get('src')
        # .* -> 임의 문자의 최대 반복
        # \. -> '.' 문자
        # .*?. -> '/'이 나오기 전까지의 최소 반복
        p = re.compile(r'(.*\..*?)/')
        url_img_cover = re.search(p, url_img_cover).group(1)

        result.append({
            'rank': rank,
            'title': title,
            'url_img_cover': url_img_cover,
            'artist': artist,
            'album': album
        })
    return result