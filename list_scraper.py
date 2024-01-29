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
    film_rows.append(['Film_title', 'Release_year', 'Director', 'Genres', 'Owner_rating', 'Average_rating', 'Runtime', 'Countries', 
                      'Original_Language', 'Spoken_Languages', 'Cast', 'Studios', 'Letterboxd URL'])

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
            
            # try to find the list owner's rating of a film if possible and converting to float
            try:
                stars = film.find('span', class_='rating').get_text().strip()
                owner_rating = transform_stars(stars)
            except:
                owner_rating = np.nan
            
            # Obtaining release year, director, cast and average rating of the movie
            film_card = film.find('div').get('data-target-link')[1:]
            film_page = _domain + film_card
            filmget = requests.get(film_page)
            film_soup = BeautifulSoup(filmget.content, 'html.parser')
            
            release_year = film_soup.find('meta', attrs={'property':'og:title'}).attrs['content'][-5:-1]
            director = film_soup.find('meta', attrs={'name':'twitter:data1'}).attrs['content']
            
            # Finding the cast, if not found insert a nan
            try:
                cast = [ line.contents[0] for line in film_soup.find('div', attrs={'id':'tab-cast'}).find_all('a')]
                
                # remove all the 'Show All...' tags if they are present
                cast = [i for i in cast if i != 'Show All…']
            except:
                cast = np.nan
            
            # Finding average rating, if not found insert a nan
            try:
                average_rating = float(film_soup.find('meta', attrs={'name':'twitter:data2'}).attrs['content'][:4])
            except:
                average_rating = np.nan

            # Finding film's genres, if not found insert nan
            try: 
                genres = film_soup.find('div', {'class': 'text-sluglist capitalize'})
                genres = [genres.text for genres in genres.find_all('a', {'class': 'text-slug'})]
            except:
                genres = np.nan

            # Get movie runtime by searching for first sequence of digits in the p element with the runtime, if not found insert nan
            try: 
                runtime = int(re.search(r'\d+', film_soup.find('p', {'class': 'text-link text-footer'}).text).group())
            except:
                runtime = np.nan

            # Finding countries
            try:
                countries = [ line.contents[0] for line in film_soup.find('div', attrs={'id':'tab-details'}).find_all('a', href=re.compile(r'country'))]
            except:
                countries = np.nan

            # Finding spoken and original languages
            try:
                # Replace non-breaking spaces (\xa0) by a normal space 
                languages = [ line.contents[0].replace('\xa0', ' ') for line in film_soup.find('div', attrs={'id':'tab-details'}).find_all('a', href=re.compile(r'language'))]
                og_language = languages[0]                                      # original language (always first)
                languages = list(sorted(set(languages), key=languages.index))   # all unique spoken languages
            except:
                languages = np.nan
                og_language = np.nan

            # !! Currently not working with films that have a comma in their title
            # # Finding alternative titles
            # try:
            #     alternative_titles = film_soup.find('div', attrs={'id':'tab-details'}).find('div', class_="text-indentedlist").text.strip().split(", ")
            # except:
            #     alternative_titles = np.nan

            # Finding studios
            try:
                studios = [ line.contents[0] for line in film_soup.find('div', attrs={'id':'tab-details'}).find_all('a', href=re.compile(r'studio'))]
            except:
                studios = np.nan

            # !! Currently not working since the stats page no longer exists
            ## Getting number of watches, appearances in lists and number of likes (requires new link) ## 
            # movie = film_page.split('/')[-2]                                        # Movie title in URL
            # r = requests.get(f'https://letterboxd.com/esi/film/{movie}//stats/')    # Stats page of said movie
            # stats_soup = BeautifulSoup(r.content, 'lxml')

            # # Get number of people that have watched the movie
            # watches = stats_soup.find('a', {'class': 'has-icon icon-watched icon-16 tooltip'})["title"]
            # watches = re.findall(r'\d+', watches)    # Find the number from string
            # watches = int(''.join(watches))          # Filter out commas from large numbers

            # # Get number of film appearances in lists
            # list_appearances = stats_soup.find('a', {'class': 'has-icon icon-list icon-16 tooltip'})["title"]
            # list_appearances = re.findall(r'\d+', list_appearances) 
            # list_appearances = int(''.join(list_appearances))

            # # Get number of people that have liked the movie
            # likes = stats_soup.find('a', {'class': 'has-icon icon-like icon-liked icon-16 tooltip'})["title"]
            # likes = re.findall(r'\d+', likes)
            # likes = int(''.join(likes))

            film_rows.append([film_name, release_year, director, genres, owner_rating, average_rating, runtime, countries, 
                              og_language, languages, cast, studios, film_page])
            
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
