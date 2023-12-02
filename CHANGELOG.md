# Change Log
All notable changes to this project will be documented in this file.

## [1.1] - 2023-12-02
 
The first update of this app after its 'official' release back in 2021. Thanks to everyone that still uses or has used this application. It is heartwarming and encouraging that people actually use and benefit from this piece of code I created :). The main work of this update comes from [@DenJackson42](https://github.com/DenJackson42), which [pull request](https://github.com/L-Dot/Letterboxd-list-scraper/pull/3) was merged to the main branch. I added some additional features and tested the code's performance against several lists. Please do let me know if you encounter any problems!

Again, I'm very grateful to the people that have come with suggestions, have helped me with the coding, or even just commented on my project. Your investment motivates me dearly.

A summary of the added features is given below:

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
    - New CSV files use the delimiter of `;` as some movies have a `,` in the title.
