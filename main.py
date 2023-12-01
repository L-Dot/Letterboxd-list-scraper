from list_class import *
from csv_writer import *

'''
Letterboxd List scraper - main program
'''

def main():
    print('====================================================')
    print('Welcome to the Letterboxd List scraper!')
    print('Provided with an URL, this program outputs a CSV file') 
    print('of movie title, release data and Letterboxd link.') 
    print('Example url: https://letterboxd.com/.../list/short-films/).')
    print('The program currently only supports lists and watchlists.')
    print('Enter q or quit to exit the program.')
    print('====================================================\n')
    
    # Checking if URL is of a watchlist or of a list
    while True:
        list_url = input('Enter the URL of the list you wish to scrape:')
        
        # exit option
        if list_url == 'q' or list_url == 'quit':
            exit()
            
        # if a watchlist proceed this way
        elif list_url.split('/')[-3] != 'list':
            try:
                list_name = list_url.split('/')[-2]
                username = list_url.split('/')[-3]
                current_list = List(list_name, list_url)
                break

            except:
                print('That is not a valid URL, please try again.')
                continue
        
        # if a list proceed this way
        elif list_url.split('/')[-3] == 'list':
            try:
                # Changed to -3 because could only get personal rating if using detail view
                list_name = list_url.split('/')[-3]
                current_list = List(list_name, list_url)
                break

            except:
                print('That is not a valid URL, please try again.')
                continue
    
    # writing to a CSV file
    try:
        csv_name = username + '_' + list_name
        print(f'Writing to {csv_name}.csv.')
        list_to_csv(current_list.films, csv_name)
          
    except:
        print(f'Writing to {list_name}.csv.')
        list_to_csv(current_list.films, list_name)
    
    print('Done!')

if __name__ == "__main__":
    main()
