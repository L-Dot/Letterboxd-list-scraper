# Change Log
All notable changes to this project will be documented in this file.

## [2.0.0] - 2023-02-06

-
This update comes with a full overhaul of the Letterboxd-list-scraper into a more interactive and functional Command Line Interface (CLI). This was done by implementing `argparse` together with a load of optional flags that can be provided along with the URL.

This overhaul has resulted in the code becoming a lot longer and more complicated in some parts. I have tried to keep a good readability by providing logical function and variable names and a lot of comments and docstrings. While I have done a lot of manual testing, I still expect a lot of new bugs to occur. Please do inform me on these if you find them. A near-future goal of mine is to add test functions and structure the code in a way more in line to the general rules of software applications.

In the meantime I hope you can enjoy and use the new 2.0.0 version of this program!
-

### Added
- The program can now be run via `python -m listscraper <list-URL>`. This is the simplest case, but multiple optional flags were added for functionality. Some of these flags are:
    - `--pages` can be used to select specific pages.
    - `--output-name` can be used to give the output CSV(s) a user-specified name.
    - `--file` can be used to import a .txt file with multiple list URLs that should be scraped. Each URL can have its own optional `--pages` and/or `--output-name` flags.
    - `--output-path` can be used to write the output CSV(s) to the desired directory.
    - `--concat` will concatenate all films of the given lists and output them in a single CSV.

    See the full overview of all flags by running `python -m listscraper --help`. 

- More scrape data! For each film the program now also scrapes:
    - Fan count (rounded off to whole thousands because of the 'K' notation LB uses).
    - Total ratings amount.
    - Rating count of all histogram bars (i.e. how many times people rated ½, ★, ★½, etc.).

- Support for more URL types. The supported URL types now include:
    - Lists (e.g. `https://letterboxd.com/bjornbork/list/het-huis-anubis/`)
    - Watchlists (e.g. `https://letterboxd.com/joelhaver/watchlist/`)
    - User films (e.g. `https://letterboxd.com/mscorsese/films/`)
    - Generic Letterboxd films (e.g. `https://letterboxd.com/films/popular/this/week/genre/documentary/`)

    Besides these, each URL can be extended with additional selection criteria. You can thus for example provide the scraper with a list like `https://letterboxd.com/mscorsese/films/decade/1950s/genre/drama/` to obtain only the films Mr. Scorsese watched that are from the 1950s and fall under the 'drama' genre. This works for all URL types and is **required** when scraping generic Letterboxd film lists.

- Program prints more detailed progress updates.

### Changed
- Updated the README to reflect changes.

- Changed some filenames (=>), moved functions (->) and/or added new modules (new) for better project organization:
    - `main.py` => `__main__.py`
        The initiator script of the program was renamed and altered for cleaner code.
    
    - (new) `instance_class.py`
        Contains the main program code. Actualizes the program as a class instance which is useful for storing information.

    - `list_scraper.py` => `scrape_functions.py`
        New file contains all functions related specifically to the scraping procedure.

    - (new) `utility_functions.py`
        Contains small amount of utility functions.
    - `cast_reader.py` -> `utility_functions.py`

    - (new) `checkimport_functions.py`
        Contains functions that check the input options and extract/import the relevant information.
    
    - (new) `cli.py`
        Contains all code regarding the command line interface argument parser.

- In actuality a huge amount of changes in the overall code (too much to list here), but the general working of the scraper has stayed exactly the same.

### Fixed
- Fixed an issue with scraping the stats page (watches, likes, list additions) in [#6](https://github.com/L-Dot/Letterboxd-list-scraper/issues/6) by changing the page URL (the page was not deleted luckily).


## [1.1.0] - 2023-12-02

### Added
- More scraping! Added new data columns for each film's:
    - Number of watches.
    - Number of appearances on a list.
    - Number of likes.
    - Genres.
    - Studios.
    - Countries.
    - Original language.
    - Spoken languages.
    - Owner rating (i.e. the rating that the owner of the list gave the film).
   
These additions were mostly inspired by users in issue [#2](https://github.com/L-Dot/Letterboxd-list-scraper/issues/2).
 
### Changed
- Updated the `requirements.txt` file.
 
### Fixed
- Some changes suggested in issue [#1](https://github.com/L-Dot/Letterboxd-list-scraper/issues/1):
    - UnicodeEncodeError was resolved by using `utf-8` encoding when writing the CSV.
