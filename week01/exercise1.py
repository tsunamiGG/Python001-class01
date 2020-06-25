import requests,pandas
from bs4 import BeautifulSoup as bs


def get_url_info(myurl):
    film_list = []
    headers = {
        'Cookie': 'uuid_n_v=v1; uuid=CF2A5180B44D11EA8C8DE3118EB8AC1A4B40B5FBD2F74EE1A61F05482897D817; mojo-uuid=f011bf395319af23ad9f86e1224dcca8; _lxsdk_cuid=172da9e4a3ec8-0d5ee2f5940bb7-f7d123e-144000-172da9e4a3ec8; _lxsdk=CF2A5180B44D11EA8C8DE3118EB8AC1A4B40B5FBD2F74EE1A61F05482897D817; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1592805708,1592830877,1592830931,1592830942; _csrf=cbbfe141e303af35121ffe5efb857746a4e3adb2a0639fe89dd0efbc5db771a2; mojo-session-id={"id":"101dbc0195ca482927d1f5dd106536ab","time":1592869913808}; mojo-trace-id=2; __mta=55409172.1592805708597.1592831009924.1592869934788.10; _lxsdk_s=172de7204ef-e6e-0fe-c32%7C%7C4',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
    }
    response = requests.get(myurl, headers=headers)
    bs_info = bs(response.text, 'html.parser')
    for movie in bs_info.find_all('div', attrs={'class': 'movie-hover-info'}, limit=10):
        name = movie.find(class_='name').text
        movie_info = movie.find_all(class_='movie-hover-title')
        tag = movie_info[1].text.strip()
        time = movie_info[3].text.strip()
        flim = {'name': name, 'tag': tag, 'time': time }
        film_list.append(flim)
    return film_list


url = 'https://maoyan.com/films?showType=2'
film_list = get_url_info(url)

print(film_list)

movie = pandas.DataFrame(film_list)
movie.to_csv('./movie.csv',index=False)
