def transform_stars(starstring):
    """
    Transforms star rating into float value
    """
    stars = {
        "★": 1,
        "★★": 2,
        "★★★": 3,
        "★★★★": 4,
        "★★★★★": 5,
        "½": 0.5,
        "★½": 1.5,
        "★★½": 2.5,
        "★★★½": 3.5,
        "★★★★½": 4.5
    }
    try:
        return stars[starstring]
    except:
        print('AAAAAAAAAAAAA')
        return -1