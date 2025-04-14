"""
Needs html data to first have been scraped

Convert Scraped HTML content into our documents of our own data structure
Refer to `constants` file for data structure
"""
from typing import Tuple
from collections.abc import Iterable
import os
from bs4 import BeautifulSoup
import constants
import json


def convert_alvinology() -> None:
    for (slug, soup) in _read_pages(constants.SITE_NAME_ALVINOLOGY):
        print(
            "[HTML to JSON] {}: {}".format(
                constants.SITE_NAME_ALVINOLOGY, slug))
        title_h1 = soup.find(
            "h1", class_="cs-entry__title")
        title = title_h1.find("span").text
        content_div = soup.find("div", class_="entry-content")
        content = []
        for para in content_div.find_all("p"):
            if para.find("img"):
                img = para.find("img")
                content.append({
                    constants.DOC_CONTENT_ITEM_KEY_TYPE:
                        constants.DOC_CONTENT_ITEM_TYPE_IMG,
                    constants.DOC_CONTENT_ITEM_KEY_SRC: img.get("src")})
            elif para.find("h2"):
                h2 = para.find("h2")
                content.append({
                    constants.DOC_CONTENT_ITEM_KEY_TYPE:
                        constants.DOC_CONTENT_ITEM_TYPE_H2,
                    constants.DOC_CONTENT_ITEM_KEY_TEXT: h2.get_text()})
            elif para.find("h3"):
                h3 = para.find("h3")
                content.append({
                    constants.DOC_CONTENT_ITEM_KEY_TYPE:
                        constants.DOC_CONTENT_ITEM_TYPE_H3,
                    constants.DOC_CONTENT_ITEM_KEY_TEXT: h3.get_text()})
            else:
                content.append({
                    constants.DOC_CONTENT_ITEM_KEY_TYPE:
                        constants.DOC_CONTENT_ITEM_TYPE_TEXT,
                    constants.DOC_CONTENT_ITEM_KEY_TEXT: para.get_text()})
        doc = {
            constants.DOC_KEY_TITLE: title,
            constants.DOC_KEY_CONTENT: content}
        _save_json(constants.SITE_NAME_ALVINOLOGY, slug, doc)

    print("[HTML to JSON] done for alvinology")


def convert_theoccasionaltraveller() -> None:
    for (slug, soup) in _read_pages(
        constants.SITE_NAME_THEOCCASIONALTRAVELLER
    ):
        print(
            "[HTML to JSON] {}: {}".format(
                constants.SITE_NAME_THEOCCASIONALTRAVELLER, slug
            )
        )
        title_h1 = soup.find(
            "h1", class_="entry-title")
        title = title_h1.get_text()
        content_div = soup.find("div", class_="entry-content")
        content = []
        for line in content_div.find_all():
            if line.name == "div":
                if line.find("img"):
                    img = line.find("img")
                    content.append({
                        constants.DOC_CONTENT_ITEM_KEY_TYPE:
                            constants.DOC_CONTENT_ITEM_TYPE_IMG,
                        constants.DOC_CONTENT_ITEM_KEY_SRC: img.get("src")})
                else:
                    continue
            elif line.name == "h2":
                content.append({
                    constants.DOC_CONTENT_ITEM_KEY_TYPE:
                        constants.DOC_CONTENT_ITEM_TYPE_H2,
                    constants.DOC_CONTENT_ITEM_KEY_TEXT: line.get_text()})
            elif line.name == "h3":
                content.append({
                    constants.DOC_CONTENT_ITEM_KEY_TYPE:
                        constants.DOC_CONTENT_ITEM_TYPE_H3,
                    constants.DOC_CONTENT_ITEM_KEY_TEXT: line.get_text()})
            elif line.name == "p":
                content.append({
                    constants.DOC_CONTENT_ITEM_KEY_TYPE:
                        constants.DOC_CONTENT_ITEM_TYPE_TEXT,
                    constants.DOC_CONTENT_ITEM_KEY_TEXT: line.get_text()})
        doc = {
            constants.DOC_KEY_TITLE: title,
            constants.DOC_KEY_CONTENT: content}
        _save_json(
            constants.SITE_NAME_THEOCCASIONALTRAVELLER, slug, doc)

    print("[HTML to JSON] done for theoccasionaltraveller")


def convert_travelerfolio() -> None:
    for (slug, soup) in _read_pages(
        constants.SITE_NAME_TRAVELERFOLIO
    ):
        print(
            "[HTML to JSON] {}: {}".format(
                constants.SITE_NAME_TRAVELERFOLIO, slug
            )
        )
        title_h1 = soup.find(
            "h1", class_="entry-title")
        title = title_h1.get_text()
        content_div = soup.find("div", class_="entry-content")
        content = []
        for line in content_div.find_all():
            if line.name == "figure":
                if line.find("img"):
                    img = line.find("img")
                    content.append({
                        constants.DOC_CONTENT_ITEM_KEY_TYPE:
                            constants.DOC_CONTENT_ITEM_TYPE_IMG,
                        constants.DOC_CONTENT_ITEM_KEY_SRC: img.get("src")})
                else:
                    continue
            elif line.name == "h2":
                content.append({
                    constants.DOC_CONTENT_ITEM_KEY_TYPE:
                        constants.DOC_CONTENT_ITEM_TYPE_H2,
                    constants.DOC_CONTENT_ITEM_KEY_TEXT: line.get_text()})
            elif line.name == "h3":
                content.append({
                    constants.DOC_CONTENT_ITEM_KEY_TYPE:
                        constants.DOC_CONTENT_ITEM_TYPE_H3,
                    constants.DOC_CONTENT_ITEM_KEY_TEXT: line.get_text()})
            elif line.name == "p":
                content.append({
                    constants.DOC_CONTENT_ITEM_KEY_TYPE:
                        constants.DOC_CONTENT_ITEM_TYPE_TEXT,
                    constants.DOC_CONTENT_ITEM_KEY_TEXT: line.get_text()})
        doc = {
            constants.DOC_KEY_TITLE: title,
            constants.DOC_KEY_CONTENT: content}
        _save_json(
            constants.SITE_NAME_TRAVELERFOLIO, slug, doc)

    print("[HTML to JSON] done for travelerfolio")


def convert_thesmartlocal() -> None:
    for (slug, soup) in _read_pages(
        constants.SITE_NAME_THESMARTLOCAL
    ):
        print(
            "[HTML to JSON] {}: {}".format(
                constants.SITE_NAME_THESMARTLOCAL, slug
            )
        )
        title_h1 = soup.find(
            "h1", class_="entry-title")
        title = title_h1.get_text()
        content_div = soup.find("div", {"id": "wtr-content"})
        content = []
        for line in content_div.find_all():
            if line.name == "h2":
                content.append({
                    constants.DOC_CONTENT_ITEM_KEY_TYPE:
                        constants.DOC_CONTENT_ITEM_TYPE_H2,
                    constants.DOC_CONTENT_ITEM_KEY_TEXT: line.get_text()})
            elif line.name == "h3":
                content.append({
                    constants.DOC_CONTENT_ITEM_KEY_TYPE:
                        constants.DOC_CONTENT_ITEM_TYPE_H3,
                    constants.DOC_CONTENT_ITEM_KEY_TEXT: line.get_text()})
            elif line.name == "p":
                if line.find("img"):
                    img = line.find("img")
                    content.append({
                        constants.DOC_CONTENT_ITEM_KEY_TYPE:
                            constants.DOC_CONTENT_ITEM_TYPE_IMG,
                        constants.DOC_CONTENT_ITEM_KEY_SRC: img.get("src")})
                else:
                    content.append({
                        constants.DOC_CONTENT_ITEM_KEY_TYPE:
                            constants.DOC_CONTENT_ITEM_TYPE_TEXT,
                        constants.DOC_CONTENT_ITEM_KEY_TEXT: line.get_text()})
        doc = {
            constants.DOC_KEY_TITLE: title, constants.DOC_KEY_CONTENT: content}
        _save_json(
            constants.SITE_NAME_THESMARTLOCAL, slug, doc)

    print("[HTML to JSON] done for thesmartlocal")


def convert_theworldtravelguy() -> None:
    for (slug, soup) in _read_pages(
        constants.SITE_NAME_THEWORLDTRAVELGUY
    ):
        print(
            "[HTML to JSON] {}: {}".format(
                constants.SITE_NAME_THEWORLDTRAVELGUY, slug
            )
        )
        title_h1 = soup.find(
            "h1", class_="entry-title")
        title = title_h1.get_text()
        content_div = soup.find("div", {"id": "penci-post-entry-inner"})
        content = []
        for line in content_div.find_all():
            if line.name == "h2":
                content.append({
                    constants.DOC_CONTENT_ITEM_KEY_TYPE:
                        constants.DOC_CONTENT_ITEM_TYPE_H2,
                    constants.DOC_CONTENT_ITEM_KEY_TEXT: line.get_text()})
            elif line.name == "div":
                if line.find("img"):
                    img = line.find("img")
                    content.append({
                        constants.DOC_CONTENT_ITEM_KEY_TYPE:
                            constants.DOC_CONTENT_ITEM_TYPE_IMG,
                        constants.DOC_CONTENT_ITEM_KEY_SRC: img.get("src")})
            elif line.name == "p":
                content.append({
                    constants.DOC_CONTENT_ITEM_KEY_TYPE:
                        constants.DOC_CONTENT_ITEM_TYPE_TEXT,
                    constants.DOC_CONTENT_ITEM_KEY_TEXT: line.get_text()})
        doc = {
            constants.DOC_KEY_TITLE: title, constants.DOC_KEY_CONTENT: content}
        _save_json(
            constants.SITE_NAME_THEWORLDTRAVELGUY, slug, doc)

    print("[HTML to JSON] done for theworldtravelguy")


def convert_asiatours() -> None:
    for (slug, soup) in _read_pages(
        constants.SITE_NAME_ASIATOURS
    ):
        print(
            "[HTML to JSON] {}: {}".format(
                constants.SITE_NAME_ASIATOURS, slug
            )
        )
        title_h1 = soup.find("h1")
        title = title_h1.get_text()
        content_div = soup.find("div", {"class": "paragraph"})
        content = []
        for line in content_div.find_all():
            if line.name == "h2":
                content.append({
                    constants.DOC_CONTENT_ITEM_KEY_TYPE:
                        constants.DOC_CONTENT_ITEM_TYPE_H2,
                    constants.DOC_CONTENT_ITEM_KEY_TEXT: line.get_text()})
            elif line.name == "h3":
                if line.find("img"):
                    img = line.find("img")
                    content.append({
                        constants.DOC_CONTENT_ITEM_KEY_TYPE:
                            constants.DOC_CONTENT_ITEM_TYPE_IMG,
                        constants.DOC_CONTENT_ITEM_KEY_SRC: img.get("src")})
            elif line.name == "p":
                content.append({
                    constants.DOC_CONTENT_ITEM_KEY_TYPE:
                        constants.DOC_CONTENT_ITEM_TYPE_TEXT,
                    constants.DOC_CONTENT_ITEM_KEY_TEXT: line.get_text()})
        doc = {
            constants.DOC_KEY_TITLE: title, constants.DOC_KEY_CONTENT: content}
        _save_json(
            constants.SITE_NAME_ASIATOURS, slug, doc)

    print("[HTML to JSON] done for asiatours")


def _read_pages(domain_name: str) -> Iterable[Tuple[str, BeautifulSoup]]:
    """
    Common function
    Will read all in data/html/<domain_name>
    """
    for filename in os.listdir("{}/{}".format(
        constants.DIR_HTML, domain_name
    )):
        yield (
            filename.replace(".html", ""),
            _read_scraped_page(domain_name, filename))


def _read_scraped_page(domain_name: str, filename: str) -> BeautifulSoup:
    """
    Common function
    Will read from data/html/<domain_name>/<filename>
    """
    parent_dir = "{}/{}".format(constants.DIR_HTML, domain_name)
    os.makedirs(parent_dir, exist_ok=True)
    path = "{}/{}".format(parent_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return BeautifulSoup(f, "html.parser")


def _save_json(
    domain_name: str, slug: str, doc: dict
) -> None:
    """
    Common function
    Will save to data/json/<domain_name>/<slug>.json
    """
    parent_dir = "{}/{}".format(constants.DIR_JSON, domain_name)
    os.makedirs(parent_dir, exist_ok=True)
    path = "{}/{}".format(parent_dir, slug + ".json")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(doc))


if __name__ == "__main__":
    # Comment and uncomment
    convert_travelerfolio()
    convert_thesmartlocal()
    convert_alvinology()
    convert_theoccasionaltraveller()
    convert_theworldtravelguy()
    convert_asiatours()
