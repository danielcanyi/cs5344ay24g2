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
        for link in detail_links:
            detail_page_url = link.get("href")
            print("[Scraping] {}".format(detail_page_url))
            filename = _travelerfolio_filename_for_detail_page_url(
                detail_page_url)
            details_page = requests.get(detail_page_url)
            details_page_soup = BeautifulSoup(
                details_page.content, "html.parser")
            _save_scraped_page(
                constants.SITE_NAME_TRAVELERFOLIO, filename, details_page_soup)
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
        for link in detail_links:
            detail_page_url = link.get("href")
            print("[Scraping] {}".format(detail_page_url))
            filename = _travelerfolio_filename_for_detail_page_url(
                detail_page_url)
            details_page = requests.get(detail_page_url)
            details_page_soup = BeautifulSoup(
                details_page.content, "html.parser")
            _save_scraped_page(
                constants.SITE_NAME_THESMARTLOCAL, filename, details_page_soup)
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
        for title in titles:
            link = title.find("a")
            detail_page_url = link.get("href")
            print("[Scraping] {}".format(detail_page_url))
            filename = _alvinology_filename_for_detail_page_url(
                detail_page_url)
            details_page = requests.get(detail_page_url)
            details_page_soup = BeautifulSoup(
                details_page.content, "html.parser")
            _save_scraped_page(
                constants.SITE_NAME_ALVINOLOGY, filename, details_page_soup)
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
        for link in detail_links:
            detail_page_url = link.get("href")
            print("[Scraping] {}".format(detail_page_url))
            filename = _theoccasionaltraveller_filename_for_detail_page_url(
                detail_page_url)
            details_page = requests.get(detail_page_url)
            details_page_soup = BeautifulSoup(
                details_page.content, "html.parser")
            _save_scraped_page(
                constants.SITE_NAME_THEOCCASIONALTRAVELLER,
                filename, details_page_soup)
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
        for link in detail_links:
            detail_page_url = link.get("href")
            print("[Scraping] {}".format(detail_page_url))
            filename = _theworldtravelguy_filename_for_detail_page_url(
                detail_page_url)
            details_page = requests.get(detail_page_url)
            details_page_soup = BeautifulSoup(
                details_page.content, "html.parser")
            _save_scraped_page(
                constants.SITE_NAME_THEWORLDTRAVELGUY,
                filename, details_page_soup)
    print("[Scraping] done for theworldtravelguy")


def _theworldtravelguy_filename_for_detail_page_url(full_url: str) -> str:
    """
    Example url:
        https://theworldtravelguy.com/antelope-canyon-x/
    """
    url_parsed = urllib.parse.urlparse(full_url)
    return url_parsed.path.replace("/", "") + ".html"


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
