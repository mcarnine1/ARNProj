import string
from urllib.request import Request
from urllib.request import urlopen
from lxml import etree
import re
# Get beautifulsoup4 with: pip install beautifulsoup4
import bs4

arn_json_output = {}
protocol = "http://"
url = "bgp.he.net"
path = "/report/world"
xpath_id = "//tbody/tr[1]/td[1]"
xpath_name = "//tbody/tr[1]/td[2]"
xpath_v4_routes = "//tbody/tr[1]/td[4]"
xpath_v6_routes = "//tbody/tr[1]/td[6]"


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


def get_asn_ids_for_country(country_url, soup):
    dom = etree.HTML(str(soup))
    links = dom.xpath('//*[@id="asns"]/tbody/tr/td/a["href"]')

    return links


def get_arn_name(country_url, soup):
    dom = etree.HTML(str(soup))
    if dom.xpath(xpath_name)[0].text:
        return dom.xpath(xpath_name)[0].text
    else:
        return "none"


def get_arn_id(country_url, soup):
    dom = etree.HTML(str(soup))
    if dom.xpath(xpath_id)[0].text:
        return dom.xpath(xpath_id)[0].text
    else:
        return "none"

def get_arn_v4_routes(country_url, soup):
    dom = etree.HTML(str(soup))
    if dom.xpath(xpath_v4_routes)[0].text:
        return dom.xpath(xpath_v4_routes)[0].text
    else:
        return "none"

def get_arn_v6_routes(country_url, soup):
    dom = etree.HTML(str(soup))
    if dom.xpath(xpath_v6_routes)[0].text:
        return dom.xpath(xpath_v6_routes)[0].text
    else:
        return "none"


fullurl = protocol + url + path
this_soup = url_to_soup(fullurl)

# paths for all countries
# this_links = []
this_links = get_countries_as_array(this_soup)

for i in this_links:
    print(i)
    fullurl = protocol + url + i
    this_soup = url_to_soup(fullurl)
    arn_name = get_arn_name(fullurl, this_soup)
    arn_id = get_arn_id(fullurl, this_soup)
    arn_route_v4 = get_arn_v4_routes(fullurl, this_soup)
    arn_route_v6 = get_arn_v6_routes(fullurl, this_soup)

    print(arn_name)
    print(arn_id)
    print(arn_route_v4)
    print(arn_route_v6)

    print("----------------------------------------------------")
