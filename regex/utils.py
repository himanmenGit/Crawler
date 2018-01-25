import re

__all__ = (
    'get_tag_attribute',
    'get_tag_content',
    'find_tag',
)

def save_melon():
    '''
    멜론 사이트의 인기차트 1~50위에 해당하는 페이지를 melon.html로 저장
    :return: None
    '''
    import requests

    response = requests.get('https://www.melon.com/chart/index.htm')
    f = open('melon.html', 'wt')
    f.write(response.text)
    f.close()

def get_tag_attribute(attribute_name, tag_string):
    '''

    :param attribute_name: 태그가 가진 속석명
    :param tag_string: 태그 문자열
    :return: 속성이 가진 값
    '''
    p_first_tag = re.compile(r'^.*?<.*?>', re.S)
    first_tag = re.search(p_first_tag, tag_string).group()

    pattern = re.compile(r'^.*?<.*?{attribute_name}="(?P<value>.*?)".*?>'.format(
        attribute_name=attribute_name), re.DOTALL)
    m = pattern.search(first_tag)
    return m.group('value') if m else ''

def get_tag_content(tag_string):
    '''
    html에서 가장 안쪽 태그 사이에 있는 데이터를 들고 올떄 사용.
    :param tag_string: 태그 문자열
    :return: 태그의 가장 안쪽 데이터 없을 경우 공백
    '''
    pattern = re.compile(r'<.*?>(?P<value>.*)</.*?>', re.DOTALL)
    m = pattern.search(tag_string)

    if m:
        return get_tag_content(m.group('value'))
    elif re.search(r'[<>]', tag_string):
        return ''
    else:
        return tag_string

def find_tag(tag, tag_string, class_=None):
    '''
    tag_string에서 tag요소를 찾아 리턴
    :param tag: 찾을 tag 명
    :param tag_string: 검색할 tag 문자열
    :return: 첫번쨰로 찾은 tag 문자열
    '''
    p = re.compile(r'.*?<{tag}.*?{class_}.*?>(.*?)</{tag}>'.format(
        tag=tag,
        class_=f'class=".*?{class_}.*?"' if class_ else '',
    ), re.DOTALL)

    print(f'find_tag (tag: {tag}, class: {class_}, pattern: {p})')

    m = re.search(p, tag_string)
    if m:
        return m.group(1)
    else:
        ''