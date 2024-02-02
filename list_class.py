from list_scraper import *
import check_and_extract_functions as cef
import sys
import csv
import os

class List:
    """
    Class that stores all data and user-specified options pertaining to a specific list that needs to be scraped.

    Attributes:
        list_url (str):             The URL of the list that needs to be scraped.
        page_options (str):         The syntax describing which pages should be selected.
        output_name (str):          The specific output name of the CSV file, optionally given by the user-input.
        global_output_name (str):   The output name set by the command line options. Revert to this if no specific output name was given.
        url_total (int):            Total amount of lists that have to be scraped.
        url_count (int):            The number of the current list.

    Methods:
        scrape():   Starts scraping the list from Letterboxd.
    """
    
    def __init__(self, list_url, pagestring, output_name, global_output_name, url_total, url_count):
        """
        Constructs necessary attributes of the list object.

        Parameters:
            url (str):              The URL of the list.
            pagestring (str):       Literal string syntax that was input.
            
            type (str):             The list type of this object.
            username (str):         The username of the list owner.
            listname (str):         The list name from the URL.

            output_name (str):      The final output name of the CSV.
            page_options (list):    List of integers corresponding to all selected pages.
        """
        
        self.url = list_url
        self.pagestring = pagestring.strip("\'\"").replace(" ", "")

        print(f"Checking inputs for URL {url_count}/{url_total}...")

        # URL input check
        urlcheck, self.type, self.username, self.listname = cef.checkextract_url(self.url)
        if not urlcheck:
            sys.exit(f"     {self.url} is not a valid list URL. Please try again!")

        # (-on) output name check
        outputnamecheck, self.output_name = cef.checkextract_outputname(output_name, global_output_name, self.listname, url_total, url_count)
        if not outputnamecheck:
            sys.exit(f"    Incorrect output name(s) were given. Please check and try again.")       

        # (-p) pages syntax check
        pagecheck, self.page_options = cef.checkextract_pages(self.pagestring)
        if not pagecheck:
            sys.exit(f"    The input syntax of the pages (-p flag) was not correct. Please try again!")
            
        # (-vo) input check

        ## Summary of all properties before scraping starts
        print(f"    url:         {self.url}")
        print(f"    username:    {self.username}")
        print(f"    type:        {self.type}")
        print(f"    page_select: {self.pagestring}")
        print(f"    output_name: {self.output_name}\n")


    def scrape(self, verbose_off):

        print(f"    Scraping {self.url}...")
        self.films = scrape_list(self.url, self.page_options, verbose_off)

        return

    def write_to_csv(self, output_path):

        # create dir if necessary
        os.makedirs(output_path, exist_ok=True)
        outpath = os.path.join(output_path, self.output_name)

        with open(outpath, 'w', newline="", encoding = "utf-8") as f:
            write = csv.writer(f, delimiter=",")
            write.writerows(self.films)
        
        return print(f"    Written to {self.output_name}!")
    

    def scrape_and_write(self, output_path, verbose_off):

        self.scrape(verbose_off)
        self.write_to_csv(output_path)