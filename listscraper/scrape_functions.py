from listscraper.utility_functions import val2stars, stars2val
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import numpy as np
import re

_domain = 'https://letterboxd.com/'

def scrape_list(list_url, page_options, output_file_extension, list_type, quiet=False, concat=False):
    """
    Scrapes a Letterboxd list. Takes into account any optional page selection.

    Parameters:
        list_url (str):                 The URL link of the first page of the LB list.
        page_options (str/list):        Either a "*" to scrape all pages, or a list with specific page integers.
        output_file_extension (str):    Type of file extension, for usage in 'scrape_page()'.
        list_type (str):                Type of list to be scraped, for usage in 'scrape_page()'.
        quiet (bool):                   Option to turn-off tqdm (not much increased speed noticed. Default is off.)
        concat (bool):                  If set true it will add an extra column with the original list name to the scraped data.

    Returns:
        list_films (list):       A list of dicts where each dict contains information on the films in the LB list.
    """

    list_films = []

    # If all pages should be scraped, go through all available pages
    if (page_options == []) or (page_options == "*"):
        while True:
            page_films, page_soup = scrape_page(list_url, list_url, output_file_extension, list_type, quiet, concat)
            list_films.extend(page_films)

            # Check if there is another page of ratings and if yes, continue to that page
            next_button = page_soup.find('a', class_='next')
            if next_button is None:
                break
            else:
                list_url = _domain + next_button['href']
    
    # If page selection was input, only go to those pages
    else:
        for p in page_options:
            new_link = list_url + f"page/{p}/"
            try:
                page_films, page_soup = scrape_page(new_link, list_url, output_file_extension, list_type, quiet, concat)
                list_films.extend(page_films)
            except:
                print(f"        No films on page {p}...")
                continue    
    
    return list_films

def scrape_page(list_url, og_list_url, output_file_extension, list_type, quiet=False, concat=False):
    """
    Scrapes the page of a LB list URL, finds all its films and iterates over each film URL
    to find the relevant information.

    Parameters:
        list_url (str):                 Link of the LB page that should be scraped.
        og_list_url (str):              The original input list URL (without any "/page/" strings added)
        output_file_extension (str):    Type of file extension, specifies 'not_found' entry.
        list_type (str):                Type of list, different specifications for different types.
        quiet (bool):                   Option to turn-off tqdm.
        concat (bool):                  Checks if concat is enabled.

    Returns:
        page_films (list):      List of dicts containing information on each film on the LB page.
        page_soup (str):        The HTML string of the entire LB page.
    """
    
    page_films = []
    page_response = requests.get(list_url)
    
    # Check to see page was downloaded correctly
    if page_response.status_code != 200:
        return print("Error: Could not load page.")

    page_soup = BeautifulSoup(page_response.content, 'lxml')
    
    # Grab the main film grid
    if list_type == "Cast/Crew":
        table = page_soup.find("div", class_="poster-grid")
    else:
        table = page_soup.find('ul', class_='poster-list')
    if table is None:
        return
    
    films = table.find_all('li')
    if films == []:
        return 
    
    not_found = np.nan if output_file_extension == ".csv" else None
    
    # Iterate through films
    for film in films if quiet else tqdm(films):
        if list_type == "Cast/Crew" and "poster-container placeholder" in str(film):
            break  # less than four entries

        film_dict = scrape_film(film, not_found)
        
        # Adds an extra column with OG list URL
        if concat:
            film_dict["List_URL"] = og_list_url
        
        page_films.append(film_dict)

    return page_films, page_soup
        
def scrape_film(film_html, not_found):
    """
    Scrapes all available information regarding a film. 
    The function makes multiple request calls to relevant Letterboxd film URLs and gets their raw HTML code.
    Using manual text extraction, the wanted information is found and stored in a dictionary.
    
    Parameters:
        film_html (str):    The raw <li> HTML string of the film object obtained from the list page HTML.
        not_found (object): Either 'np.nan' if output is CSV or 'None' if output is JSON
    Returns:
        film_dict (dict):   A dictionary containing all the film's information.
    """
    
    film_dict = {}

    # Obtaining release year, director and average rating of the movie
    film_card = film_html.find('div').get('data-target-link')[1:]
    film_url = _domain + film_card
    filmget = requests.get(film_url)
    film_soup = BeautifulSoup(filmget.content, 'html.parser')

    # Finding the film name
    film_dict["Film_title"] = film_soup.find("div", {"class" : "col-17"}).find("h1").text
    
    # Try to find release year, if missing or 0 insert nan
    release_year = int(str(film_soup.find_all("script")).split("releaseYear: ")[1].split(",")[0].strip("\""))
    if release_year == 0:
        release_year = not_found
    film_dict["Release_year"] = release_year

    # Try to find director, if missing insert nan
    director = film_soup.find('meta', attrs={'name':'twitter:data1'}).attrs['content']
    if director == "":
        director = not_found
    film_dict["Director"] = director

    # Finding the cast, if not found insert a nan
    try:
        cast = [ line.contents[0] for line in film_soup.find('div', attrs={'id':'tab-cast'}).find_all('a')]

        # remove all the 'Show All...' tags if they are present
        film_dict["Cast"] = [i for i in cast if i != 'Show All…']
    except:
        film_dict["Cast"] = not_found

    # Finding average rating, if not found insert a nan
    try:
        film_dict["Average_rating"] = float(film_soup.find('meta', attrs={'name':'twitter:data2'}).attrs['content'][:4])
    except:
        film_dict["Average_rating"] = not_found

    # Try to find the list owner's rating of a film if possible and converting to float
    try:
        stringval = film_html.attrs['data-owner-rating']
        if stringval != '0':
            film_dict["Owner_rating"] = float(int(stringval)/2)
        else:
            film_dict["Owner_rating"] = not_found
    except:
        # Extra clause for type 'film' lists
        try:
            starval = film_html.find_all("span")[-1].text
            film_dict["Owner_rating"] = stars2val(starval, not_found)
        except:
            film_dict["Owner_rating"] = not_found
        
    # Finding film's genres, if not found insert nan
    try: 
        genres = film_soup.find('div', {'class': 'text-sluglist capitalize'})
        film_dict["Genres"] = [genres.text for genres in genres.find_all('a', {'class': 'text-slug'})]
    except:
        film_dict["Genres"] = not_found

    # Get movie runtime by searching for first sequence of digits in the p element with the runtime, if not found insert nan
    try: 
        film_dict["Runtime"] = int(re.search(r'\d+', film_soup.find('p', {'class': 'text-link text-footer'}).text).group())
    except:
        film_dict["Runtime"] = not_found

    # Finding countries
    try:
        film_dict["Countries"] = [ line.contents[0] for line in film_soup.find('div', attrs={'id':'tab-details'}).find_all('a', href=re.compile(r'country'))]
        if film_dict["Countries"] == []:
            film_dict["Countries"] = not_found
    except:
        film_dict["Countries"] = not_found

    # Finding spoken and original languages
    try:
        # Replace non-breaking spaces (\xa0) by a normal space 
        languages = [ line.contents[0].replace('\xa0', ' ') for line in film_soup.find('div', attrs={'id':'tab-details'}).find_all('a', href=re.compile(r'language'))]
        film_dict["Original_language"] = languages[0]                                      # original language (always first)
        film_dict["Spoken_languages"] = list(sorted(set(languages), key=languages.index))   # all unique spoken languages
    except:
        film_dict["Original_language"] = not_found
        film_dict["Spoken_languages"] = not_found

    # Finding the description, if not found insert a nan
    try:
        film_dict['Description'] = film_soup.find('meta', attrs={'name' : 'description'}).attrs['content']
    except:
        film_dict['Description'] = not_found

    # !! Currently not working with films that have a comma in their title
    # # Finding alternative titles
    # try:
    #     alternative_titles = film_soup.find('div', attrs={'id':'tab-details'}).find('div', class_="text-indentedlist").text.strip().split(", ")
    # except:
    #     alternative_titles = not_found

    # Finding studios
    try:
        film_dict["Studios"] = [ line.contents[0] for line in film_soup.find('div', attrs={'id':'tab-details'}).find_all('a', href=re.compile(r'studio'))]
        if film_dict["Studios"] == []:
            film_dict["Studios"] = not_found
    except:
        film_dict["Studios"] = not_found

    # Getting number of watches, appearances in lists and number of likes (requires new link) ## 
    movie = film_url.split('/')[-2]                                        # Movie title in URL
    r = requests.get(f'https://letterboxd.com/csi/film/{movie}/stats/')    # Stats page of said movie
    stats_soup = BeautifulSoup(r.content, 'lxml')

    # Get number of people that have watched the movie
    watches = stats_soup.find('a', {'class': 'has-icon icon-watched icon-16 tooltip'})["title"]
    watches = re.findall(r'\d+', watches)    # Find the number from string
    film_dict["Watches"] = int(''.join(watches))          # Filter out commas from large numbers

    # Get number of film appearances in lists
    list_appearances = stats_soup.find('a', {'class': 'has-icon icon-list icon-16 tooltip'})["title"]
    list_appearances = re.findall(r'\d+', list_appearances) 
    film_dict["List_appearances"] = int(''.join(list_appearances))

    # Get number of people that have liked the movie
    likes = stats_soup.find('a', {'class': 'has-icon icon-like icon-liked icon-16 tooltip'})["title"]
    likes = re.findall(r'\d+', likes)
    film_dict["Likes"] = int(''.join(likes))

    # Getting info on rating histogram (requires new link)
    r = requests.get(f'https://letterboxd.com/csi/film/{movie}/rating-histogram/')    # Rating histogram page of said movie
    hist_soup = BeautifulSoup(r.content, 'lxml')

    # Get number of fans. Amount is given in 'K' notation, so if relevant rounded off to full thousands
    try:
        fans = hist_soup.find('a', {'class': 'all-link more-link'}).text
        fans = re.findall(r'\d+.\d+K?|\d+K?', fans)[0]
        if "." and "K" in fans:
            fans = int(float(fans[:-1]) * 1000)
        elif "K" in fans:
            fans = int(fans[-1]) * 1000
        else:
            fans = int(fans)
    except:
        fans = 0
    film_dict["Fans"] = fans

    # Get rating histogram (i.e. how many star ratings were given) and total ratings (sum of rating histogram)
    ratings = hist_soup.find_all("li", {'class': 'rating-histogram-bar'})
    tot_ratings = 0
    if len(ratings) != 0:
        for i, r in enumerate(ratings):
            string = r.text.strip(" ")
            stars = val2stars((i+1)/2, not_found)
            if string == "":
                film_dict[f"{stars}"] = 0
            else:
                Nratings = re.findall(r'\d+', string)[:-1]
                Nratings = int(''.join(Nratings))
                film_dict[f"{stars}"] = Nratings
                tot_ratings += Nratings

    # If the film has not been released yet (i.e. no ratings)
    else:
        for i in range(10):
            stars = val2stars((i+1)/2, not_found)
            film_dict[f"{stars}"] = 0
            
    film_dict["Total_ratings"] = tot_ratings

    # Thumbnail URL?

    # Banner URL?
    
    # Save the film URL as an extra column
    film_dict["Film_URL"] = film_url
    
    return film_dict
