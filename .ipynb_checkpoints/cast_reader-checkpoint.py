def cast_reader(csv_file):
    """
    Takes in a scraped CSV file with a 'Cast' column and
    outputs a normal list of all the cast members.
    Can be used to read in the cast data from a scraped CSV
    
    """
    
    df = pd.read_csv(csv_file)
    
    # importing the cast cell as an entire literal string
    caststring = df['Cast'].values[0]
    cast = [ actor.strip(" '") for actor in castio[1:-1].split(',') ]
    
    return cast