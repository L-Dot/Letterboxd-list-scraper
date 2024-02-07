# Some utility functions are stored here
import numpy as np

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