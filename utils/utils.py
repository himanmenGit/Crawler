import os

import requests
from bs4 import BeautifulSoup

__all__ = (
    'get_source',
    'get_response',
)


def get_source(**kwargs):
    """

    :param kwargs: 데이터디렉터리, 데이터경로, 새로받는가, url, params
    :return: None or BeautifulSoup instance
    """
    join_data_dir = kwargs.get('data_dir')
    join_data_path = kwargs.get('data_path')
    refresh_html = kwargs.get('is_refresh')
    request_url = kwargs.get('url')
    request_params = kwargs.get('params')

    file_path = os.path.join(join_data_dir, join_data_path)
    try:
        file_mode = 'wt' if refresh_html else 'xt'
        with open(file_path, file_mode) as f:
            source = get_response(False, url=request_url, params=request_params)

            # 만약 받은 길이가 지나치게 짧은 경우 예외를 일으키고
            # 예외 블럭에서 기록한 파일을 삭제하도록 함
            file_length = f.write(source)
            if file_length < 10:
                raise ValueError('파일이 너무 짧습니다.')
    except FileExistsError:
        print(f'"{file_path}" file is already exists!')
        source = open(file_path, 'rt').read()
    except ValueError:
        os.remove(file_path)
        return None

    return BeautifulSoup(source, 'lxml')


def get_response(is_soup=True, **kwargs):
    request_url = kwargs.get('url')
    request_params = kwargs.get('params')
    response = requests.get(request_url, request_params)

    if is_soup:
        return BeautifulSoup(response.text, 'lxml')
    else:
        return response.text

