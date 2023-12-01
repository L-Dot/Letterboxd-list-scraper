# Letterboxd-list-scraper

A tool for scraping Letterboxd lists from a simple URL. The output is a CSV file with film titles, release year, director, cast, rating (only available for personal film lists), average rating and a link to the Letterboxd page. The current version is tested on watchlists and normal lists. The current scrape rate is about 1.3 seconds per film.

## Getting Started

### Dependencies

Requires python 3.x, numpy, BeautifulSoup (bs4), requests and tqdm.

### Installing

* Copy over the repository and work in there.

### Executing program

* Run the program by running ` python main.py` and inputting a valid URL (e.g. https://letterboxd.com/bjornbork/list/het-huis-anubis/detail/). After some time a CSV file will be outputted containing your data. See `imdb-top-250.csv` for a preview.
* The detailed version of the list (same url but with /detail on the end) should be used or personal ratings may not be scraped.
* Use the script `cast_reader.py` to read-in the 'Cast' column from the CSV files to proper python lists.

## TODO

* Create a list identifier to identify if the input URL contains a watchlist, personal films list, or normal list and let the code behave accordingly (e.g. no rating scraping for a watchlist).

* Create a way that user can choose to request only specific data and not all.

* Add feature that scrapes how many times a movie has been given a specific rating.

## Authors

Arno Lafontaine  

## Acknowledgments

Thanks to BBotml for the inspiration for this project https://github.com/BBottoml/Letterboxd-friend-ranker.
