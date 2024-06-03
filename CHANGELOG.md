# Change Log
All notable changes to this project will be documented in this file.

## [2.2.0] - 2024-06-03

### Added

- Functionality to scrape all films from a certain `role` (i.e. person) in Cast/Crew. The input links for these should follow the structure of `https://letterboxd.com/{role}/{name}/` (e.g. https://letterboxd.com/actor/anne-hathaway/). 
     
   - A list of the currently available roles includes:
     ```
     ROLES = [
        "actor",
        "additional-directing",
        "additional-photography",
        "art-direction",
        "assistant-director",
        "camera-operator",
        "casting",
        "choreography",
        "cinematography",
        "co-director",
        "composer",
        "costume-design",
        "director",
        "editor",
        "executive-producer",
        "hairstyling",
        "lighting",
        "makeup",
        "original-writer",
        "producer",
        "production-design",
        "set-decoration",
        "songs",
        "sound",
        "special-effects",
        "story",
        "stunts",
        "title-design",
        "visual-effects",
        "writer",
        ]
    This feature was added by @jonathanhouge in [#13](https://github.com/L-Dot/Letterboxd-list-scraper/pull/13).

  
- Functionality to scrape the description/synopsis of films, if available. The scraped text is written to the `Description` column. This change was inspired by @meanjoep92 in [#2](https://github.com/L-Dot/Letterboxd-list-scraper/issues/2).


## [2.1.0] - 2024-04-23

### Added
- Functionality to export the lists to a JSON file. 
Added by @jonathanhouge in [#11](https://github.com/L-Dot/Letterboxd-list-scraper/issues/11).

### Fixed
- A bug that caused incomplete writeout when the first film in the list was an unreleased film (see issue [#8](https://github.com/L-Dot/Letterboxd-list-scraper/issues/8) and issue [#12](https://github.com/L-Dot/Letterboxd-list-scraper/issues/12)).


## [2.0.0] - 2024-02-06

### Added
- The program can now be run on the command line via `python -m listscraper <list-URL>`. This is the simplest case, but multiple optional flags were added for functionality. Some of these flags are:
    - `--pages` can be used to select specific pages.
    - `--output-name` can be used to give the output CSV(s) a user-specified name.
    - `--file` can be used to import a .txt file with multiple list URLs that should be scraped. Each URL can have its own optional `--pages` and/or `--output-name` flags.
    - `--output-path` can be used to write the output CSV(s) to the desired directory.
    - `--concat` will concatenate all films of the given lists and output them in a single CSV.

    See the full overview of all flags by running `python -m listscraper --help`. 

- More scrape data! For each film the program now also scrapes:
    - Fan count (rounded off to whole hundreds because of the 'K' notation LB uses).
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
    - `main.py` => `__main__.py` <br>
        The initiator script of the program was renamed and altered for cleaner code.
    - `list_scraper.py` => `scrape_functions.py` <br>
       File was renamed and now contains all functions related specifically to the scraping procedure.
    - (new) `instance_class.py` <br>
        Contains the main program code. Actualizes the program as a class instance which is useful for storing information.
    - (new) `utility_functions.py` <br>
        Contains small utility functions.
    - (new) `checkimport_functions.py` <br>
        Contains functions that check the input arguments and extract/import the relevant information.
    - (new) `cli.py` <br>
        Contains all code regarding the command line interface argument parser.

- In actuality a huge amount of changes in the overall code (too much to list here), but the general working of the scraper has stayed exactly the same.

### Fixed
- Fixed an issue with scraping the stats page (watches, likes, list additions) in [#6](https://github.com/L-Dot/Letterboxd-list-scraper/issues/6) by changing the page URL (the page was not deleted luckily).
- Fixed an issue with not scraping some film title's correctly as mentioned by @BeSweets in [#2](https://github.com/L-Dot/Letterboxd-list-scraper/issues/2).

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
