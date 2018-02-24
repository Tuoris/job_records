import requests
from bs4 import BeautifulSoup
from .validation import validate_salary


def get_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return


def _extract_first(node):
    return (node or [None])[0]


def m_rabota_info(url):
    content = get_content(url)
    info = {}
    if not content:
        return info

    soup = BeautifulSoup(content, 'html.parser')
    paper_blocks = soup.find_all(class_='paper-block')

    top_block = _extract_first(paper_blocks)
    if top_block:
        salary_block = _extract_first(
            top_block.find_all(class_='salary')
        )
        if salary_block:
            salary = salary_block.text.split()[0]
            info['salary'] = validate_salary(salary)

        title_block = _extract_first(
            top_block.find_all(class_='name')
        )
        if title_block:
            info['job_title'] = title_block.text

    second_block = _extract_first(paper_blocks[1:])
    if second_block:
        company_block = _extract_first(
            second_block.find_all(class_='company-name')
        )
        if company_block:
            info['company'] = company_block.text

    return info
