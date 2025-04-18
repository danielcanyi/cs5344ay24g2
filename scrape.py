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
        """
        Example url:
            https://theworldtravelguy.com/antelope-canyon-x/
        """
        _scrape_detail_links(
            detail_links=detail_links,
            filename_func=(
                lambda full_url: urllib.parse.urlparse(
                    full_url).path.replace("/", "") + ".html"
            ),
            site_name=constants.SITE_NAME_THEWORLDTRAVELGUY
        )
    print("[Scraping] done for theworldtravelguy")


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


def scrape_asiakingtravel() -> None:
    URL_BASE = "https://www.asiakingtravel.com/blog/"
    for cty in constants.COUNTRY_NAMES:
        cty_base = URL_BASE + cty + "?page="
        for i in range(10):  # max is 10
            pagenum = i + 1
            listings_page_url = cty_base + str(pagenum)
            listings_page = requests.get(listings_page_url)
            listings_page_soup = BeautifulSoup(
                listings_page.content, "html.parser")

            # each listing page has snippets of full articles
            # with a 'Read More' link
            titles = listings_page_soup.find_all(
                "h4", class_="_title")
            detail_links = [title.find("a") for title in titles]
            """
            Example url:
                https://www.asiakingtravel.com/blog/top-food-spots-saigon-bib-gourmand-suggested.html
            """
            _scrape_detail_links(
                detail_links=detail_links,
                filename_func=(
                    lambda full_url: urllib.parse.urlparse(
                        full_url).path.replace("blog/", "")
                ),
                site_name=constants.SITE_NAME_ASIAKINGTRAVEL
            )
    print("[Scraping] done for asiakingtravel")


def scrape_wanderlush() -> None:
    URL_BASE = "https://wander-lush.org/asia/page/"
    for i in range(21):  # 21 listing pages found
        pagenum = i + 1
        listings_page_url = URL_BASE + str(pagenum)
        listings_page = requests.get(listings_page_url)
        listings_page_soup = BeautifulSoup(
            listings_page.content, "html.parser")

        # each listing page has snippets of full articles
        # with a 'Read More' link
        titles = listings_page_soup.find_all(
            "h2", class_="entry-title")
        detail_links = [title.find("a") for title in titles]
        """
        Example url:
            https://wander-lush.org/best-thai-street-food-khao-soy-mai-sae/
        """
        _scrape_detail_links(
            detail_links=detail_links,
            filename_func=(
                lambda full_url: urllib.parse.urlparse(
                    full_url).path.replace("/", "") + ".html"
            ),
            site_name=constants.SITE_NAME_WANDERLUSH
        )
    print("[Scraping] done for wanderlush")


def scrape_nomadicmatt() -> None:
    URL_BASE = \
        "https://www.nomadicmatt.com/travel-blogs/tag/southeast-asia/page/"
    for i in range(3):
        pagenum = i + 1
        listings_page_url = URL_BASE + str(pagenum)
        listings_page = requests.get(listings_page_url)
        listings_page_soup = BeautifulSoup(
            listings_page.content, "html.parser")

        # each listing page has snippets of full articles
        # with a 'Read More' link
        titles = listings_page_soup.find_all(
            "h2", class_="entry-title")
        detail_links = [title.find("a") for title in titles]
        """
        Example url:
            https://www.nomadicmatt.com/travel-blogs/ko-phi-phi/
        """
        _scrape_detail_links(
            detail_links=detail_links,
            filename_func=(
                lambda full_url: urllib.parse.urlparse(
                    full_url).path.replace("/", "") + ".html"
            ),
            site_name=constants.SITE_NAME_NOMADICMATT
        )
    print("[Scraping] done for nomadicmatt")


def scrape_themarriedwanderers() -> None:
    # NOTE: BLOCKED BY SITE SECURITY
    URL_BASE = \
        "https://www.themarriedwanderers.com/category/countries/asia/page/"
    for i in range(5):
        pagenum = i + 1
        listings_page_url = URL_BASE + str(pagenum)
        print(listings_page_url)
        listings_page = requests.get(listings_page_url)
        listings_page_soup = BeautifulSoup(
            listings_page.content, "html.parser")
        print(listings_page_soup)

        # each listing page has snippets of full articles
        # with a 'Read More' link
        titles = listings_page_soup.find_all(
            "div", class_="read-more")
        print(titles)
        detail_links = [title.find("a") for title in titles]
        print(detail_links)
        """
        Example url:
            https://www.themarriedwanderers.com/2017/01/15/hsipaw-what-to-do-when-youre-not-trekking/
        """
        _scrape_detail_links(
            detail_links=detail_links,
            filename_func=(
                lambda full_url: urllib.parse.urlparse(
                    full_url).path.replace("/", "_") + ".html"
            ),
            site_name=constants.SITE_NAME_THEMARRIEDWANDERERS
        )
    print("[Scraping] done for themarriedwanderers")


def scrape_realisticasia() -> None:
    URL_BASE = \
        "https://realisticasia.com/travel-blogs?page="
    for i in range(5):
        pagenum = i + 1
        listings_page_url = URL_BASE + str(pagenum)
        listings_page = requests.get(listings_page_url)
        listings_page_soup = BeautifulSoup(
            listings_page.content, "html.parser")

        # each listing page has snippets of full articles
        # with a 'Read More' link
        titles = listings_page_soup.find_all(
            "div", class_="post")
        detail_links = [title.find("a") for title in titles]
        """
        Example url:
            https://realisticasia.com/travel-blogs/122-one-day-at-the-kingdom-of-gentle-giants-in-chiangmai
        """
        _scrape_detail_links(
            detail_links=detail_links,
            filename_func=(
                lambda full_url: urllib.parse.urlparse(
                    full_url).path.replace("/", "") + ".html"
            ),
            site_name=constants.SITE_NAME_REALISTICASIA,
            base_url="https://realisticasia.com/"
        )
    print("[Scraping] done for realisticasia")


def scrape_asialegend() -> None:
    URL_BASE = \
        "https://asialegend.travel/blog/page/"
    for i in range(37):
        pagenum = i + 1
        listings_page_url = URL_BASE + str(pagenum)
        listings_page = requests.get(listings_page_url)
        listings_page_soup = BeautifulSoup(
            listings_page.content, "html.parser")

        # each listing page has snippets of full articles
        # with a 'Read More' link
        titles = listings_page_soup.find_all(
            "h2", class_="entry-title")
        detail_links = [title.find("a") for title in titles]
        """
        Example url:
            https://asialegend.travel/7-best-things-to-do-around-west-lake-hanoi/
        """
        _scrape_detail_links(
            detail_links=detail_links,
            filename_func=(
                lambda full_url: urllib.parse.urlparse(
                    full_url).path.replace("/", "") + ".html"
            ),
            site_name=constants.SITE_NAME_ASIALEGEND
        )
    print("[Scraping] done for asialegend")


def scrape_explorient() -> None:
    # NOTE: BLOCKED BY SITE SECURITY
    URL_BASE = \
        "https://www.explorient.com/blog/page/"
    for i in range(8):
        pagenum = i + 1
        listings_page_url = URL_BASE + str(pagenum)
        listings_page = requests.get(listings_page_url)
        listings_page_soup = BeautifulSoup(
            listings_page.content, "html.parser")
        print(listings_page_soup)

        # each listing page has snippets of full articles
        # with a 'Read More' link
        titles = listings_page_soup.find_all(
            "p", class_="read-more")
        detail_links = [title.find("a") for title in titles]
        """
        Example url:
            https://www.explorient.com/blog-singapore-luxury-gateway-to-asia/
        """
        _scrape_detail_links(
            detail_links=detail_links,
            filename_func=(
                lambda full_url: urllib.parse.urlparse(
                    full_url).path.replace("/", "") + ".html"
            ),
            site_name=constants.SITE_NAME_EXPLORIENT
        )
    print("[Scraping] done for explorient")


def scrape_studentuniverse() -> None:
    # NOTE: SCRAPING DISALLOWED - ROBOT CHECKED
    URL_BASE = \
        "https://www.studentuniverse.com/blog/category/destinations/asia/page/"
    for i in range(37):
        pagenum = i + 1
        listings_page_url = URL_BASE + str(pagenum)
        listings_page = requests.get(listings_page_url)
        listings_page_soup = BeautifulSoup(
            listings_page.content, "html.parser")
        print(listings_page_soup)

        # each listing page has snippets of full articles
        # with a 'Read More' link
        titles = listings_page_soup.find_all(
            "h2", class_="entry-title")
        detail_links = [title.find("a") for title in titles]
        """
        Example url:
            https://www.studentuniverse.com/blog/destinations/5-best-destinations-for-women-in-2015
        """
        _scrape_detail_links(
            detail_links=detail_links,
            filename_func=(
                lambda full_url: urllib.parse.urlparse(
                    full_url).path.replace("/", "_") + ".html"
            ),
            site_name=constants.SITE_NAME_STUDENTUNIVERSE
        )
    print("[Scraping] done for studentuniverse")


def _scrape_detail_links(
    detail_links, filename_func, site_name, base_url=""
) -> None:
    for link in detail_links:
        detail_page_url = base_url + link.get("href")
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
    scrape_asiakingtravel()
    scrape_wanderlush()
    scrape_nomadicmatt()
    scrape_realisticasia()
    scrape_asialegend()
