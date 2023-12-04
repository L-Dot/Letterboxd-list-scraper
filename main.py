import csv
from list_scraper import scrape_list

'''
Letterboxd List scraper - main program
'''

HELLO_STRING = \
"""
====================================================\r
Welcome to the Letterboxd List scraper!\r
Provided with an URL, this program outputs a CSV file'\r
of movie title, release data and Letterboxd link.'\r
Example url: https://letterboxd.com/.../list/short-films/).\r
The program currently only supports lists and watchlists.\r
Enter q or quit to exit the program.\r
====================================================\r
"""

class MovieList(list):
    """
    List to store data pertaining to a specific list
    """
    
    def __init__(self, list_name, link):
        """
        :param list_name: List name for data file (if applicable):
        :param link: The link of the list
        """
        
        self.name = list_name
        self.link = link
        self.films = []

def main():

    print(f'{HELLO_STRING}')

    # Checking if URL is of a watchlist or of a list
    list_url = input('Enter the URL of the list you wish to scrape:')
    # exit option
    if list_url == 'q' or list_url == 'quit':
        exit()
        
    # if a watchlist proceed this way
    elif list_url.split('/')[-2] == 'watchlist':
        try:
            list_name = list_url.split('/')[-2]
            username = list_url.split('/')[-3]
            print("\nScraping list data...\n")
            current_list = MovieList(list_name, list_url)
            current_list.films = scrape_list(current_list.link)
        except:
            print('That is not a valid list URL, please try again.')
    
    # if a list proceed this way
    elif list_url.split('/')[-3] == 'list':
        try:
            list_name = list_url.split('/')[-2]
            list_url = list_url + '/detail/'            # Adding detail to URL access the personal rating later
            print("\nScraping list data...\n")
            current_list = MovieList(list_name, list_url)
            current_list.films = scrape_list(current_list.link)
        except:
            print('That is not a valid list URL, please try again.')

    # writing to a CSV file
    try:
        csv_name = username + '_' + list_name
        print(f'Writing to {csv_name}.csv.')
        list_to_csv(current_list.films, csv_name)
          
    except:
        print(f'Writing to {list_name}.csv.')
        list_to_csv(current_list.films, list_name)
    
    print('Done!')

def list_to_csv(film_rows, list_name):
    """
    Takes in a list of filmrows outputted by the list_scraper()
    and converts it to a CSV file
    
    """
    
    with open(f'{list_name}.csv', 'w', newline="", encoding = "utf-8") as f:
        write = csv.writer(f, delimiter=",")
        write.writerows(film_rows)
    return

if __name__ == "__main__":
    main()
