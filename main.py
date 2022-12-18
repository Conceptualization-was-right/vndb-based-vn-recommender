import pandas as pd
import requests


class Vote:
    """Class for application users visual novel votes"""
    def __init__(self, id, vote):
        self.novel_id = id
        self.user_vote = vote * 10  # '* 10' for equal data format (vndb_votes)


class Recs:
    """Class for user's visual novel recommendations"""
    def __init__(self, id, title):
        self.rec_id = id
        self.rec_title = title


def print_vn_info(response):
    """Function prints all information about the visual novel,
    changes the rating format to 10-point scale,
    and warns if vn image may contain explicit content
    """
    results = response.json()
    fields = ['title', 'image', 'description', 'popularity', 'rating']
    is_adult = False
    if results['results'][0]['image']['sexual'] >= 1: # a number from 0 to 2 indicates the level of adult content (0 - min, 2 - max)
        is_adult = True
    for field in fields:
        field_info = results['results'][0][field]
        if field == 'rating':
            field_info = round(field_info / 10, 1)  # changing rating format
        if field == 'image':
            field_info = str(results['results'][0][field]['url'])
            if is_adult:
                field_info += ' WARNING: image may contain explicit content'
        print(str(field).capitalize(), '—', field_info)


def find_vn():
    """Function finds visual novel in vndb database by its id or title,
     1 result if search by id, 3 results (if available 3 or more) if search by title
    """
    found_vn_id = 0
    answer = input('Do you want to find a visual novel by id or by title? t: title, id: id')
    if answer == 'id':
        vn_id = input('Enter visual novel id')
        filter = '{"filters": ["id", "=", ' + vn_id + '], "fields": "title, image.url, image.sexual, description, popularity, rating"}'
        headers = {'Content-Type': 'application/json'}
        response = requests.post('https://api.vndb.org/kana/vn', headers=headers, data=filter)
        print(response.text)




def rate_vn():
    pass


def import_vndb_votes():
    pass




# XML import only vn and votes
data = pd.read_xml('data/my_import.xml', xpath='.//vn')

# remaining columns: id, title, vote
new_data = data.drop(['private', 'label', 'added'], axis='columns')

print(new_data)

# filters: 'search' for title, 'id' for id
filter = '{"filters": ["id", "=", "17"], "fields": "title, image.url, image.sexual, description, popularity, rating"}'
headers = {'Content-Type': 'application/json'}

# 'reverse: true' for top popular novels
popularity_filter = '{"fields": "title, image.url", "sort": "popularity", "reverse": true, "results": 2}'
response = requests.post('https://api.vndb.org/kana/vn', headers=headers, data=filter)

#print_vn_info(response)


