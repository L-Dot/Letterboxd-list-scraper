from list_class import List
from csv_writer import *
import concurrent.futures # for pool of threads
import os.path # for checking if file exists
import argparse
import time
import sys

out_dir = "ScrapedCSVs/"
max_workers = 4

'''
Letterboxd List scraper - main program
'''

class LBlistscraper:

    def __init__(self, inputURLs, pages, output_name, output_path, infile, concat, verbose_off, threads):

        self.inputURLs  = inputURLs
        self.global_page_options = pages
        self.global_output_name = output_name
        self.output_path = output_path
        self.infile = infile
        self.concat = concat
        self.verbose_off = verbose_off
        
        self.Nthreads = threads
        self.starttime = time.time()

        self.lists_to_scrape = []

        print(f"        infile:         {self.infile.name}")
        print(f"        output_path:    {self.output_path}")
        print(f"        concat:         {self.concat}")
        print(f"        threads:        {self.Nthreads}")
        print(f"        verbose:        {not self.verbose_off}")
        print("=============================================\n")

        # Checks if only .txt or only command line URL were given
        if self.infile and self.inputURLs:
            sys.exit("Please provide either a .txt file with -f OR a valid list URL.")

        # Checks for an input file and saves any URLs to List instances
        elif self.infile:
            self.infile = self.infile
            self.import_from_infile(self.infile)

        # Checks for input URLs and saves them to List instances
        elif self.inputURLs:
            self.import_from_commandline(self.inputURLs)

        # No scrapable URLs were found...
        else:
            sys.exit("No scrapable URLs were provided! Please type 'python main.py --help' for more information")

        print("Initialization successful!\n")

        #=== Scraping ===#
        self.start_scraping(self.lists_to_scrape, self.Nthreads)


    def import_from_infile(self, infile):
        lines = infile.read().split("\n")

        # Filtering out comments (#)
        final_lines = []
        for line in lines:
            if line.startswith("#"):
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

            self.lists_to_scrape.append(List(url, page_options, output_name, self.global_output_name, self.url_total, self.url_count))
            self.url_count += 1

    def import_from_commandline(self, inputURLs):

        self.url_total = len(inputURLs)
        self.url_count = 1

        print(f"A total of {self.url_total} URLs were found!\n")

        for url in inputURLs:
            self.lists_to_scrape.append(List(url, self.global_page_options, self.global_output_name, self.global_output_name, self.url_total, self.url_count))
            self.url_count += 1

    def start_scraping(self, list_objs, max_workers=4):
        """
        Starts the scraping of all lists from Letterboxd.

            Parameters:
                target_lists (list):   The collection of List objects that have to be scraped.
                max_workers (int):     The max amount of threads to generate (default = 4).
        """
        print(f"Starting the scraping process with {max_workers} available threads...\n")

        # if --concat = False:
        #   scrape_and_write()
        #       scrape()
        #       write()
        # else:
        #   scrape()
        #   concat_write()
        #       concat()
        #       write()

        # Writes out when each list has been scraped
        if self.concat == False:

            with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
                futures = [executor.submit(listobj.scrape_and_write, self.output_path, self.verbose_off) for listobj in list_objs]

        # Waits for all lists to finish before writing out
        elif self.concat == True:
            
            with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
                futures = [executor.submit(listobj.scrape, self.verbose_off) for listobj in list_objs]

            # self.concat
            # self.write
        
        print(f"\nProgram successfully finished! Your CSV(s) can be found in {self.output_path}.")
        print(f"    Total run time was {time.time() - self.starttime :.2f} seconds.")
                


        # for list_obj in list_objs:

        #     thread = pool.submit(list_obj.scrape, self.verbose_off) 

        #     while thread.running():
        #         print("still running...")
        #         time.sleep(2)
            # pool.submit(list_obj.write_to_csv) 

            # start writing to CSV only if not being concatenated at the end
            # print(list_obj.films)
            # if self.concat == False:
            #     self.write_out(list_obj, self.concat)

        

        # if self.concat == True:
        #     self.write_out(list_obj, self.concat)

    # def write_out(list_obj, concat=False):

    #     with open(f'{list_obj.output_name}.csv', 'w', newline="", encoding = "utf-8") as f:
    #             write = csv.writer(f, delimiter=",")
    #             write.writerows(list_obj.films)
        
    #     return
        
    












def main(inputURLs, global_pages, global_output_names, global_output_path, infile, concat, verbose_off):


    print("=============================================")
    print("           Letterboxd-List-Scraper           ")
    print("=============================================\n")
    
    print(inputURLs)

    # # Checks if an input .txt file is given and if yes, imports the URLs and their options into List classes
    # if infile != None:
    #     print(f"The infile {infile[0].name} was found!\n")
        
    #     import_infile(infile[0], global_pages, global_output_names)

    #     # Append URLs from file to any inputURLs given
    #     inputURLs.extend(infile[0].read().split("\n"))

    # elif inputURLs:
    #     # Check how much URLs are given and create a List class instance for each one 
    #     N_URLs = len(inputURLs)
    #     print(f"A total of {N_URLs} list URLs were found.")

    #     URL_list = []
    #     for url in inputURLs:
    #         URL_list.append(List(url, global_pages, global_output_names))






    # Apply options and scrape



#     target_lists = list()
#     if os.path.isfile("target_lists.txt"):
#         print('====================================================')
#         print('Welcome to the Letterboxd List scraper!')
#         print('Scraping the lists specified in target_lists.txt,') 
#         print('(letterboxd_url,filename), filename is optional!)') 
#         print('Example url: https://letterboxd.com/.../list/short-films/).')
#         print('The program currently only supports lists and watchlists.')
#         print('====================================================\n')
#         with open(f"target_lists.txt",'r') as f:
#             reader = csv.reader(f)
#             for row in reader:
#                 if len(row) >1:
#                     target_lists.append((row[0],row[1]))
#                 else:
#                     target_lists.append((row[0],None))
#     else:
#         print('====================================================')
#         print('Welcome to the Letterboxd List scraper!')
#         print('Provided with an URL, this program outputs a CSV file') 
#         print('of movie title, release data and Letterboxd link.') 
#         print('Example url: https://letterboxd.com/.../list/short-films/).')
#         print('The program currently only supports lists and watchlists.')
#         print('Enter q or quit to exit the program.')
#         print('====================================================\n')

#         list_url=input('Enter the URL of the list you wish to scrape:')
#         target_lists.append(((list_url),None))

#         # exit option
#         if list_url == 'q' or list_url == 'quit':
#             exit()

#     pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
#     for target in target_lists:
#         pool.submit(collect_lists,target[0],target[1]) 
#     pool.shutdown(wait=True)





# def collect_lists(list_url, passed_name=None):
    
#     # Checking if URL is of a watchlist or of a list
#     while True:

#         # if a watchlist proceed this way
#         if list_url.split('/')[-2] == 'watchlist':
#             try:
#                 list_name = list_url.split('/')[-2]
#                 username = list_url.split('/')[-3]
#                 current_list = List(list_name, list_url)
#                 break

#             except:
#                 print('That is not a valid list URL, please try again.')
#                 continue
        
#         # if a list proceed this way
#         elif list_url.split('/')[-3] == 'list':
#             try:
#                 list_name = list_url.split('/')[-2]
#                 list_url = list_url + '/detail/'            # Adding detail to URL access the personal rating later
#                 current_list = List(list_name, list_url)
#                 break

#             except:
#                 print('That is not a valid list URL, please try again.')
#                 continue
    
#     # writing to a CSV file
#     try:
#         if passed_name != None:
#             csv_path = out_dir + passed_name
#         else:
#             csv_path = out_dir + username + '_' + list_name
#         print(f'Writing to {csv_path}.csv')
#         list_to_csv(current_list.films, csv_path)
          
#     except:
#         if passed_name != None:
#             csv_path = out_dir + passed_name
#         else:
#             csv_path = out_dir + list_name
#         print(f'Writing to {csv_path}.csv')
#         list_to_csv(current_list.films, csv_path)
    
#     print('All Done!')

if __name__ == "__main__":

    parser=argparse.ArgumentParser(prog="main", usage="%(prog)s [options] list-url",
                                   description="A Python program that scrapes Letterboxd lists and outputs the information on all of its films in a CSV file. Input form and desired outputs are user customizable. Concurrent scraping of multiple lists is supported.",
                                   epilog="Thank you for using the scraper! If you have any trouble and/or suggestions please contact me via the GitHub page https://github.com/L-Dot/Letterboxd-list-scraper.",
                                   formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version='%(prog)s 2.0.0')

    ## arguments / flags
    parser.add_argument("-vo","--verbose-off",help="Turn off verbose, stops describing everything the program does and no longer displays tqdm() progression bars.\
                        From testing this does not significantly increase program runtime, meaning verbose is turned on by default.",required=False,action="store_true")
    
    parser.add_argument("-p","--pages", type=str,
                        help=("only scrape selected pages from a URL. Default is to scrape all pages.\n"
                              "Page selection syntax follows these rules:\n"
                              "\t -p 1 \t\t page 1 (first page)\n"
                              "\t -p 1,3,5 \t pages 1,3,5\n"
                              "\t -p 1~3 \t pages 1,2,3\n"
                              "\t -p 1~3,5 \t pages 1,2,3 and 5\n"
                              "\t -p '<3,5' \t pages 1,2,3 and 5\n"
                              "\t -p '*' \t\t all pages (default)\n"
                              "The string should contain NO spaces. Also note the requirement of quotation marks when using the less-than (<) or star (*) signs!"),
                        required=False, default="*")

    parser.add_argument("-on", "--output_name", type=str,
                        help=("set the filename of the output CSV(s). Default output is a CSV file with the same name as its respective list.\n"
                              "If multiple URLs are provided, each CSV will be the concatenation of the filename with an increasing number _1, _2, etc.\n"
                              "The original list name will be output in the CSV."), 
                        required=False, default=None)
    
    parser.add_argument("-op", "--output_path", type=str, 
                        help="set the path for the output CSV(s). Default output is a folder called 'scraper_outputs'.", 
                        required=False, default="scraper_outputs")
    
    parser.add_argument("-f", "--infile", type=argparse.FileType('r'),
                        help="provide a .txt file with all of the URLs that should be scraped. Each URL should be isolated on its own newline together with any specific option flags. \
                            This feature is especially handy when you need to scrape a large amount of lists and/or when you have specific option flags for each URL.\n\
                            When using an input file, make sure to not give the script any URLs on the command line!", 
                        required=False, default=None)

    parser.add_argument("--concat", type=bool,
                        help="option to output all the scraped lists into a single concatenated CSV. An extra column is added that specifies the original list URL.",
                        required=False, default=False)
    
    parser.add_argument("--threads", type=int,
                        help="option to tweak the number of CPU threads used. Increase this to speed up scraping of multiple lists simultaneously. Default value is 4.",
                        required=False, default=4)

    ## positionals
    parser.add_argument("listURL", type=str, nargs="*", 
                        help=("the Letterboxd URL of the list that should be scraped. Multiple URLs can be given, separated by a space. For example:\n\n"
                        "\t python %(prog)s.py <list-url_1>\n"
                        "\t python %(prog)s.py <list-url_1> <list-url_2> <list-url_3>"))

    args=parser.parse_args()

    
    # Start the program

    print("=============================================")
    print("           Letterboxd-List-Scraper           ")
    print("=============================================")

    LBscraper = LBlistscraper(args.listURL, args.pages, args.output_name, args.output_path, args.infile, args.concat, args.verbose_off, args.threads)
    
    # target_lists = LBscraper.lists_to_scrape
    # LBscraper.start_scraping(target_lists)
