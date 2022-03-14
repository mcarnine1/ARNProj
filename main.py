from urllib.request import Request
from urllib.request import urlopen
from lxml import etree
import bs4
import json

# arn_json_output = {}
protocol = "http://"
url = "bgp.he.net"
path = "/report/world"


def url_to_soup(_url):
    req = ""
    html = ""
    soup = ""

    try:
        req = Request(_url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        soup = bs4.BeautifulSoup(html, features="html.parser")
    except TypeError:
        return "null"

    return soup


def get_country_name(soup):
    _country_name = ""
    try:
        dom = etree.HTML(str(soup))
        _country_name = dom.xpath("//*[@id='header']/h1/a")[0].text
    except TypeError:
        _country_name = "TypeError"
    finally:
        return _country_name


def get_countries_as_array(soup):
    links = []
    for a in soup.findAll('a', href=True):
        try:
            thislink = a.attrs['href']
            if thislink.startswith('/country'):
                links.append(thislink)
        except TypeError:
            links.append("TypeError")
    return links


def get_arn_names_as_array(soup):
    x_path = f"//table/tbody/tr/td[2]"
    dom = etree.HTML(str(soup))
    links = dom.xpath(x_path)
    text_links = []
    for link in links:
        text_links.append(link.text)

    return text_links


def get_arn_ids_as_array(soup):
    text_links = []
    x_path = f"//*[@id='asns']/tbody/tr/td[1]/a"
    dom = etree.HTML(str(soup))
    links = dom.xpath(x_path)
    for link in links:
        text_links.append(link.text)

    return text_links


def get_arn_v4_as_array(soup):
    text_links = []
    x_path = f"//table/tbody/tr/td[4]"
    dom = etree.HTML(str(soup))
    links = dom.xpath(x_path)

    for link in links:
        text_links.append(link.text)

    return text_links


def get_arn_v6_as_array(soup):
    text_links = []
    x_path = f"//table/tbody/tr/td[6]"
    dom = etree.HTML(str(soup))
    links = dom.xpath(x_path)

    for link in links:
        text_links.append(link.text)

    return text_links


def get_arn_name(x_path, soup):
    _arn_name = ""
    try:
        dom = etree.HTML(str(soup))
        _arn_name = dom.xpath(x_path)[0].text
    except TypeError:
        _arn_name = "TypeError".__str__
    finally:
        return _arn_name


def get_arn_count(soup):
    dom = etree.HTML(str(soup))
    all_elems = dom.xpath("//table/tbody/tr/td[2]")
    return all_elems


def get_arn_id(x_path, country_url, soup):
    arn_id = ""
    try:
        dom = etree.HTML(str(soup))
        arn_id = dom.xpath(x_path)
    except TypeError:
        arn_id = "TypeError"
    finally:
        return arn_id


def get_arn_v4_routes(x_path, soup):
    arn_v4_route = ""
    try:
        dom = etree.HTML(str(soup))
        arn_v4_route = dom.xpath(x_path)[0].text
    except TypeError:
        arn_v4_route = "TypeError"
    finally:
        return arn_v4_route


def get_arn_v6_routes(x_path, soup):
    arn_v6_route = ""
    try:
        dom = etree.HTML(str(soup))
        arn_v6_route = dom.xpath(x_path)[0].text
    except TypeError:
        arn_v6_route = "TypeError"
    finally:
        return arn_v6_route


fullurl = protocol + url + path
this_soup = url_to_soup(fullurl)
this_links = get_countries_as_array(this_soup)
inc = 1

for i in this_links:
    fullurl = protocol + url + i
    this_soup = url_to_soup(fullurl)
    country_name = get_country_name(this_soup)
    xpath_arn_count = get_arn_count(this_soup)
    arr_arn_names = get_arn_names_as_array(this_soup)
    arr_arn_ids = get_arn_ids_as_array(this_soup)
    arr_arn_v4_routes = get_arn_v4_as_array(this_soup)
    arr_arn_v6_routes = get_arn_v6_as_array(this_soup)

    for range_ind in range(len(xpath_arn_count)):
        arn_json_output = {
            country_name: [
                {
                    "id": arr_arn_ids,
                    "name": arr_arn_names,
                    "v4_routes": arr_arn_v4_routes,
                    "v6_routes": arr_arn_v6_routes
                }
            ]
        }

    print(arn_json_output)
    inc = inc + 1

