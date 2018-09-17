
# Coding Challenge
import bs4 as bs
import os    
import json



"""
    This is a utility function which will compute the total amount
    rate of usd is 1.3, 
    prev: is the already computed total of previous work of this artist
    currency: usd or gbp
    amount: value
"""
def get_total_value(currency, amount , prev = ''):
    
    if prev != '':
        prev = prev.split()
        prev = float(prev[1])
    else:
        prev = 0
    
    amount = int(''.join(amount.split(',')))
    if currency.lower() != 'usd':
        amount *= 1.34
    
    amount += prev
    
    # expecting to be in two decimal places
    amount = "%.2f" % round(amount,2)
    return "USD "+ str(amount)




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
return the list of dict {'artist': artist, 'totalValue': get_total_value(price[0] , price[1]),
                                   'works': [{'title' : work, 'currency' : price[0],
                                              'totalLifetimeValue': price[1]}]} format
"""
def question_5_soup1(all_soup):
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
        # clean the name
        artist = clean_artist_name(artist)
        work = soup.find_all('h3')[0].string
        price = soup.find_all('div')[1].string
        price = price.split()
        
        """
            totalvalue is computed as sum of all price in USD
        """
        if artist in object_dicts:
            object_dicts[artist]['works'].append({'title' : work, 'currency' : price[0],
                                              'totalLifetimeValue': price[1]})
            object_dicts[artist]['totalValue'] = get_total_value(price[0] , price[1] , 
                                                                 object_dicts[artist]['totalValue'])
            
        else:
            object_dicts[artist] = {'artist': artist,
                                    'totalValue': get_total_value(price[0] , price[1]),
                                   'works': [{'title' : work, 'currency' : price[0],
                                              'totalLifetimeValue': price[1]}]}
            
    # return complete dict because it will be modified in below function question_5_soup2
    return object_dicts
        

    
"""
This is a similar function to the previous one, just it runs on different data set
I have kept two different function for modularization. 

object_dicts: this is a dict which is returned from above functions question_5_soup1.
"""
def question_5_soup2(all_soup , object_dicts):
    if not all_soup or len(all_soup) == 0:
        return
    
    
    for soup in all_soup:
        price = [soup.find_all('span')[0].string , soup.find_all('span')[1].string]
        artist = soup.find_all('h3')[0].string
        artist = clean_artist_name(artist)
        work = soup.find_all('h3')[1].string 
        
        """
            totalvalue is computed as sum of all price in USD
        """
        
        if artist in object_dicts:
            object_dicts[artist]['works'].append({'title' : work, 'currency' : price[0],
                                              'totalLifetimeValue': price[1]})
            object_dicts[artist]['totalValue'] = get_total_value(price[0] , price[1] , 
                                                                 object_dicts[artist]['totalValue'])
            
        else:
            object_dicts[artist] = {'artist': artist,
                                    'totalValue': get_total_value(price[0] , price[1]),
                                   'works': [{'title' : work, 'currency' : price[0],
                                              'totalLifetimeValue': price[1]}]}
            
            
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
    with open('problem5.json', 'w') as outfile:
        json.dump(loaded_info,outfile)
    

"""
remember to change the path if the html directory is not in the current folder
"""
file_names = os.listdir('./soup1')
file_names = ["./soup1/"+file for file in file_names if file[-4:] == 'html']

# parse first data set
object_dicts = question_5_soup1(read_soup(file_names))

file_names = os.listdir('./soup2')
file_names = ["./soup2/"+file for file in file_names if file[-4:] == 'html']

# parse second data set
dump_json(question_5_soup2(read_soup(file_names) , object_dicts))