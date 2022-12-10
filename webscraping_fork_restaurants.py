# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 16:56:20 2022
Requirement: Data Collection Case Study
@author: preethievelyn
"""

from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json


def request_parser(url):
    """ Function to make a request using selenium and then grab the html and convert it into a soup object BeautifulSoup's lxml parser. """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(20)
    html_text = driver.page_source
    soup = BeautifulSoup(html_text,'lxml')
    driver.close()
    
    return soup

def restaurant_details(soup):
    """Function to get the name and link for each restaurant listed on the page. """
    
    restaurant_name = []
    rest_link = []
    for i in soup.find_all('div', attrs = {'class': 'css-fqnmwb elkhwc30'}):
        name = i.get_text()
        link = i.find('a', attrs = {'class':'css-6bxcy ei5oc307'})
        rest_link.append('https://thefork.com'+ link.get('href'))
        
        restaurant_name.append(name)
        
    rest_dict = {'Name': restaurant_name,
                 'Link': rest_link}
        
    restaurant_df = pd.DataFrame(rest_dict)
    restaurant_df.to_csv('resturant_list.csv', index = False)
        
    return restaurant_df

def menu_details(soup):
    """Function to get the name and price for each menu item listed on the page. """
    
    menu_list = []
    for i in soup.find_all('div', attrs = {'class': 'css-1hw493p e11odl1810'}): 
        item_name = i.find('dt', attrs = {'class': 'css-vhto7q e11odl188'})
        item_price = i.find('dd', attrs = {'class': 'css-m5h5s9 e11odl186'})
    
        
        if item_name is not None:
            item_name_final = item_name.get_text()
        else:
            item_name_final = ''
            
        if item_price is not None:
            item_price_final = item_price.get_text()
        else:
            item_price_final = ''
          
        menu_dict = {'name': item_name_final,
                     'price': item_price_final}
        
        menu_list.append(menu_dict)
        
        
    return menu_list

def review_details(soup):
    """Function to get the review text and rating for each customer review listed on the page. """

    reviews_list = []
    rating = soup.find('div', attrs = {'class': 'css-1qlf8lu elkhwc30'}).get_text()
    
    for i in soup.find_all('li', attrs = {'data-test': 'restaurant-page-review-item'}): #'class': 'css-jt9u3f elkhwc30'
        review_text = i.find('div', attrs = {'class': 'css-1q7ojw1 er1i9v62'})
        review_rating = i.find('div', attrs = {'class': 'css-1niwa0b elkhwc30'})
    
        
        if review_text is not None:
            text_final =review_text.get_text()
        else:
            text_final = ''
            
        if review_rating is not None:
            rev_rating_final =review_rating.get_text().replace('/10', '')
        else:
            rev_rating_final = ''
            
        review_dict = {'review_text':text_final,
                       'review_rating': rev_rating_final}
        rating_final = rating.replace('/10', '')
        
        reviews_list.append(review_dict)  
        
    return reviews_list, rating_final
        
def main():
    """Main function 
    1) Makes request using request_parser(url) function , 
    2) Gathers restaurant details using restaurant_details(soup) function"""
    
    url = 'https://www.thefork.com/search?cityId=415144'
    s = request_parser(url)
    restaurant_df = restaurant_details(s)
    
    name_list = restaurant_df['Name'].to_list()
    link_list = restaurant_df['Link'].to_list()

    rest = {}
    for key, value in zip(name_list, link_list):
        rest[key] = value
    
    final_restaurant_list = []
    
    print(rest.items())
    
    for name, link in rest.items():
        print(f'Name:{name}, URL: {link}')
        # Fetching menu details
        url = link + '/menu'
        s = request_parser(url)
        menu = menu_details(s)
        
        # Fetching reviews
        url = link + '/reviews'
        s = request_parser(url)
        reviews, avg_rating = review_details(s)
        
        restaurant_dict = {'restaurant_name':name,
                           'menu_items': menu,
                           'rating': avg_rating,
                           'reviews': reviews
                           }
        
        final_restaurant_list.append(restaurant_dict)
        
    
    jsonString = json.dumps(final_restaurant_list)
 
    # Writing to json file
    with open("restaurant.json", "w") as outfile:
        outfile.write(jsonString)
        
    
    
if __name__ == '__main__':
    main()
        