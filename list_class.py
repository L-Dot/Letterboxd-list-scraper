from list_scraper import *

'''''''''''''''''''''''''''''''''''''''''''''''''''''
user class to store data pertaining to user
'''''''''''''''''''''''''''''''''''''''''''''''''''''


class List:

    def __init__(self, list_name, link):
        """
        :param list_name: File name for data file (if applicable):
        :param link: Main user's username
        """
        
        self.name = list_name
        self.link = link
        print("\nScraping list data...\n")
        self.films = scrape_list(self.link)