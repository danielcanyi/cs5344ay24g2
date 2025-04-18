"""
Sites we want to try to scrape:
    - https://travelerfolio.com/
    - https://thesmartlocal.com/
    - https://alvinology.com/
    - https://theoccasionaltraveller.net/
    - https://theworldtravelguy.com/
"""
import requests
import urllib
import os
from bs4 import BeautifulSoup
import constants


def scrape_travelerfolio() -> None:
    URL_BASE = "https://travelerfolio.com/blog/page/"
    for i in range(67):  # 67 listing pages found
        pagenum = i + 1
        listings_page_url = URL_BASE + str(pagenum)
        listings_page = requests.get(listings_page_url)
        listings_page_soup = BeautifulSoup(
            listings_page.content, "html.parser")

        # each listing page has snippets of full articles
        # with a 'Read More' link
        detail_links = listings_page_soup.find_all("a", class_="more-link")
        _scrape_detail_links(
            detail_links=detail_links,
            filename_func=_travelerfolio_filename_for_detail_page_url,
            site_name=constants.SITE_NAME_TRAVELERFOLIO
        )
    print("[Scraping] done for travelerfolio")


def _travelerfolio_filename_for_detail_page_url(full_url: str) -> str:
    """ Example url: https://travelerfolio.com/family-friendly-penang-trip/
    """
    url_parsed = urllib.parse.urlparse(full_url)
    return url_parsed.path.replace("/", "") + ".html"


def scrape_thesmartlocal() -> None:
    URL_BASE = "https://thesmartlocal.com/category/travel/southeast-asia/page/"
    for i in range(67):  # 67 listing pages found
        pagenum = i + 1
        listings_page_url = URL_BASE + str(pagenum)
        listings_page = requests.get(listings_page_url)
        listings_page_soup = BeautifulSoup(
            listings_page.content, "html.parser")
        # each listing page has snippets of full articles
        # with a 'Read More' link
        detail_links = listings_page_soup.find_all(
            "a", class_="link-secondary")

        _scrape_detail_links(
            detail_links=detail_links,
            filename_func=_thesmartlocal_filename_for_detail_page_url,
            site_name=constants.SITE_NAME_THESMARTLOCAL
        )
    print("[Scraping] done for thesmartlocal")


def _thesmartlocal_filename_for_detail_page_url(full_url: str) -> str:
    """ Example url: https://thesmartlocal.com/read/bangkok-to-khao-yai/
    """
    url_parsed = urllib.parse.urlparse(full_url)
    return url_parsed.path.replace("read/", "").replace("/", "") + ".html"


def scrape_alvinology() -> None:
    URL_BASE = "https://alvinology.com/category/all-travel/page/"
    for i in range(208):  # 208 listing pages found
        pagenum = i + 1
        listings_page_url = URL_BASE + str(pagenum)
        listings_page = requests.get(listings_page_url)
        listings_page_soup = BeautifulSoup(
            listings_page.content, "html.parser")

        # the read-more link is a little trickier to find,
        # can't search globally based on class
        # Need to target the content area
        listings_page_content = listings_page_soup.find(
            "div", class_="cs-posts-area cs-posts-area-posts")

        # each listing page has snippets of full articles
        # with a 'Read More' link, they are hidden in the title
        titles = listings_page_content.find_all(
            "h2", class_="cs-entry__title")
        detail_links = [title.find("a") for title in titles]
        _scrape_detail_links(
            detail_links=detail_links,
            filename_func=_alvinology_filename_for_detail_page_url,
            site_name=constants.SITE_NAME_ALVINOLOGY
        )
    print("[Scraping] done for alvinology")


def _alvinology_filename_for_detail_page_url(full_url: str) -> str:
    """
    Example url:
        https://alvinology.com/2024/01/12/royal-caribbeans-icon-of-the\
        -seas-docks-in-miami-a-spectacular-arrival-marks\
        -the-start-of-a-new-vacation-era/
    """
    url_parsed = urllib.parse.urlparse(full_url)
    return url_parsed.path.split("/")[4] + ".html"


def scrape_theoccasionaltraveller() -> None:
    URL_BASE = "https://theoccasionaltraveller.com/blog/page/"
    for i in range(56):  # 56 listing pages found
        pagenum = i + 1
        listings_page_url = URL_BASE + str(pagenum)
        listings_page = requests.get(listings_page_url)
        listings_page_soup = BeautifulSoup(
            listings_page.content, "html.parser")

        # each listing page has snippets of full articles
        # with a 'Read More' link
        detail_links = listings_page_soup.find_all(
            "a", class_="button article-read-more")
        _scrape_detail_links(
            detail_links=detail_links,
            filename_func=_theoccasionaltraveller_filename_for_detail_page_url,
            site_name=constants.SITE_NAME_THEOCCASIONALTRAVELLER
        )
    print("[Scraping] done for theoccasionaltraveller")


def _theoccasionaltraveller_filename_for_detail_page_url(full_url: str) -> str:
    """
    Example url:
        https://theoccasionaltraveller.com/taiwan-tales-5-hualien-taroko-gorge/
    """
    url_parsed = urllib.parse.urlparse(full_url)
    return url_parsed.path.replace("/", "") + ".html"


def scrape_theworldtravelguy() -> None:
    URL_BASE = "https://theworldtravelguy.com/blog/page/"
    for i in range(10):  # 56 listing pages found
        pagenum = i + 1
        listings_page_url = URL_BASE + str(pagenum)
        listings_page = requests.get(listings_page_url)
        listings_page_soup = BeautifulSoup(
            listings_page.content, "html.parser")

        # each listing page has snippets of full articles
        # with a 'Read More' link
        detail_links = listings_page_soup.find_all(
            "a", class_="penci-btn-readmore")
        _scrape_detail_links(
            detail_links=detail_links,
            filename_func=_theworldtravelguy_filename_for_detail_page_url,
            site_name=constants.SITE_NAME_THEWORLDTRAVELGUY
        )
    print("[Scraping] done for theworldtravelguy")


def _theworldtravelguy_filename_for_detail_page_url(full_url: str) -> str:
    """
    Example url:
        https://theworldtravelguy.com/antelope-canyon-x/
    """
    url_parsed = urllib.parse.urlparse(full_url)
    return url_parsed.path.replace("/", "") + ".html"


def scrape_asiatours() -> None:
    URL_BASE = "https://www.asiatours.com/blog/"
    listings_page = requests.get(URL_BASE)
    listings_page_soup = BeautifulSoup(
        listings_page.content, "html.parser")

    # each listing page has snippets of full articles
    # with a 'Read More' link
    detail_links = listings_page_soup.find_all(
        "a", class_="btn-st2")
    _scrape_detail_links(
        detail_links=detail_links,
        filename_func=_asiatours_filename_for_detail_page_url,
        site_name=constants.SITE_NAME_ASIATOURS
    )
    print("[Scraping] done for asiatours")


def _asiatours_filename_for_detail_page_url(full_url: str) -> str:
    """
    Example url:
        https://www.asiatours.com/blog/how-to-get-a-bit-of-everything-in-your-first-asia-tour.html
    """
    url_parsed = urllib.parse.urlparse(full_url)
    return url_parsed.path.replace("blog/", "")


def _scrape_detail_links(detail_links, filename_func, site_name) -> None:
    for link in detail_links:
        detail_page_url = link.get("href")
        print("[Scraping] {}".format(detail_page_url))
        filename = filename_func(
            detail_page_url)
        details_page = requests.get(detail_page_url)
        details_page_soup = BeautifulSoup(
            details_page.content, "html.parser")
        _save_scraped_page(
            site_name,
            filename, details_page_soup)


def _save_scraped_page(
    domain_name: str, filename: str, soup: BeautifulSoup
) -> None:
    """
    Common function
    Will save to data/html/<domain_name>/<filename>
    """
    parent_dir = "{}/{}".format(constants.DIR_HTML, domain_name)
    os.makedirs(parent_dir, exist_ok=True)
    path = "{}/{}".format(parent_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))


if __name__ == "__main__":
    # Comment and uncomment
    scrape_travelerfolio()
    scrape_thesmartlocal()
    scrape_alvinology()
    scrape_theoccasionaltraveller()
    scrape_theworldtravelguy()
    scrape_asiatours()
