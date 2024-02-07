# Some utility functions are stored here
import numpy as np
import pandas as pd

def stars2val(stars):
    """
    Transforms star rating into float value.
    """
    
    conv_dict = {
        "★": 1.0,
        "★★": 2.0,
        "★★★": 3.0,
        "★★★★": 4.0,
        "★★★★★": 5.0,
        "½": 0.5,
        "★½": 1.5,
        "★★½": 2.5,
        "★★★½": 3.5,
        "★★★★½": 4.5 }

    try:
        val = conv_dict[stars]
        return val
    except:
        return np.nan
    
def val2stars(val):
    """
    Transforms float value into star string.
    """
    conv_dict = {
        1.0 : "★",
        2.0 : "★★",
        3.0 : "★★★",
        4.0 : "★★★★",
        5.0 : "★★★★★",
        0.5 : "½",
        1.5 : "★½",
        2.5 : "★★½",
        3.5 : "★★★½",
        4.5 : "★★★★½" }
    try:
        stars = conv_dict[val]
        return stars
    except:
        return np.nan

def cast_reader(csv_file, film_title):
    """
    Takes in a scraped CSV file with a 'Cast' column and
    a specific movie and outputs a normal list of all the cast members.
    Can be used to read in the cast data from a scraped CSV
    """
    
    df = pd.read_csv(csv_file)

    # importing the cast cell as an entire literal string
    movie = df[df['Film_title'] == film_title]
    caststring = movie['Cast'].values[0]

    # check if cast is not nan
    try:
        cast = [ actor.strip(" '") for actor in caststring[1:-1].split(',') ]
        return cast
    
    except:
        return []