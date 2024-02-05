from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import numpy as np
import re

_domain = 'https://letterboxd.com/'

def scrape_list(list_link, page_options, verbose_off=False, concat=False):
    """
    Scrapes a Letterboxd list. Takes into account any page flags.

    Parameters:
        list_link (str):         The URL link of the first page of the LB list.
        page_options (str/list): Either a "*" to scrape all pages, or a list with specific page integers.
        verbose_off (bool):      Option to turn-off tqdm (not much increased speed noticed. Default is off.)
        concat (bool):           If set true it will add an extra column with the original list name to the scraped data.

    Returns:
        film_rows (list):        A list of lists where each row contains information on the films in the LB list.
    """

    film_rows = []
    if not concat:
        film_rows.append(['Film_title', 'Release_year', 'Director', 'Genres', 'Owner_rating', 'Average_rating', 'Runtime', 
                        'Watches', 'List_Appearances', 'Likes', 'Countries', 'Original_Language', 'Spoken_Languages', 
                        'Cast', 'Studios', 'Film_URL'])
    elif concat:
        film_rows.append(['Film_title', 'Release_year', 'Director', 'Genres', 'Owner_rating', 'Average_rating', 'Runtime', 
                'Watches', 'List_Appearances', 'Likes', 'Countries', 'Original_Language', 'Spoken_Languages', 
                'Cast', 'Studios', 'Film_URL', 'List_URL'])

    if (page_options == []) or (page_options == "*"):
        while True:
            film_rows_page, soup = scrape_page(list_link, verbose_off, concat)
            film_rows.extend(film_rows_page)

            # check if there is another page of ratings and continue if yes
            next_button = soup.find('a', class_='next')
            if next_button is None:
                break
            else:
                list_link = _domain + next_button['href']
    
    else:
        for p in page_options:
            new_link = list_link + f"page/{p}/"
            
            try:
                film_rows_page, soup = scrape_page(new_link, verbose_off, concat)
                film_rows.extend(film_rows_page)
            except:
                print(f"        No films on page {p}...")
                continue

    return film_rows

def scrape_page(list_link, verbose_off=False, concat=False):
    """
    Scrapes the page of a LB list URL, finds all its films and iterates over each film URL
    to find the relevant information.

    Parameters:
        list_link (str):        Link of the LB page that should be scraped.
        verbose_off (bool):     Option to turn-off tqdm.
        concat (bool):          Checks if concat is enabled.

    Returns:
        film_rows_page (list):  List of lists containing information on each film on the LB page.
        soup (str):             The HTML string of the entire LB page.
    """
    
    film_rows_page = []
    list_page = requests.get(list_link)
    
    # check to see page was downloaded correctly
    if list_page.status_code != 200:
        return print("Error: Could not load page.")

    soup = BeautifulSoup(list_page.content, 'lxml')

    # grab the main film grid
    table = soup.find('ul', class_='poster-list')
    if table is None:
        return

    films = table.find_all('li')
    if films == []:
        return 

    # iterate through films
    for film in films if verbose_off else tqdm(films):
        
        # finding the film name
        panel = film.find('div').find('img')
        film_name = panel['alt']
        
        # try to find the list owner's rating of a film if possible and converting to float
        try:
            stringval = film.attrs['data-owner-rating']
            owner_rating = int(stringval)/2
        except:
            owner_rating = np.nan
        
        # Obtaining release year, director, cast and average rating of the movie
        film_card = film.find('div').get('data-target-link')[1:]
        film_page = _domain + film_card
        filmget = requests.get(film_page)
        film_soup = BeautifulSoup(filmget.content, 'html.parser')
        
        # Try to find release year, if missing insert nan
        release_year = int(str(film_soup.find_all("script")).split("releaseYear: ")[1].split(",")[0].strip("\""))
        if release_year == 0:
            release_year = np.nan
        
        # Try to find director, if missing insert nan
        director = film_soup.find('meta', attrs={'name':'twitter:data1'}).attrs['content']
        if director == "":
            director = np.nan
        
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
            if countries == []:
                countries = np.nan
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
            if studios == []:
                studios = np.nan
        except:
            studios = np.nan

        # Getting number of watches, appearances in lists and number of likes (requires new link) ## 
        movie = film_page.split('/')[-2]                                        # Movie title in URL
        r = requests.get(f'https://letterboxd.com/csi/film/{movie}/stats/')    # Stats page of said movie
        stats_soup = BeautifulSoup(r.content, 'lxml')

        # Get number of people that have watched the movie
        watches = stats_soup.find('a', {'class': 'has-icon icon-watched icon-16 tooltip'})["title"]
        watches = re.findall(r'\d+', watches)    # Find the number from string
        watches = int(''.join(watches))          # Filter out commas from large numbers

        # Get number of film appearances in lists
        list_appearances = stats_soup.find('a', {'class': 'has-icon icon-list icon-16 tooltip'})["title"]
        list_appearances = re.findall(r'\d+', list_appearances) 
        list_appearances = int(''.join(list_appearances))

        # Get number of people that have liked the movie
        likes = stats_soup.find('a', {'class': 'has-icon icon-like icon-liked icon-16 tooltip'})["title"]
        likes = re.findall(r'\d+', likes)
        likes = int(''.join(likes))

        # Getting info on rating histogram (requires new link)
        r = requests.get(f'https://letterboxd.com/csi/film/{movie}/rating-histogram/')    # Rating histogram page of said movie
        stats_soup = BeautifulSoup(r.content, 'lxml')

        watches = stats_soup.find('a', {'class': 'has-icon icon-watched icon-16 tooltip'})["title"]
        watches = re.findall(r'\d+', watches)    # Find the number from string
        watches = int(''.join(watches))          # Filter out commas from large numbers





        if not concat:
            film_rows_page.append([film_name, release_year, director, genres, owner_rating, average_rating, runtime, 
                    watches, list_appearances, likes, countries, og_language, languages, cast, studios, film_page])
        elif concat:
            film_rows_page.append([film_name, release_year, director, genres, owner_rating, average_rating, runtime, 
                    watches, list_appearances, likes, countries, og_language, languages, cast, studios, film_page, list_link])
 
        
    return film_rows_page, soup

def transform_stars(starstring):
    """
    Transforms star rating into float value.
        
        Parameters:
            starstring (str):   A string of star symbols.
        
        Returns:
            val (float):        The corresponding numeric value from 0-5.
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
        val = stars[starstring]
        return val
    except:
        return np.nan