# 507/206 Homework 7 Part 1
import requests
import json
from bs4 import BeautifulSoup

#### Your Part 1 solution goes here ####
#### Implement your function here ####
def get_umsi_data(page):

    base_url = ' https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All'
    umsi = requests.get(base_url+'&page='+str(page), headers={'User-Agent': 'SI_CLASS'})
    soup = BeautifulSoup(umsi.text, 'html.parser')

    list_of_each_person_chunk = soup.find_all(class_='views-row')

    umsi_titles_for_single_page = {}

    for i in range(0,len(list_of_each_person_chunk)):
        first_person_contact_chunk = list_of_each_person_chunk[i].find(class_='field field-name-contact-details field-type-ds field-label-hidden')

        additional_url = first_person_contact_chunk.a['href']
        baseurl_for_each_person = 'https://www.si.umich.edu'

        contact = requests.get(baseurl_for_each_person+additional_url, headers={'User-Agent': 'SI_CLASS'})
        contact_soup = BeautifulSoup(contact.text, 'html.parser')

        name_chunk = contact_soup.find(class_='field-name-title')
        email_chunk = contact_soup.find(class_='field-name-field-person-email')
        title_chunk = contact_soup.find(class_='field-name-field-person-titles')


        umsi_titles_for_single_page[name_chunk.text]= {'tittle':title_chunk.text ,'email':email_chunk.a.text}

    return umsi_titles_for_single_page


def get_unique_key(url):
  return url

def make_request_using_cache(url):
    header = {'User-Agent': 'SI_CLASS'}
    unique_ident = get_unique_key(url)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url, headers=header)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

def caching(page):
    base_url = ' https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All'
    details_url = base_url+'&page='+str(page)
    headers={'User-Agent': 'SI_CLASS'}
    page_text = make_request_using_cache(details_url)
    page_soup = BeautifulSoup(page_text, 'html.parser')

#### Execute funciton, get_umsi_data, here ####

umsi_titles = {}
for i in range(0,13):
    CACHE_FNAME = 'cache_'+str(i)+'.json'
    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()

    except:
        CACHE_DICTION = {}
    caching(i)
    contact_on_each_page = get_umsi_data(i)
    umsi_titles.update(contact_on_each_page)

print(umsi_titles)


#### Write out file here #####
result_file_name = 'directory_dict.json'
rf = open(result_file_name, 'w')
rf.write(json.dumps(umsi_titles))
rf.close()
