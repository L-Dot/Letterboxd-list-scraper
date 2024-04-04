import argparse

def cli_arguments():
    """
    Function that parses the user-input arguments from the command line interface (CLI)
    and returns these arguments stored in an 'args' object.
    """

    parser=argparse.ArgumentParser(prog="listscraper", usage="%(prog)s [options] [list-url]",
                                   description="A Python program that scrapes Letterboxd lists and outputs the information on all of its films in a file. Input form and desired outputs are user customizable. Concurrent scraping of multiple lists is supported.",
                                   epilog="Thank you for using the scraper! If you have any trouble and/or suggestions please contact me via the GitHub page https://github.com/L-Dot/Letterboxd-list-scraper.",
                                   formatter_class=argparse.RawTextHelpFormatter)
    
    ## Optional arguments / flags
    parser.add_argument('--version', action='version', version='%(prog)s 2.0.0')

    parser.add_argument("-on", "--output_name", type=str,
                        help=("set the filename of the output file(s). Default output is a CSV file with the same name as its respective list.\n"
                              "If this flag is used and multiple URLs are provided, each file will be the concatenation of the output name with an increasing number _1, _2, etc.\n"), 
                        required=False, default=None)
    
    parser.add_argument("-op", "--output_path", type=str, 
                        help="set the path for the output file(s). Default output is a folder called 'scraper_outputs'.", 
                        required=False, default="scraper_outputs")

    parser.add_argument("-ofe", "--output_file_extension", type=str,
                        help="specify output file type, .csv or .json. Default output is .csv.",
                        required=False, default=".csv")
    
    parser.add_argument("-f", "--file", type=argparse.FileType('r'),
                        help="provide a .txt file with all of the URLs that should be scraped. Each URL should be isolated on its own newline together with any specific option flags. \
                            This feature is especially handy when you need to scrape a large amount of lists and/or when you have specific option flags for each URL.\n\
                            When using an input file, make sure to not give the script any URLs on the command line!", 
                        required=False, default=None)

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

    parser.add_argument("--concat", action="store_true",
                        help="option to output all the scraped lists into a single concatenated file. An extra column is added that specifies the original list URL.",
                        required=False)
    
    parser.add_argument("--threads", type=int,
                        help="option to tweak the number of CPU threads used. Increase this to speed up scraping of multiple lists simultaneously. Default value is 4.",
                        required=False, default=4)

    parser.add_argument("--quiet", action="store_true",
                        help="Stops describing everything the program does and no longer displays tqdm() progression bars.\
                        From testing this does not significantly increase program runtime, meaning this is turned off by default.",
                        required=False)
    
    ## WIP ##
    # parser.add_argument("--more-stats", action=argparse.BooleanOptionalAction,
    #                     help="option to enable extensive scraping, at the cost of a small increase in runtime. New data includes info on a film's rating histogram and fans.",
    #                     required=False, default=False)

    # parser.add_argument("--meta-data", action=argparse.BooleanOptionalAction,
    #                     help="option to add a header row with some meta data to the CSV.",
    #                     required=False, default=False)

    ## Positionals
    parser.add_argument("listURL", type=str, nargs="*", 
                        help=("the Letterboxd URL of the list that should be scraped. Multiple URLs can be given, separated by a space. For example:\n\n"
                        "\t python %(prog)s.py <list-url_1>\n"
                        "\t python %(prog)s.py <list-url_1> <list-url_2> <list-url_3>"))

    args=parser.parse_args()

    return args
