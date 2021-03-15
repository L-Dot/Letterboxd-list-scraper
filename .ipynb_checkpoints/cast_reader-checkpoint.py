import pandas

def cast_reader(csv_file, film_title):
    """
    Takes in a scraped CSV file with a 'Cast' column and
    a specific movie and outputs a normal list of all the cast members.
    Can be used to read in the cast data from a scraped CSV
    
    """
    
    df = pandas.read_csv(csv_file)

    # importing the cast cell as an entire literal string
    movie = df[df['Film_title'] == film_title]
    caststring = movie['Cast'].values[0]

    # check if cast is not nan
    try:
        cast = [ actor.strip(" '") for actor in caststring[1:-1].split(',') ]
        return cast
    
    except:
        return []
    
    