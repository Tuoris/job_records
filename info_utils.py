import re
import requests
from bs4 import BeautifulSoup
from validation import validate_salary


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

    title_block = soup.select_one('h1')
    if title_block:
        info['job_title'] = title_block.text

    company_block = soup.select_one('a[href*="/company/view"] span')
    if company_block:
        info['company'] = company_block.text

    salary_block = soup.select_one('div[class*="leading-20"]')
    if salary_block:
        salary, _, currency = salary_block.text.partition(' ')
        if salary:
            info['salary'] = validate_salary(salary)

    return info


def rabota_info(url):
    content = get_content(url)
    info = {}
    if not content:
        return info

    soup = BeautifulSoup(content, 'html.parser')

    title_block = soup.select_one('h1')
    if title_block:
        info['job_title'] = title_block.text

    company_block = soup.select_one('title')
    if company_block:
        company_names = re.findall(r'\-\s(.*)\s\|', company_block.text)
        if company_names:
            info['company'] = company_names[0]

    salary_block = soup.select_one('.vacancy-ssr-holder h4')
    if salary_block:
        salary, _, currency = salary_block.text.partition(' ')
        if salary:
            info['salary'] = validate_salary(salary)

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

    salary_block = soup.select_one('b.text-black')
    if salary_block:
        salary = salary_block.text.replace('\u202f', '').split()[0]
        info['salary'] = validate_salary(salary)

    company_block = soup.select_one('p.text-indent a[href*="/jobs/"]')
    if company_block:
        info['company'] = company_block.text

    return info


def jobs_dou_info(url):
    content = get_content(url)
    info = {}
    if not content:
        return info

    soup = BeautifulSoup(content, 'html.parser')

    vacancy_block = soup.find(class_='b-vacancy')
    if vacancy_block:
        company_block = vacancy_block.find('a', class_='')
        if company_block:
            info['company'] = company_block.text

    title_block = soup.find(class_='g-h2')
    if title_block:
        # TODO: Normalize all string data, because job title data from dou.ua
        # contains non-breaking space in random positions
        info['job_title'] = title_block.text

    salary_block = soup.find(class_='salary')
    if salary_block:
        salary_entries = re.findall(r'\d{3,}', salary_block.text)
        if salary_entries:
            salary = salary_entries[0]
            info['salary'] = validate_salary(salary)

    return info
