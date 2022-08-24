import json
import requests
import time

from bs4 import BeautifulSoup

def extract_links_insider(html):
    base_url = 'https://insider.in/'
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    li = soup.findAll('li', {'class': 'card-list-item'})
    for i in li:
        a_tag = i.find('div', {'data-ref' : 'event_card'})
        link = a_tag.find('a')
        try:
            links.append(base_url + link['href'])
        except Exception as e:
            links.append('UNABLE_TO_EXTRACT')
    
    return links

def extract_secondary_insider(links):
    titles, genres, venues, addresses, dates, costs, abouts, directions_urls= [], [], [], [], [], [], [], []
    #j = 1
    for i in links:
        #print(j)
        #j+=1
        if i == 'UNABLE_TO_EXTRACT':
            continue
        print('Scraping from sub-link: ' + i)
        response = requests.get(i)
        time.sleep(1)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h1', {'data-ref' : 'edp_event_title_desktop'}).text
        genre = soup.find('p', {'data-ref' : 'edp_event_category_desktop'}).text
        price = soup.find('p', {'data-ref' : 'edp_price_string_desktop'}).text
        date = soup.find('p', {'data-ref' : 'edp_event_datestring_desktop'}).text
        about = soup.find('section', {'class' : 'text text-left css-1rmq8t0'}).findAll('p')
        about = [x.text for x in about]
        about = ' '.join(about)
        loc_script = soup.find('script', {'type' : 'application/ld+json'})
        location_info = json.loads(loc_script.text)
        lat, lon = location_info.get('location').get('geo').get('latitude'), location_info.get('location').get('geo').get('longitude')
        directions_url = 'https://www.google.com/maps/dir/?api=1&destination=' + str(lat) + ',' + str(lon)
        venue_name = location_info.get('location').get('name')
        address = location_info.get('location').get('address')
        titles.append(title)
        genres.append(genre)
        venues.append(venue_name)
        dates.append(date)
        costs.append(price)
        abouts.append(about)
        addresses.append(address)
        directions_urls.append(directions_url)
        #print(title, genre, location, date, price, about, directions_url)
    return titles, genres, addresses, venues, dates, costs, abouts, directions_urls
