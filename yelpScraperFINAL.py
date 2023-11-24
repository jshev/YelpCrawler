import re
from bs4 import BeautifulSoup
import requests
import lxml

# code base found here: https://www.scrapingbee.com/blog/web-scraping-yelp/

search_url = "https://www.yelp.com/search/snippet?find_desc=Restaurants&find_loc=Newington%2C+CT%2C+United+States&request_origin=user"
search_response = requests.get(search_url)
search_results = search_response.json()['searchPageProps']['mainContentComponentsListProps']

url_list = []

for result in search_results:
    if result['searchResultLayoutType'] == "iaResult":
        url1 = "https://www.yelp.com" + result['searchResultBusiness']['businessUrl']
        url_list.append(url1)

for url in url_list:
    # print(url)
    
    html = requests.get(url)
    soup = BeautifulSoup(html.text, features="lxml")

    name = soup.find('h1').text
    print(name)

    website_sibling = soup.find('p', string="Business website")
    if website_sibling:
        website = website_sibling.next_sibling.text
        print(website)

    phone_no_sibling = soup.find('p', string="Phone number")
    if phone_no_sibling:
        phone_no = phone_no_sibling.next_sibling.text
        print(phone_no)

    address_sibling = soup.find('a', string="Get Directions")
    if address_sibling:
        address = address_sibling.parent.next_sibling.text
        print(address)

    rating_tag = soup.find('div', attrs={'aria-label': re.compile('star rating')})
    rating = rating_tag['aria-label']
    print(rating)

    review_count = soup.find('span', string=re.compile('reviews')).text
    print(review_count)

    print("--------")
