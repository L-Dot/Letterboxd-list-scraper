# Letterboxd-list-scraper

A tool for scraping Letterboxd lists from a simple URL. The output is a file with film titles, release year, director, cast, owner rating, average rating and a whole lot more (see example CSVs and JSONs in `/example_output/`). 

Version v2.2.0 supports the scraping of:
- **Lists** (e.g. `https://letterboxd.com/bjornbork/list/het-huis-anubis/`)
- **Watchlists** (e.g. `https://letterboxd.com/joelhaver/watchlist/`)
- **User films** (e.g. `https://letterboxd.com/mscorsese/films/`)
- **Generic Letterboxd films** (e.g. `https://letterboxd.com/films/popular/this/week/genre/documentary/`)
- **Roles** (e.g. `https://letterboxd.com/actor/willem-dafoe/`)

The current scrape rate is about 1.2 films per second. Multiple lists can be concurrently scraped using separate CPU threads (default max of 4 threads, but this is configurable).

## Getting Started

### Dependencies

Requires Python 3.x, numpy, BeautifulSoup (bs4), requests, tqdm and **lxml**.

If dependencies are not met it is recommended to install everything needed in one go using `pip install -r requirements.txt` (ideally in a clean virtual environment).

### Installing

* Clone the repository and work in there.

### Executing program

* Execute the program by running `python -m listscraper [options] [list-url]` on the command line in the project directory. 

    Multiple list URLs can be provided, separated by a space. The output file(s) can then be found in the folder `/scraper_outputs/`, which will be created if not already present.
    Some of the optional flags are:
    - `-p` or `--pages` can be used to select specific pages.
    - `-on` or `--output-name` can be used to give the output file(s) a user-specified name.
    - `-f` or `--file` can be used to import a .txt file with multiple list URLs that should be scraped.
    - `-op` or `--output-path` can be used to write the output file(s) to a desired directory.
    - `-ofe` or `--output-file-extension` can be used to specify what type of file is outputted (support for CSV and json).
    - `--concat` will concatenate all films of the given lists and output them in a single file.

> [!NOTE]
> Please use `python -m listscraper --help` for a full list of all available flags including extensive descriptions on how to use them.

> [!TIP]
> Scraping multiple lists is most easily done by running `python -m listscraper -f <file>` with a custom .txt file that contains the URL on each newline. Each newline can take unique `-p` and `-on` optional flags. For an example of such a file please see `target_lists.txt`.

> [!IMPORTANT]
> Program currently does not support the scraping of extremely long generic Letterboxd pages (e.g. `https://letterboxd.com/films/popular/this/week/genre/documentary/`, which contains ~152000 films). To circumvent this, please use the `-p` flag to make a smaller page selection.

## TODO

* Add further options for output, currently supports CSV and json.
* Add scrape functionality for user top 4 and diary.
* Add `-u <username>` flag that scrapes the diary, top 4, films and lists of a single user.
* Add a `--meta-data` flag to print original list name, scrape date, username above CSV header.
* Optimize thread usage to increase scrape speed.


## Authors

Arno Lafontaine  

## Acknowledgments

Thanks to BBotml for the inspiration for this project https://github.com/BBottoml/Letterboxd-friend-ranker.
