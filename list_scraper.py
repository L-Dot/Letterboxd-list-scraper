from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import numpy as np
import re

_domain = 'https://letterboxd.com/'

def scrape_list(list_link):
    """
    Takes in a Letterboxd link and outputs a list of film title, release year, 
    director, cast, average rating and letterboxd url
    """
    
    film_rows = []
    film_rows.append(['Film_title', 'Release_year', 'Director', 'Genres', 'Personal_rating', 'Average_rating', 'Runtime', "Watches", "Likes" 'Cast', 'Letterboxd URL'])

    while True:
        list_page = requests.get(list_link)
        
        # check to see page was downloaded correctly
        if list_page.status_code != 200:
            return print("Error: Could not load page")

        soup = BeautifulSoup(list_page.content, 'lxml')
        
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
                
                # remove all the 'Show All...' tags if they are present
                cast = [i for i in cast if i != 'Show All…']
            
            except:
                cast = np.nan
            
            # try to find average rating, if not insert a nan
            try:
                average_rating = float(film_soup.find('meta', attrs={'name':'twitter:data2'}).attrs['content'][:4])
            except:
                average_rating = np.nan

            # Scrape movie genres
            genres = film_soup.find('div', {'class': 'text-sluglist capitalize'})
            genres = [genres.text for genres in genres.find_all('a', {'class': 'text-slug'})]

            # Get movie runtime by searching for first sequence of digits in the p element with the runtime
            runtime = int(re.search(r'\d+', film_soup.find('p', {'class': 'text-link text-footer'}).text).group())

            # In order to get stats on how many people watched/liked the movie, need to use new link

            # This grabs the name of the movie as it appears in the url
            movie = film_page.split('/')[-2]
            # This goes to the page with the desired stats for the movie
            r = requests.get(f'https://letterboxd.com/esi/film/{movie}//stats/')
            stats_soup = BeautifulSoup(r.content, 'lxml')

            # Get number of people that have watched the movie
            # Grab the full "Watched by X members" string
            watches = stats_soup.find('a', {'class': 'has-icon icon-watched icon-16 tooltip'})["title"]
            # Filters above message to only grab the number portion
            watches = re.findall(r'\d+', watches)
            # Numbers are separated by the comma, join them back together to get actual count
            watches = int(''.join(watches))

            # Get number of people that have liked the movie
            # Grab the full "Liked by X members" string
            likes = stats_soup.find('a', {'class': 'has-icon icon-like icon-liked icon-16 tooltip'})["title"]
            # Filters above message to only grab the number portion
            likes = re.findall(r'\d+', likes)
            # Numbers are separated by the comma, join them back together to get actual count
            likes = int(''.join(likes))

            film_rows.append([film_name, release_year, director, genres, rating, average_rating, runtime, watches, likes, cast, film_page])
            
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