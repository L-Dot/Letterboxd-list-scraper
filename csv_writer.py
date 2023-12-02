import csv

def list_to_csv(film_rows, list_name):
    """
    Takes in a list of filmrows outputted by the list_scraper()
    and converts it to a CSV file
    
    """
    
    with open(f'{list_name}.csv', 'w', newline="", encoding = "utf-8") as f:
        write = csv.writer(f, delimiter=",")
        write.writerows(film_rows)
    return