from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import numpy as np

_domain = 'https://letterboxd.com/'

def scrape_list(list_link):
    """
    Takes in a Letterboxd link and outputs a list of film title, release year, 
    director, cast, average rating and letterboxd url
    """
    
    film_rows = []
    film_rows.append(['Film_title', 'Release_year', 'Director', 'Cast', 'Personal_rating', 'Average_rating','Letterboxd URL'])
    
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
            
            # finding the film name
            panel = film.find('div').find('img')
            film_name = panel['alt']
            
            # try to find the rating of a film if possible and converting to float
            try:
                stars = film.find('span', class_='rating').get_text().strip()
                rating = transform_stars(stars)
            except:
                rating = np.nan
            
            # Obtaining release year, director, cast and average rating of the movie
            film_card = film.find('div').get('data-target-link')
            film_page = _domain + film_card
            filmget = requests.get(film_page)
            film_soup = BeautifulSoup(filmget.content, 'html.parser')
            
            release_year = film_soup.find('meta', attrs={'property':'og:title'}).attrs['content'][-5:-1]
            director = film_soup.find('meta', attrs={'name':'twitter:data1'}).attrs['content']
            
            # try to find the cast, if not found insert a nan
            try:
                cast = [ line.contents[0] for line in film_soup.find('div', attrs={'id':'tab-cast'}).find_all('a')]
            except:
                cast = np.nan
            
            # try to find average rating, if not insert a nan
            try:
                average_rating = float(film_soup.find('meta', attrs={'name':'twitter:data2'}).attrs['content'][:4])
            except:
                average_rating = np.nan

            film_rows.append([film_name, release_year, director, cast, rating, average_rating, _domain+film_card])
            
        # check if there is another page of ratings
        next_button = soup.find('a', class_='next')
        if next_button is None:
            break
        else:
            list_link = _domain + next_button['href']
            
    return film_rows

def transform_stars(starstring):
    """
    Transforms star rating into float value
    """
    stars = {
        "★": 1,
        "★★": 2,
        "★★★": 3,
        "★★★★": 4,
        "★★★★★": 5,
        "½": 0.5,
        "★½": 1.5,
        "★★½": 2.5,
        "★★★½": 3.5,
        "★★★★½": 4.5
    }
    try:
        return stars[starstring]
    except:
        return np.nan