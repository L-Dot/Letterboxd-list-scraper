# Change Log
All notable changes to this project will be documented in this file.

## [1.1] - 2023-12-02

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
