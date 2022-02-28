import string
from urllib.request import Request
from urllib.request import urlopen
import re
# Get beautifulsoup4 with: pip install beautifulsoup4
import bs4


# To help get you started, here is a function to fetch and parse a page.
# Given url, return soup.
def url_to_soup(url):
    # bgp.he.net filters based on user-agent.
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = bs4.BeautifulSoup(html, features="html.parser")
    return soup


def get_countries_as_array(soup):
    links = []
    for a in soup.findAll('a', href=True):
        thislink = a.attrs['href']
        if thislink.startswith('/country'):
            links.append(thislink)

    return links


def get_asn_ids_for_country(country_url):
    print(country_url)


protocol = "http://"
url = "bgp.he.net"
path = "/report/world"

fullurl = protocol + url + path
this_soup = url_to_soup(fullurl)

#paths for all countries
this_links = []
this_links = get_countries_as_array(this_soup)
print(len(this_links))

for i in this_links:
    fullurl = protocol + url + i
    this_soup = url_to_soup(fullurl)
    print(this_soup)

