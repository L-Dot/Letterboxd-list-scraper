from list_class import *
from csv_writer import *
import concurrent.futures # for pool of threads
import os.path # for checking if file exists
import argparse

out_dir = "ScrapedCSVs/"
max_workers = 4

'''
Letterboxd List scraper - main program
'''

def main():

    target_lists = list()
    if os.path.isfile("target_lists.txt"):
        print('====================================================')
        print('Welcome to the Letterboxd List scraper!')
        print('Scraping the lists specified in target_lists.txt,') 
        print('(letterboxd_url,filename), filename is optional!)') 
        print('Example url: https://letterboxd.com/.../list/short-films/).')
        print('The program currently only supports lists and watchlists.')
        print('====================================================\n')
        with open(f"target_lists.txt",'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >1:
                    target_lists.append((row[0],row[1]))
                else:
                    target_lists.append((row[0],None))
    else:
        print('====================================================')
        print('Welcome to the Letterboxd List scraper!')
        print('Provided with an URL, this program outputs a CSV file') 
        print('of movie title, release data and Letterboxd link.') 
        print('Example url: https://letterboxd.com/.../list/short-films/).')
        print('The program currently only supports lists and watchlists.')
        print('Enter q or quit to exit the program.')
        print('====================================================\n')

        list_url=input('Enter the URL of the list you wish to scrape:')
        target_lists.append(((list_url),None))

        # exit option
        if list_url == 'q' or list_url == 'quit':
            exit()

    pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    for target in target_lists:
        pool.submit(collect_lists,target[0],target[1]) 
    pool.shutdown(wait=True)





def collect_lists(list_url,passed_name=None):
    
    # Checking if URL is of a watchlist or of a list
    while True:

        # if a watchlist proceed this way
        if list_url.split('/')[-2] == 'watchlist':
            try:
                list_name = list_url.split('/')[-2]
                username = list_url.split('/')[-3]
                current_list = List(list_name, list_url)
                break

            except:
                print('That is not a valid list URL, please try again.')
                continue
        
        # if a list proceed this way
        elif list_url.split('/')[-3] == 'list':
            try:
                list_name = list_url.split('/')[-2]
                list_url = list_url + '/detail/'            # Adding detail to URL access the personal rating later
                current_list = List(list_name, list_url)
                break

            except:
                print('That is not a valid list URL, please try again.')
                continue
    
    # writing to a CSV file
    try:
        if passed_name != None:
            csv_path = out_dir + passed_name
        else:
            csv_path = out_dir + username + '_' + list_name
        print(f'Writing to {csv_path}.csv')
        list_to_csv(current_list.films, csv_path)
          
    except:
        if passed_name != None:
            csv_path = out_dir + passed_name
        else:
            csv_path = out_dir + list_name
        print(f'Writing to {csv_path}.csv')
        list_to_csv(current_list.films, csv_path)
    
    print('All Done!')

if __name__ == "__main__":

    parser=argparse.ArgumentParser(prog="main", usage="%(prog)s [options] list-url",
                                   description="A Python program that scrapes Letterboxd lists and outputs the information on all of its films in a CSV file. Input form and desired outputs are user customizable. Concurrent scraping of multiple lists is supported.",
                                   epilog="Thank you for using the scraper! If you have any trouble and/or suggestions please contact me via the GitHub page https://github.com/L-Dot/Letterboxd-list-scraper.",
                                   formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version='%(prog)s 2.0.0')

    ## arguments / flags
    parser.add_argument("-vo","--verbose-off",help="Turn off verbose, stops describing everything the program does and no longer displays progression bars.",required=False,action="store_true")
    parser.add_argument("-p","--pages", type=str,
                        help=("only scrape selected pages from a URL. Default is to scrape all pages.\n"
                              "Page selection syntax follows these rules:\n"
                              "\t -p 1 \t\t page 1 (first page)\n"
                              "\t -p 1,3,5 \t pages 1,3,5\n"
                              "\t -p 1~3 \t pages 1,2,3\n"
                              "\t -p 1~3,5 \t pages 1,2,3 and 5\n"
                              "\t -p <3,5 \t pages 1,2,3 and 5\n"
                              "\t -p * \t\t all pages (default)\n"),
                        required=False, default="*")

    parser.add_argument("-on", "--output_name", type=str, nargs="+",
                        help=("set the filename of the output CSV(s). Default output is a CSV file with the same name as its respective list.\n"
                              "If multiple URLs are provided and only one filename, each CSV will be the concatenation of that filename with an increasing number _1, _2, etc. "
                              "If you want to rename each output CSV separately, you can give a list of unique filenames here, each one separated by a space.\n"
                              "If --concat is used, you only have to provide one filename for the concatenated CSV."), 
                        required=False, default=None)
    
    parser.add_argument("-op", "--output_path", type=str, nargs=1, 
                        help="set the path for the output CSV(s). Default output is in the working directory.", 
                        required=False, default=None)
    
    parser.add_argument("-f", "--infile", type=argparse.FileType('r'), nargs=1,
                        help="provide a .txt file with all of the URLs that should be scraped. Each URL should be isolated on its own newline together with its specific option flags. This feature is especially handy when you need to scrape a large amount of lists and/or when you have specific option flags for each URL.", 
                        required=False, default=None)

    parser.add_argument("--concat", type=bool,
                        help="option to concatenate all the scraped lists into one final CSV. An extra column is added that specifies the original list URL.",
                        required=False, default=False)

    ## positionals
    parser.add_argument("list-url", type=str, nargs="*", 
                        help=("the Letterboxd URL of the list that should be scraped. Multiple URLs can be given, separated by a space. For example:\n\n"
                        "\t python %(prog)s.py <list-url_1>\n"
                        "\t python %(prog)s.py <list-url_1> <list-url_2> <list-url_3>"))
    parser.print_help()

    args=parser.parse_args()

    # main( args.list-url)