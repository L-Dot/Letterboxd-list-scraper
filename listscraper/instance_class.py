from listscraper.list_class import List
import listscraper.checkimport_functions as cef
import concurrent.futures # for pool of threads
import time
import sys
import os
import csv
import json

class ScrapeInstance:
    """
    Initializes the program instance of the Letterboxd-list-scraper.
    All attributes are read and saved as variables from the 'argparse' flags of the command line, or from the provided .txt file.

    Attributes:
        inputURLs (list):               A list of URLs input from the command line.
        pages (str):                    Page options read from optional '-p' flag. Default is all pages ('*').
        output_name (str):              Output name obtained from optional '-on' flag. Default is list name from URL.
        output_path (str):              Output path obtained from optional '-op' flag. Default is 'scraper_outputs' directory.
        output_file_extension (str):    Type of file outputted. Default is CSV, ".csv".
        infile (str):                   Name of input .txt file obtained from optional '-f' flag.
        concat (bool):                  Option to turn on list concatenation read from optional '--concat' flag. Default is False.
        quiet(bool):                    Turn off tqdm loading bars read from optional '-vo' flag. Default is False.
        threads (int):                  Amount of threads used for scraping read from optional '--threads' flag. Default is 4. 

    Methods:
        import_from_infile(infile):
            Imports the list URLs and their options from the .txt file into List objects.
        import_from_commandline(inputURLs):
            Imports the list URLs and their options from the command line into List objects.
        concatenate_lists():
            Concatenates all the films in the List objects into one big list.
        scrape_all_and_writeout(listobjs, maxworkers=4):
            Scrapes all the films from the List objects using their LB link.
    """

    def __init__(self, inputURLs, pages, output_name, output_path, output_file_extension, infile, concat, quiet, threads):
        """
        Initializes the program by running various checks if input values and syntax were correct.

        (new) Attributes:

            global_page_options(str):   The page selection options that will be used if no '-p' input was given.
            global_output_name (str):   The output name that will be used if no '-on' input was given.

            Nthreads (int):             The amount of worker threads that should be used for scraping.
            starttime(time.obj):        Time at the start of the program.
            lists_to_scrape (list):     Collection of all imported List objects that should be scraped.
            endtime (time.obj):         Time at the end of the program.
        """

        self.inputURLs  = inputURLs
        self.global_page_options = pages
        self.global_output_name = output_name
        self.output_path = output_path
        self.infile = infile
        self.concat = concat
        self.quiet = quiet

        output_file_extension_check, self.output_file_extension = cef.checkimport_output_output_file_extension(output_file_extension)
        if not output_file_extension_check:
            sys.exit(f"    Incorrect output file extension was given. Please check and try again.")  
        
        self.Nthreads = threads
        self.starttime = time.time()

        self.lists_to_scrape = []

        if self.infile:
            infilename = self.infile.name
        else:
            infilename = None

        print(f"        infile:         {infilename}")
        print(f"        output_path:    {self.output_path}")
        print(f"        concat:         {self.concat}")
        print(f"        threads:        {self.Nthreads}")
        print(f"        verbose:        {not self.quiet}")
        print("=============================================\n")

        # Checks if only .txt or only command line URL were given
        if self.infile and self.inputURLs:
            sys.exit("Please provide either a .txt file with -f OR a valid list URL.")

        # Checks for an input file and saves any URLs to List instances
        elif self.infile:
            self.import_from_infile(self.infile)

        # Checks for input URLs and saves them to List instances
        elif self.inputURLs:
            self.import_from_commandline(self.inputURLs)

        # No scrapable URLs were found...
        else:
            sys.exit("No scrapable URLs were provided! Please type 'python main.py --help' for more information")

        print("Initialization successful!\n")

        #=== Scraping and writing to file ===#

        # Create output dir if necessary
        os.makedirs(self.output_path, exist_ok=True)
        self.scrape_all_and_writeout(self.lists_to_scrape, self.Nthreads)

        self.endtime = time.time()


    def import_from_infile(self, infile):
        """
        Imports the lines from a .txt file into List objects. 
        Each line can contain specific list URLs and option flags (-p or -on) referring to that list.
        Lines starting with a "#" will be skipped.

        Parameters:
            infile (str): The file name of the input .txt.
        """
        
        lines = infile.read().split("\n")

        # Filtering out comments (#) and empty lines
        final_lines = []
        for line in lines:
            if line.startswith("#") or not line.strip():
                continue
            else:
                final_lines.append(line)

        self.url_total = len(final_lines)
        self.url_count = 1

        print(f"A total of {self.url_total} URLs were read-in from {self.infile.name}!\n")

        for line in final_lines:
            chunks = line.split(' ')
            url = [i for i in chunks if ("https://") in i][0]

            # Check for page option on this line
            if ("-p" in chunks): 
                page_options = chunks[chunks.index("-p") + 1]
            elif ("--pages" in chunks):
                page_options = chunks[chunks.index("--pages") + 1]
            else:
                page_options = self.global_page_options

            # Check for output name option on this line
            if ("-on" in chunks): 
                output_name = chunks[chunks.index("-on") + 1]
            elif ("--output_name" in chunks):
                output_name = chunks[chunks.index("--output_name") + 1]
            else:
                output_name = self.global_output_name

            self.lists_to_scrape.append(List(url, page_options, output_name, self.global_output_name, self.output_file_extension, 
                                             self.url_total, self.url_count, self.concat))
            self.url_count += 1

    def import_from_commandline(self, inputURLs):
        """
        Checks if there are URLs on the command line and individually imports them into List objects.

        Parameters:
            inputURLs (list):   List of strings of all list URLs on the command line.
        """

        self.url_total = len(inputURLs)
        self.url_count = 1

        print(f"A total of {self.url_total} URLs were found!\n")

        for url in inputURLs:
            self.lists_to_scrape.append(List(url, self.global_page_options, self.global_output_name, self.global_output_name, self.output_file_extension, 
                                             self.url_total, self.url_count, self.concat))
            self.url_count += 1

    def concatenate_lists(self):
        """
        Concatenates all the films in the scraped List objects together. 
        """

        self.concat_lists = []
        for i, list in enumerate(self.lists_to_scrape):
            if i == 0:
                self.concat_lists.extend(list.films)
            else:
                self.concat_lists.extend(list.films[1:])

    def scrape_all_and_writeout(self, list_objs, max_workers=4):
        """
        Starts the scraping of all lists from Letterboxd and subsequently writes out to file(s).

            Parameters:
                target_lists (list):   The collection of List objects that have to be scraped.
                max_workers (int):     The max amount of threads to generate (default = 4).
        """
        print(f"Starting the scraping process with {max_workers} available threads...\n")

        # Writes out when each list has been scraped
        if self.concat == False:

            with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
                _ = [executor.submit(listobj.scrape_and_write, self.output_path, self.quiet, self.concat) for listobj in list_objs]

        # Waits for all lists to finish before writing out
        elif self.concat == True:
            
            with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
                _ = [executor.submit(listobj.scrape, self.quiet, self.concat) for listobj in list_objs]

            self.concatenate_lists()
            
            # Checks if manual name for concatenated file was given, and otherwise uses a default
            if self.global_output_name == None:
                self.global_output_name = "concatenated_lists"

            # Write out to path
            outpath = os.path.join(self.output_path, self.global_output_name + self.output_file_extension)
            if self.output_file_extension == ".json":
                with open(outpath, "w", encoding="utf-8") as jsonf:
                    jsonf.write(json.dumps(self.concat_lists, indent=4, ensure_ascii=False))
            else:
                header = list( self.concat_lists[0].keys() )
                with open(outpath, 'w', newline="", encoding = "utf-8") as f:
                    write = csv.DictWriter(f, delimiter=",", fieldnames=header)
                    write.writeheader()
                    write.writerows(self.concat_lists)
            
            return print(f"    Written concatenated lists to {self.global_output_name}{self.output_file_extension}!")
