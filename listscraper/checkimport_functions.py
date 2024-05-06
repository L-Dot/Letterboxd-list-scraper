# This file contains functions that checks the user-input and, if deemed valid, imports the relevant information
# If user-input is not valid, a relevant error message is generated and printed

ROLES = [
    "actor",
    "additional-directing",
    "additional-photography",
    "art-direction",
    "assistant-director",
    "camera-operator",
    "casting",
    "choreography",
    "cinematography",
    "co-director",
    "composer",
    "costume-design",
    "director",
    "editor",
    "executive-producer",
    "hairstyling",
    "lighting",
    "makeup",
    "original-writer",
    "producer",
    "production-design",
    "set-decoration",
    "songs",
    "sound",
    "special-effects",
    "story",
    "stunts",
    "title-design",
    "visual-effects",
    "writer",
]

def checkimport_url(url_string):
    """
    Checks the input URL for correct syntax and imports relevant list information.

        Parameters:
            url_string (str):   The input URL.
        
        Returns:
            check (boolean):    True or False depending on if the input URL is recognized by the program.
            type (str):         The list type (watchlist, list, films).
            username (str):     The username of the lists owner.
            listname (str):     The program-assigned name for the list, extracted from the URL.
    """

    url_chunks = url_string.split('/')
    
    try: 
        # All user-type lists
        if url_chunks[4] == "list":
            type = "list"
            username = url_chunks[3]
            listname = url_chunks[5]
            check = True

        elif url_chunks[4] == "watchlist":
            type = "watchlist"
            username = url_chunks[3]
            listname = f"{username.lower()}-watchlist"
            check = True

        elif url_chunks[4] == "films":
            type = "films"
            username = url_chunks[3]
            listname = f"{username.lower()}-films"
            check = True
        
        # Letterboxd site generic lists
        elif url_chunks[3] == "films" and len(url_chunks) > 5:
            type = "LBfilms"
            username = "Letterboxd"
            listname = "LBfilms"
            check = True
        
        # Cast / Crew roles
        elif url_chunks[3] in ROLES:
            type = "Cast/Crew"
            username = "Letterboxd"
            listname = f"{url_chunks[3]}-{url_chunks[4]}-films"
            check = True

        else:
            check = False
            type, username, listname = ['']*3

    except:
        check = False
        type, username, listname = ['']*3

    # Check for additional selection in URL and add it to the list output name
    if (type in {"list"} and len(url_chunks) > 7):
        extra_chunks = url_chunks[6:-1]
        listname = listname + "-" + ("-").join(extra_chunks)

    elif (type in {"watchlist", "films"} and len(url_chunks) > 6):
        extra_chunks = url_chunks[5:-1]
        listname = listname + "-" + ("-").join(extra_chunks)
        
    elif (type in {"LBfilms"}):
        extra_chunks = url_chunks[4:-1]
        listname = listname + "-" + ("-").join(extra_chunks)

    return check, type, username, listname

def checkimport_output_output_file_extension(output_file_extension):
    """ 
    Checks if valid output file extension was given.

    Returns:
        check (bool):       Check for if the output file extension is valid.
        extension (str):    The output file extension for the file.
    """

    if output_file_extension == ".json" or output_file_extension == ".csv":
        check = True
        extension = output_file_extension
    elif output_file_extension == "json" or output_file_extension == "csv":
        check = True
        extension = "." + output_file_extension
    else:
        check = False
        extension = None

    return check, extension

def checkimport_outputname(output_name, global_output_name, output_file_extension, listname, url_total, url_count, concat):
    """ 
    Checks if valid output names are given, then finds the appropriate output name for the list.

    Returns:
        check (bool):   Check for if the output name is valid.
        name (str):     The output name for the list.
    """

    # Checks for if concat was applied
    if concat and global_output_name:
        check = True
        name = global_output_name + output_file_extension
        return check, name
    elif concat and (global_output_name == None):
        check = True
        name = "concatenated" + output_file_extension
        return check, name
    else:

        # Checks if concat was not applied
        if output_name == None:
            check = True
            name = listname + output_file_extension
        elif output_name != global_output_name:
            check = True
            name = output_name + output_file_extension
        elif (output_name != None) and (url_total == 1):
            check = True
            name = output_name + output_file_extension
        elif (output_name != None) and (url_total > 1):
            check = True
            name = output_name + f"_{url_count - 1}" + output_file_extension
        else:
            check = False
            name = ""
    
    return check, name

def checkimport_pages(pages_string):
    """
    Checks the input string for correct syntax and converts to
    a list of integers representing all the pages that should be scraped.

        Parameters:
            pages_string (str): The input after the "-p" flag
        
        Returns:
            check (boolean):    True or False depending on if the input string could be decoded.
            final_pages (list): An explicit list of integers denoting the pages that should be scraped.
                                In case all pages should be scraped, this list is empty.
    """

    final_pages = []
    try:
        if pages_string == "*":
            check = True
            return check, final_pages

        chunks = pages_string.split(",")
        for chunk in chunks:
            if "~" in chunk:
                i, j = chunk.split("~")
                if int(i) <= int(j):
                    if int(i) == 0:
                        i = 1
                    final_pages.extend(range(int(i),int(j)+1))
                else:
                    check = False
                    return check, final_pages
            
            elif "<" in chunk:
                j = chunk.split("<")[1]
                print(j)
                final_pages.extend(range(1,int(j)))
            else:
                final_pages.append(int(chunk))

        final_pages = list(sorted(set(final_pages)))            # Delete duplicates and sort
        check = True
    except:
        check = False

    return check, final_pages