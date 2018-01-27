# from utils import *
#
# if __name__ == '__main__':
#     # result = get_top100_list()
#     # get_song_detail(result)
#     result = get_song_search('빨간맛')
#
#     for item in result:
#         print(item)

from utils.models import MelonCrawler

if __name__ == '__main__':
    crawler = MelonCrawler()
    # q = input('검색할 곡 명을 입력해주세요: ')
    # song_list = crawler.get_song_search(q)
    # q = input('검색할 아티스트를 입력해주세요: ')
    artist_list = crawler.get_search_artist('아이유')
    artist_list[0].get_detail()
