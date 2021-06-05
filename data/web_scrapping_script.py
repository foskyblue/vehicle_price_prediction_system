from bs4 import BeautifulSoup
import requests
import json
from collections import defaultdict
import numpy as np
import pandas as pd
import progressbar
import time


def fetch_all_url_link(url_increasing_link, n):
    """
        :param url_increasing_link: str, a link with an increasing index, e.g https//:abc.com/cars&page_number=idx
        :param n: int, the maximum number of index
        :return: a list of all the url links from index 1 to n
    """
    url_links_to_crawl = []
    for idx in range(1, n+1):
        # print("Sleeping for 10 seconds...")
        # time.sleep(10)
        url_links_to_crawl.append(url_increasing_link + str(idx))

    return url_links_to_crawl


def fetch_each_webpage_vehicle_urls(webpage_urls_list, url_prefix):
    """
        :param webpage_urls_list: a list of root url links
        :param url_prefix: str, a prefix to be appended to an incomplete vehicle url, e.g https://abc.africa/ng/
        :return: a list of all the url links in each root url
    """
    vehicle_urls = []
    for curr_url in webpage_urls_list:
        soup_obj = get_beautiful_soup_object(curr_url)
        filtered_tags = get_tag_from_soup('a', 'jsx-3456531073 car-item hover:tw-shadow-md', soup_obj) # filter html text by tag
        vehicle_urls.append(get_vehicle_urls(filtered_tags, url_prefix))
    return vehicle_urls


def get_beautiful_soup_object(url_links):
    """
        :param url_links: a url link
        :return: a beautiful soup object
    """
    try:
        html_content = requests.get(url_links).text
        soup = BeautifulSoup(html_content, "html5lib")  # Parse the html content
    except ConnectionError:
        print('A connection error occurred here: ', url_links)

    return soup


def get_vehicle_urls(soup_object, url_prefix):
    """
        :param soup_object: a beautiful soup object
        :param url_prefix: str, a prefix to be appended to an incomplete vehicle url, e.g https://abc.africa/ng/
        :return: a list of prefixed urls
    """
    return [get_vehicle_urls_with_prefix(url_prefix, tag.get("href")[11:]) for tag in soup_object]


def get_vehicle_urls_with_prefix(url_prefix, url_link_):
    """
        :param url_prefix: str, a prefix to be appended to an incomplete vehicle url, e.g https://abc.africa/ng/
        :param url_link_: a url link
        :return: a prefixed url link
    """
    return url_prefix + url_link_


# def get_vehicle_urls_with_prefix(url_prefix, url_list):
#     return [url_prefix+url for url in url_list]


def get_tag_from_soup(tag, class_name, soup_object):
    """
        :param tag: an HTML tag name
        :param class_name: an HTML tag class name
        :param soup_object: a beautiful soup object
        :return: a beautiful soup object with a specific tagged element
    """
    tag_space_search = soup_object.find_all(tag, class_=class_name)
    return tag_space_search


def get_script_tag_from_soup(soup_object):
    """
        :param soup_object: a beautiful soup object
        :return: a json data structure with key-value properties
    """
    script_tags = soup_object.find_all('script', attrs={'type': 'application/json'})  # find script tag elements
    script_tags = script_tags[-1].text  # gets the script tag content in a string format
    product_info_json = json.loads(script_tags, strict=False)  # converts to a dictionary format
    return product_info_json


def print_urls(url_list):
    for url in url_list:
        print(url)


def is_length_complete(normal_keys, special_keys, excluded_keys, vehicle_features_json):
    n = len(normal_keys)
    temp_list = []
    for k, val in vehicle_features_json.items():
        if k in special_keys and k not in excluded_keys:
            if k == 'model':
                try:
                    temp_list.append(vehicle_features_json['model']['name'])
                    temp_list.append(vehicle_features_json['model']['make']['name'])
                except KeyError:
                    print('The key: ', k, ' does not exit in this link.')
            elif k == 'bodyType':
                temp_list.append(vehicle_features_json['bodyType']['name'])
        elif k in normal_keys and k not in excluded_keys:
            temp_list.append(val)
    if len(temp_list) == n:
        return True
    return False


def get_vehicle_features(url_lists):
    """
        :param url_lists -
        :return: training data dataframe, target columns dataframe and target column names
    """

    normal_keys = ['id', 'year', 'insured', 'mileage', 'vin', 'licensePlate', 'price',
                   'createdBy', 'marketplacePrice', 'marketplaceVisible', 'marketplaceVisibleDate', 'model_name',
                   'isFeatured' 'reasonForSelling', 'ownerId', 'state', 'country', 'address', 'carManagerId',
                   'ownerType', 'transmission', 'fuelType', 'sellingCondition', 'city', 'marketplaceOldPrice',
                   'createdAt', 'mileageUnit', 'hasWarranty', 'interiorColor', 'exteriorColor', 'engineType',
                   'gradeScore', 'installment', 'depositReceived', 'isFirstOwner', 'firstOwnerName',
                   'firstOwnerPhone', 'loanValue', 'websiteUrl', 'hasThreeDImage', 'model_brand_name'
                   ]

    special_keys = ['model', 'bodyType']
    vehicle_features = defaultdict(lambda: list())
    excluded_keys = ['features', 'modelFeatures', '', 'carFeatures', 'damageMedia', 'stats']

    n_url_list = len(url_lists)
    counter = 0
    bar = progressbar.ProgressBar(maxval=n_url_list + 1,
                                  widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for curr_url_list in url_lists:
        counter += 1
        print('counter = ', counter)
        # print(bar.update(counter))
        for curr_url in curr_url_list:

            soup_obj = get_beautiful_soup_object(curr_url)  # get beautiful soup object
            product_info_json = get_script_tag_from_soup(soup_obj)

            vehicle_features_json = product_info_json['props']['pageProps']['car']

            if is_length_complete(normal_keys, special_keys, excluded_keys, vehicle_features_json):
                for k, val in vehicle_features_json.items():
                    if k in special_keys and k not in excluded_keys:
                        if k == 'model':
                            try:
                                vehicle_features['model_name'].append(vehicle_features_json['model']['name'])
                                vehicle_features['model_brand_name'].append(vehicle_features_json['model']['make']['name'])
                            except KeyError:
                                print('The key: ', k, ' does not exit in this link.')
                        elif k == 'bodyType':
                            vehicle_features[k].append(vehicle_features_json['bodyType']['name'])
                    elif k in normal_keys and k not in excluded_keys:
                        vehicle_features[k].append(val)
            print(curr_url)
            # df = create_dataframe(vehicle_features)
            # save_to_csv(df)
    bar.finish()
    print('Saving to json...')
    save_to_file(vehicle_features)
    print('Save to json is complete!!!')
    print('Creating a pandas dataframe...')
    df = create_dataframe(vehicle_features)
    print('Data frame has been created successfully!!!')
    print('Saving dataframe to csv...')
    save_to_csv(df, 'trucks')
    print('Saving to csv has been completed!!!')
    return df


def create_dataframe(features_dict):
    """
        :param features_dict: a dictionary with key-value properties
        :return: a Pandas dataframe object
    """
    return pd.DataFrame(features_dict)


def save_to_csv(df, kind="cars"):
    """
        :param df: a Pandas dataframe object
        :param kind: a string to specify if the dataset is of cars or trucks
        :return: bool, success/failure message
    """
    if kind == 'cars':
        pass
    elif kind == 'trucks':
        df.to_csv('trucks.csv', index=False)


def save_to_file(df_dict):
    """
        :param df_dict: a dictionary with key-value properties
        :return: bool, success/failure message
    """
    with open('truck_data.json', 'w') as fp:
        json.dump(df_dict, fp, indent=4)


url_link_prefix = "https://autochek.africa/ng/"

url_link = ['https://autochek.africa/ng/car/toyota-highlander-ref-iHkhKlmQv',
            'https://autochek.africa/ng/car/volkswagen-t4-caravelle-ref--bLz480j-']

# base_link_cars = 'https://autochek.africa/ng/cars-for-sale?country=ng&page_number='
n = 12
base_link = "https://autochek.africa/ng/cars-for-sale/truck?country=ng&page_number="
print("Fetching all top level URL's...")
url_to_cr = fetch_all_url_link(base_link, n)
print("Fetch completed!")
print("Fetching URL's from each top level URL's...")
vehicle_url_list = fetch_each_webpage_vehicle_urls(url_to_cr, url_link_prefix)
print("Fetch completed!")
df_ = get_vehicle_features(vehicle_url_list)


print(df_.head())
