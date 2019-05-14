from bs4 import BeautifulSoup
from URLs import UTANET_TOP, SEARCH
from soup_util import get_soup, add_query
import Levenshtein


def search_lyrics_from_query(title, artists=''):
    q = []
    a_q = ('Aselect', '2')
    b_q = ('Bselect', '3')
    title_q = ('Keyword', title)
    q.append(a_q)
    q.append(b_q)
    q.append(title_q)

    url = add_query(UTANET_TOP + SEARCH, q)
    soup = get_soup(url)

    result_box = soup.find('div', class_='result_table last')   # 検索結果一覧のボックス
    result_tbody = result_box.find('tbody')                     # result_box内のtbody
    result_musics = result_tbody.find_all('tr')

    min_id = False
    min_dist = 100
    for music in result_musics:
        cur_title = music.find('td', class_='side td1').find('a').text
        cur_artists = music.find('td', class_='td2').find('a').text
        cur_id = music.find('td', class_='side td1').find('a').get('href')

        dist = Levenshtein.distance(artists, cur_artists) + Levenshtein.distance(title, cur_title)
        if min_dist > dist:
            min_dist = dist
            min_id = cur_id

        # print('title: {} \nartist: {} \nmusic id: {}\n'.format(cur_title, cur_artists, cur_id))

    return UTANET_TOP + min_id, min_dist


def get_lyrics_from_lyrics_page(url):
    soup = get_soup(url)
    lyrics_text = soup.find('div', id='kashi_area').text

    return lyrics_text


if __name__ == '__main__':
    url, dist = search_lyrics_from_query('Tulip', '速水奏')
    print(url)
    lyrics = get_lyrics_from_lyrics_page(url)

    print(lyrics)
