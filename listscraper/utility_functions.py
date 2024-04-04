# Some utility functions are stored here

def stars2val(stars, not_found):
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
        return not_found
    
def val2stars(val, not_found):
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
        return not_found