from listscraper.scrape_functions import scrape_list
import listscraper.checkimport_functions as cef
import sys
import csv
import json
import os

class List:
    """
    Class that stores all data and user-specified options pertaining to a specific list that needs to be scraped.

    Attributes:
        list_url (str):                 The URL of the list that needs to be scraped.
        page_options (str):             The syntax describing which pages should be selected.
        output_name (str):              The specific output name of the file, optionally given by the user-input.
        global_output_name (str):       The output name set by the command line options. Revert to this if no specific output name was given.
        output_file_extension (str):    Type of file outputted.
        url_total (int):                Total amount of lists that have to be scraped.
        url_count (int):                The number of the current list.

    Methods:
        scrape():               Starts scraping the list from Letterboxd.
        write_to_file():        Writes the objects's films to a file.
        scrape_and_write():     Wrapper function to both scrape and write out to file.
    """
    
    def __init__(self, list_url, pagestring, output_name, global_output_name, output_file_extension, url_total, url_count, concat):
        """
        Constructs necessary attributes of the list object.

        Parameters:
            url (str):                      The URL of the list.
            pagestring (str):               Literal string syntax that was input.
            
            type (str):                     The list type of this object.
            username (str):                 The username of the list owner.
            listname (str):                 The list name from the URL.

            output_name (str):              The final output name of the file.
            output_file_extension (str):    Type of output file.
            page_options (list):            List of integers corresponding to all selected pages.
        """
        
        self.url = list_url
        self.pagestring = pagestring.strip("\'\"").replace(" ", "")
        self.output_file_extension = output_file_extension

        print(f"Checking inputs for URL {url_count}/{url_total}...")

        # URL input check
        urlcheck, self.type, self.username, self.listname = cef.checkimport_url(self.url)
        if not urlcheck:
            sys.exit(f"     {self.url} is not a valid list URL. Please try again!") 

        # (-on) output name check
        outputnamecheck, self.output_name = cef.checkimport_outputname(output_name, global_output_name, self.output_file_extension, self.listname, url_total, url_count, concat)
        if not outputnamecheck:
            sys.exit(f"    Incorrect output name(s) were given. Please check and try again.")       

        # (-p) pages syntax check
        pagecheck, self.page_options = cef.checkimport_pages(self.pagestring)
        if not pagecheck:
            sys.exit(f"    The input syntax of the pages (-p flag) was not correct. Please try again!")

        ## Summary of all properties before scraping starts
        print(f"    url:         {self.url}")
        print(f"    username:    {self.username}")
        print(f"    type:        {self.type}")
        print(f"    page_select: {self.pagestring}")
        print(f"    output_name: {self.output_name}\n")

    def scrape(self, quiet, concat):
        """
        Scrapes the Letterboxd list by using the List object's URL
        and stores information on each film in a new attribute.

        Attribute:
            films (list):   The list of films with all scraped information.
        """

        print(f"    Scraping {self.url}...")

        # If list is of generic LB site, URL should be slightly altered
        if self.type == "LBfilms":
            scrape_url = "films/ajax".join(self.url.split("films"))         # 'ajax' is inserted
        else:
            scrape_url = self.url

        self.films = scrape_list(scrape_url, self.page_options, self.output_file_extension, self.type, quiet, concat)

    def write_to_file(self, output_path):
        """
        Writes the films of the List object to a file.
        """

        if len(self.films) == 1:
            return print(f"        No films found to write out for list {self.listname}. Please try a different selection.")

        outpath = os.path.join(output_path, self.output_name)
        if self.output_file_extension == ".json":
            with open(outpath, "w", encoding="utf-8") as jsonf:
                jsonf.write(json.dumps(self.films, indent=4, ensure_ascii=False))
        else:
            header = list( self.films[0].keys() )
            with open(outpath, 'w', newline="", encoding = "utf-8") as f:
                write = csv.DictWriter(f, delimiter=",", fieldnames=header)
                write.writeheader()
                write.writerows(self.films)
    
        return print(f"    Written to {self.output_name}!")
    

    def scrape_and_write(self, output_path, quiet, concat):
        """
        Function to initiate scraping from URL and writing to file of the LB list.
        """

        self.scrape(quiet, concat)
        self.write_to_file(output_path)