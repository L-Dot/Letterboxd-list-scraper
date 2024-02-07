from listscraper.list_class import List
import concurrent.futures # for pool of threads
import time
import sys
import os
import csv

class ScrapeInstance:
    """
    Initializes the program instance of the Letterboxd-list-scraper.
    All attributes are read and saved as variables from the 'argparse' flags of the command line, or from the provided .txt file.

    Attributes:
        inputURLs (list):       A list of URLs input from the command line.
        pages (str):            Page options read from optional '-p' flag. Default is all pages ('*').
        output_name (str):      Output name obtained from optional '-on' flag. Default is list name from URL.
        output_path (str):      Output path obtained from optional '-op' flag. Default is 'scraper_outputs' directory.
        infile (str):           Name of input .txt file obtained from optional '-f' flag.
        concat (bool):          Option to turn on list concatenation read from optional '--concat' flag. Default is False.
        quiet(bool):      Turn off tqdm loading bars read from optional '-vo' flag. Default is False.
        threads (int):          Amount of threads used for scraping read from optional '--threads' flag. Default is 4. 

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

    def __init__(self, inputURLs, pages, output_name, output_path, infile, concat, quiet, threads):
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

        #=== Scraping and writing to CSV ===#

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

            self.lists_to_scrape.append(List(url, page_options, output_name, self.global_output_name,
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
            self.lists_to_scrape.append(List(url, self.global_page_options, self.global_output_name, self.global_output_name, 
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
        Starts the scraping of all lists from Letterboxd and subsequently writes out to CSV(s).

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
            
            # Checks if manual name for concatenated CSV was given, and otherwise uses a default
            if self.global_output_name == None:
                self.global_output_name = "concatenated_lists"

            # Write out to path
            header = list( self.concat_lists[0].keys() )
            outpath = os.path.join(self.output_path, self.global_output_name + ".csv")
            with open(outpath, 'w', newline="", encoding = "utf-8") as f:
                write = csv.DictWriter(f, delimiter=",", fieldnames=header)
                write.writeheader()
                write.writerows(self.concat_lists)
            
            return print(f"    Written concatenated lists to {self.global_output_name}.csv!")
        

# if __name__ == "__main__":

#     parser=argparse.ArgumentParser(prog="listscraper", usage="%(prog)s [options] [list-url]",
#                                    description="A Python program that scrapes Letterboxd lists and outputs the information on all of its films in a CSV file. Input form and desired outputs are user customizable. Concurrent scraping of multiple lists is supported.",
#                                    epilog="Thank you for using the scraper! If you have any trouble and/or suggestions please contact me via the GitHub page https://github.com/L-Dot/Letterboxd-list-scraper.",
#                                    formatter_class=argparse.RawTextHelpFormatter)
#     parser.add_argument('--version', action='version', version='%(prog)s 2.0.0')

#     ## arguments / flags
#     parser.add_argument("-on", "--output_name", type=str,
#                         help=("set the filename of the output CSV(s). Default output is a CSV file with the same name as its respective list.\n"
#                               "If multiple URLs are provided, each CSV will be the concatenation of the filename with an increasing number _1, _2, etc.\n"
#                               "The original list name will be output in the CSV."), 
#                         required=False, default=None)
    
#     parser.add_argument("-op", "--output_path", type=str, 
#                         help="set the path for the output CSV(s). Default output is a folder called 'scraper_outputs'.", 
#                         required=False, default="scraper_outputs")
    
#     parser.add_argument("-f", "--file", type=argparse.FileType('r'),
#                         help="provide a .txt file with all of the URLs that should be scraped. Each URL should be isolated on its own newline together with any specific option flags. \
#                             This feature is especially handy when you need to scrape a large amount of lists and/or when you have specific option flags for each URL.\n\
#                             When using an input file, make sure to not give the script any URLs on the command line!", 
#                         required=False, default=None)

#     parser.add_argument("-p","--pages", type=str,
#                         help=("only scrape selected pages from a URL. Default is to scrape all pages.\n"
#                               "Page selection syntax follows these rules:\n"
#                               "\t -p 1 \t\t page 1 (first page)\n"
#                               "\t -p 1,3,5 \t pages 1,3,5\n"
#                               "\t -p 1~3 \t pages 1,2,3\n"
#                               "\t -p 1~3,5 \t pages 1,2,3 and 5\n"
#                               "\t -p '<3,5' \t pages 1,2,3 and 5\n"
#                               "\t -p '*' \t\t all pages (default)\n"
#                               "The string should contain NO spaces. Also note the requirement of quotation marks when using the less-than (<) or star (*) signs!"),
#                         required=False, default="*")

#     # parser.add_argument("--more-stats", action=argparse.BooleanOptionalAction,
#     #                     help="option to enable extensive scraping, at the cost of a small increase in runtime. New data includes info on a film's rating histogram and fans.",
#     #                     required=False, default=False)

#     # parser.add_argument("--meta-data", action=argparse.BooleanOptionalAction,
#     #                     help="option to add a header row with some meta data to the CSV.",
#     #                     required=False, default=False)

#     parser.add_argument("--concat", action=argparse.BooleanOptionalAction,
#                         help="option to output all the scraped lists into a single concatenated CSV. An extra column is added that specifies the original list URL.",
#                         required=False, default=False)
    
#     parser.add_argument("--threads", type=int,
#                         help="option to tweak the number of CPU threads used. Increase this to speed up scraping of multiple lists simultaneously. Default value is 4.",
#                         required=False, default=4)

#     parser.add_argument("--verbose-off", action=argparse.BooleanOptionalAction,
#                         help="Turn off verbose, stops describing everything the program does and no longer displays tqdm() progression bars.\
#                         From testing this does not significantly increase program runtime, meaning verbose is turned on by default.",
#                         required=False,default=False)

#     ## positionals
#     parser.add_argument("listURL", type=str, nargs="*", 
#                         help=("the Letterboxd URL of the list that should be scraped. Multiple URLs can be given, separated by a space. For example:\n\n"
#                         "\t python %(prog)s.py <list-url_1>\n"
#                         "\t python %(prog)s.py <list-url_1> <list-url_2> <list-url_3>"))

#     args=parser.parse_args()


#     ## Starts the program

#     print("=============================================")
#     print("           Letterboxd-List-Scraper           ")
#     print("=============================================")

#     LBscraper = LBlistscraper(args.listURL, args.pages, args.output_name, args.output_path, args.file, args.concat, args.quiet, args.threads)

#     # Ends the program

#     print(f"\nProgram successfully finished! Your CSV(s) can be found in the ./{LBscraper.output_path}/.")
#     print(f"    Total run time was {LBscraper.endtime - LBscraper.starttime :.2f} seconds.")