from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import numpy as np

_domain = 'https://letterboxd.com/'

def scrape_list(list_link):
    
    film_rows = []
    film_rows.append(['Film_title', 'Release_year', 'Director', 'Average_rating','Letterboxd URL'])
    
    while True:
        list_page = requests.get(list_link)
        
        # check to see page was downloaded correctly
        if list_page.status_code != 200:
            encounter_error("")

        soup = BeautifulSoup(list_page.content, 'html.parser')
        # browser.get(following_url)
        
        # grab the main film grid
        table = soup.find('ul', class_='poster-list')
        if table is None:
            return None
        
        films = table.find_all('li')
        
        # iterate through films
        for film in tqdm(films):
            
            panel = film.find('div').find('img')
            film_name = panel['alt']
            
            # Obtaining release year, director and average rating of the movie
            film_card = film.find('div').get('data-target-link')
            film_page = _domain + film_card
            filmget = requests.get(film_page)
            film_soup = BeautifulSoup(filmget.content, 'html.parser')
            
            release_year = film_soup.find('meta', attrs={'property':'og:title'}).attrs['content'][-5:-1]
            director = film_soup.find('meta', attrs={'name':'twitter:data1'}).attrs['content']
            
            # try to find average rating, if not insert a nan
            try:
                average_rating = float(film_soup.find('meta', attrs={'name':'twitter:data2'}).attrs['content'][:4])
            except:
                average_rating = np.nan

            film_rows.append([film_name, int(release_year), director, average_rating, _domain+film_card])
            
        # check if there is another page of ratings
        next_button = soup.find('a', class_='next')
        if next_button is None:
            break
        else:
            list_link = _domain + next_button['href']
            
    return film_rows
