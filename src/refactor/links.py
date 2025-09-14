import datetime
from datetime import date
from typing import List, Tuple

from bs4 import BeautifulSoup

'''
def parse_page_links(html: str, start_date: date, end_date: date):
    """
    Парсит ссылки на бюллетени с одной страницы:
    <a class="accordeon-inner__item-title link xls" href="/upload/reports/oil_xls/oil_xls_20240101_test.xls">link1</a>
    """
    results = []
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="accordeon-inner__item-title link xls")

    for link in links:
        href = link.get("href")
        if not href:
            continue

        href = href.split("?")[0]
        if "/upload/reports/oil_xls/oil_xls_" not in href or not href.endswith(".xls"):
            continue

        try:
            date = href.split("oil_xls_")[1][:8]
            file = datetime.datetime.strptime(date, "%Y%m%d").date()
            if start_date <= file <= end_date:
                u = href if href.startswith("http") else f"https://spimex.com{href}"
                results.append((u, file))
            else:
                print(f"Ссылка {href} вне диапазона дат")
        except Exception as e:
            print(f"Не удалось извлечь дату из ссылки {href}: {e}")

    return results
'''


class PageLinkParser:
    # TODO: Создать настройки проекта и вынести туда
    BASE_URL = "https://spimex.com"

    def __init__(self, start_date: date, end_date: date):
        self.start_date = start_date
        self.end_date = end_date

    def valid_report_link(self, href: str) -> bool:
        if not href:
            return False
        href = href.split("?")[0]
        return href.startswith('upload/reports/oil_xls/oil_xls_') and href.endswith('.xls')

    def extract_date_from_href(self, href: str) -> date | None:
        try:
            date = href.split("oil_xls_")[1][:8]
            return datetime.datetime.strptime(date, "%Y%m%d").date()
        except Exception as e:
            # TODO: Можно добавить логи
            print(f'Не удалось извлечь дату из ссылки {href}: {e}')
            return None

    def parse(self, html: str, url: str = BASE_URL) -> List[Tuple[str, date]]:
        results: List[Tuple[str, date]] = []
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("a", class_="accordeon-inner__item-title link xls")
        for link in links:
            href = link.get("href")
            if not self.valid_report_link(href):
                continue
            file_date = self.extract_date_from_href(href)
            if not file_date:
                continue
            if self.start_date <= file_date <= self.end_date:
                full_url = href if href.startswith('http') else f'{url}{href}'
                results.append((full_url, file_date))
            else:
                # TODO: Можно добавить логи
                print(f'Ссылка {href} вне диапазона дат!')
        return results
