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
    print("=" * 200)
    crawler = MelonCrawler()
    # q = input('검색할 곡 명을 입력해주세요: ')
    # song_list = crawler.get_song_search(q)
    # for song in song_list:
    #     print(song)
    # print("="*200)

    q = input('검색할 아티스트를 입력해주세요: ')
    artist_list = crawler.get_search_artist(q)
    iu = artist_list[0]
    print('iu.info')
    print(iu.info)
    print('')

    print('iu.award_history')
    print(iu.award_history)
    print('')

    print('iu.introduction')
    print(iu.introduction)
    print('')

    print('iu.activity_information')
    print(iu.activity_information)
    print('')

    print('iu.personal_information')
    print(iu.personal_information)
    print('')

    print('iu.related_information')
    print(iu.related_information)
    print('')

    artist_list = crawler.get_search_artist('아이유악대')
    dutbozap = artist_list[0]
    print('dutbozap.info')
    print(dutbozap.info)
    print('')

    print('dutbozap.award_history')
    print(dutbozap.award_history)
    print('')

    print('dutbozap.introduction')
    print(dutbozap.introduction)
    print('')

    print('dutbozap.activity_information')
    print(dutbozap.activity_information)
    print('')

    print('dutbozap.personal_information')
    print(dutbozap.personal_information)
    print('')

    print('dutbozap.related_information')
    print(dutbozap.related_information)
    print('')
    print("=" * 200)

    # song_list = artist_list[0].get_songs()
    # for index, song in enumerate(song_list):
    #     print(f"{index} : 곡명: {song['곡명']}, 아티스트: {song['아티스트']}, 앨범: {song['앨범']}")
    # print("=" * 200)


# ==================================================================================================================== #