import csv
import os
import time

import click
from selenium import webdriver

from insider.scraper import extract_links_insider, extract_secondary_insider

base_url_insider = 'https://insider.in/all-events-in-'
csv.register_dialect('semicolon-delimited', delimiter = ';')

def extract_info(html, download_folder, city):
    links = extract_links_insider(html)
    titles, genres, addresses, venues, dates, costs, abouts, directions_urls = extract_secondary_insider(links)
    if os.path.exists(download_folder):
        pass
    else:
        os.mkdir('../{}'.format(download_folder))
    with open('../{}/events_insider_{}.csv'.format(download_folder, city), 'w') as f:
        writer = csv.writer(f, dialect = 'semicolon-delimited')
        writer.writerow(['Title', 'Genre', 'Address', 'Venue', 'Date', 'Cost', 'About', 'Directions URL'])
        for i in range(len(titles)):
            writer.writerow([titles[i], genres[i], addresses[i], venues[i], dates[i], costs[i], abouts[i], directions_urls[i]])
    

@click.command()
@click.option('--city', '-c' , default='',help='Enter the City Name in the actual form (Bengaluru not Bangalore)')
@click.option('--browser', '-b', default='chrome', help='Enter the webdriver type (chrome, firefox, safari, etc)')
@click.option('--driver-path', '-dp', default='', help='Enter the path of the webdriver')
@click.option('--download-folder', '-df', default='', help='Enter the path of the download folder')
def main(city, browser, driver_path, download_folder):
    '''Scrape insider.in for events in a city'''
    try:
        url = base_url_insider + str(city) + '?type=physical'
        print('Scraping from: ' + url)
    except Exception as e:
        raise ValueError('Invalid Website Information')
    if (browser == 'chrome' or browser == 'firefox') and not driver_path:
        raise ValueError('Invalid Webdriver Information')
    try:
        if browser == 'chrome' or browser == 'Chrome':
            driver = webdriver.Chrome(executable_path=driver_path)
        elif browser == 'firefox' or browser == 'Firefox':
            driver = webdriver.Firefox(executable_path=driver_path)
        elif browser == 'safari' or browser == 'Safari':
            driver = webdriver.Safari()
    except Exception as e:
        raise ValueError('Invalid Webdriver Information')
    driver.get(url)
    prev_height = driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == prev_height:
            html = driver.page_source
            driver.close()
            extract_info(html, download_folder, city)
            break
        prev_height = new_height


if __name__ == '__main__':
    main()
