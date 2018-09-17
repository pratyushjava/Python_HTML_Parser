

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
    if not all_soup or len(all_soup) == 0:
        return
    
    artists = []
    
    for soup in all_soup:
        artist = soup.find_all('h3')[0].string
        artist = clean_artist_name(artist)
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
    with open('problem1_soup2.json', 'w') as outfile:
        json.dump(loaded_info,outfile)
    
"""
remember to change the path if the html directory is not in the current folder
"""

file_names = os.listdir('./soup2')
file_names = ["./soup2/"+file for file in file_names if file[-4:] == 'html']

# caller
dump_json(questiom_1(read_soup(file_names)))
