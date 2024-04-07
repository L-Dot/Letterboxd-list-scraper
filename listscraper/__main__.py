from listscraper.cli import cli_arguments
from listscraper.instance_class import ScrapeInstance


def main():
    """
    Starts the program and prints some text when finished.
    """

    # Welcome message
    print("=============================================")
    print("           Letterboxd-List-Scraper           ")
    print("=============================================")

    # Importing command line arguments and create a scrape instance
    args = cli_arguments()
    LBscraper = ScrapeInstance(args.listURL, args.pages, args.output_name, args.output_path, args.output_file_extension, args.file, args.concat, args.quiet, args.threads)

    # # End message
    print(f"\nProgram successfully finished! Your {LBscraper.output_file_extension}(s) can be found in ./{LBscraper.output_path}/.")
    print(f"    Total run time was {LBscraper.endtime - LBscraper.starttime :.2f} seconds.")


if __name__ == "__main__":
    main()