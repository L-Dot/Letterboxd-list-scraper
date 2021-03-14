import csv

def list_to_csv(film_rows, list_name):
    """
    Takes in a list of lists and converts it to a CSV file
    
    """
    
    with open(f'{list_name}.csv', 'w') as f:
        write = csv.writer(f)

        write.writerows(film_rows)
        
    return