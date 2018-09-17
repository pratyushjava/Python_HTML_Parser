
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
    return the list of dict {'artist': artist,
                            'works': [{'title' : work, 
                                    'currency' : price[0],
                                        'amount': price[1]}]} format
"""
def questiom_4(all_soup):
    if not all_soup or len(all_soup) == 0:
        return
    
    """
        the idea is to first have a key with artist name, 
        so that the all records can be added to the same artist.
        since we need {'artist': artist, 'works': [work]} as a result.
        later I have returned only values of this dict which will not have 
        artist name as key.
    """
    
    object_dicts = {}
    
    for soup in all_soup:
        artist = soup.find_all('h2')[0].string
        artist = clean_artist_name(artist)
        work = soup.find_all('h3')[0].string
        price = soup.find_all('div')[1].string
        price = price.split()
        if artist in object_dicts:
            object_dicts[artist]['works'].append({'title' : work, 'price' : price})
        else:
            object_dicts[artist] = {'artist': artist,
                                   'works': [{'title' : work, 'currency' : price[0],
                                              'amount': price[1]}]}
            
            
    return list(object_dicts.values())
        

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
    with open('problem4_1.json', 'w') as outfile:
        json.dump(loaded_info,outfile)
    

"""
remember to change the path if the html directory is not in the current folder
"""
file_names = os.listdir('./soup1')
file_names = ["./soup1/"+file for file in file_names if file[-4:] == 'html']

# caller
dump_json(questiom_4(read_soup(file_names)))


