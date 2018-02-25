import requests
from bs4 import BeautifulSoup
from .validation import validate_salary


def get_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
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


def work_ua_info(url):
    content = get_content(url)
    info = {}
    if not content:
        return info

    soup = BeautifulSoup(content, 'html.parser')

    title_block = soup.find(id='h1-name')
    if title_block:
        info['job_title'] = title_block.text

    salary_block = soup.find('h3')
    if salary_block:
        salary = salary_block.text.split()[0]
        info['salary'] = validate_salary(salary)

    company_block = soup.find('dd').find('a')
    if company_block:
        info['company'] = company_block.text

    return info
