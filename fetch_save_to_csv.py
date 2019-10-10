import csv
import sys
import time

import requests

THROTTLE_INTERVAL = 1.3


def get_reviews(app_id, page_num):
    time.sleep(THROTTLE_INTERVAL) # be kind to apple's api endpoint

    url = f'https://itunes.apple.com/rss/customerreviews/id={app_id}/page={page_num}/sortby=mostrecent/json'
    res = requests.get(url)
    res_json = res.json()
    data = res_json.get('feed')

    if data.get('entry') == None: return None

    reviews = []

    for entry in data.get('entry'):
        if entry.get('im:name'): continue
        review_id = entry.get('id').get('label')
        title = entry.get('title').get('label')
        author = entry.get('author').get('name').get('label')
        author_url = entry.get('author').get('uri').get('label')
        version = entry.get('im:version').get('label')
        rating = entry.get('im:rating').get('label')
        review = entry.get('content').get('label').replace("\n", ' ')
        vote_count = entry.get('im:voteCount').get('label')
        review = [review_id, title.replace('"', '""'), author, author_url, version, rating, review.replace('"', '""'), vote_count]
        reviews.append(review)

    return reviews


def get_all_reivews(app_id, filename):
    headers = ['review_id', 'title', 'author', 'author_url', 'version', 'rating', 'review', 'vote_count']

    if filename:
        compiled_filename = f"{filename}_{app_id}.csv"
    else:
        compiled_filename = f"{app_id}.csv"

    with open(compiled_filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        max_page = 10 # rss feed from apple maxs out at 10

        for page_num in range(1, (max_page+1)):
            reviews = get_reviews(app_id, page_num)
            writer.writerows(reviews)


if __name__ == '__main__':
    #
    # example run,
    #
    #      pipenv run python fetch_save_to_csv.py 1205990992
    #
    #  or python,
    #
    #      python fetch_save_to_csv.py 1205990992
    #
    #
    app_id = str(sys.argv[1])

    filename = None
    if sys.argv[2] != None or sys.argv[2] != '':
        filename = sys.argv[2]

    get_all_reivews(app_id, filename)
