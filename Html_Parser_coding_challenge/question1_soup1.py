

# Coding Challenge
import bs4 as bs
import os
import json

"""
this function cleans the name. There were many similar names with little difference
The idea is that there should be one artist with that name, so to reduced redundancy
I have removed all extre caracters like - [. , (1550 - 1767), etc ] 

Note: I have purposely kept artist name case sensitive as this did not effect my results.
      but ideally the name should be first lower and then tested
"""
def clean_artist_name(artist):
  
    i = 0
    ret = ''
    while(i < len(artist)):
      
        if (artist[i].isalpha() or artist[i] == ' ') and artist[i] != '.':
            ret += artist[i]
        i += 1
        
    return ret.strip()

"""
return the list of artists
"""
def questiom_1(all_soup):
    # check the NULL case
    if not all_soup or len(all_soup) == 0:
        return
    
    artists = []
    
    # Get the artist name and append in list
    for soup in all_soup:
        artist = soup.find_all('h2')[0].string
        artists.append(clean_artist_name(artist))
            
    """
        I don't want the duplicate in the list so first converting it to set.
        Then converting back to list for the desired result
    """
    return list(set(artists))

"""
Parse the HTML and return the soup obj
"""
def read_soup(file_names):
    all_file_soup1 = []
    for file in file_names:
            f=open(file, 'r')
            soup = bs.BeautifulSoup(f, 'html.parser')
            all_file_soup1.append(soup)
    return all_file_soup1
 

"""
    dump the data into the jason file
"""
def dump_json(obj_list):
    info = json.dumps(obj_list)
    loaded_info = json.loads(info)
    with open('problem1_soup1.json', 'w') as outfile:
        json.dump(loaded_info,outfile)

"""
remember to change the path if the html directory is not in the current folder
"""

file_names = os.listdir('./soup1')
file_names = ["./soup1/"+file for file in file_names if file[-4:] == 'html']


# caller
dump_json(questiom_1(read_soup(file_names)))
