import requests
from bs4 import BeautifulSoup
import json

url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

vacancies = []

for vacancy in soup.find_all('div', class_='vacancy-serp-item'):
    title = vacancy.find('a', class_='bloko-link').text

    link = vacancy.find('a', class_='bloko-link')['href']

    company = vacancy.find('a', {
        'data-qa': 'vacancy-serp__vacancy-employer'}).text.strip()

    city = vacancy.find('div', {
        'data-qa': 'vacancy-serp__vacancy-address'}).text.strip()

    salary_tag = vacancy.find('span',
                              {'data-qa': 'vacancy-serp__vacancy-compensation'})
    salary = salary_tag.text.strip() if salary_tag else "Не указана"

    vacancy_response = requests.get(link, headers=headers)
    vacancy_soup = BeautifulSoup(vacancy_response.text, 'html.parser')

    description = vacancy_soup.find('div', {
        'data-qa': 'vacancy-description'}).text.lower()

    if "django" in description and "flask" in description:
        vacancies.append({
            'title': title,
            'link': link,
            'company': company,
            'city': city,
            'salary': salary
        })

with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(vacancies, f, ensure_ascii=False, indent=4)

print(f"Найдено {len(vacancies)} вакансий, соответствующих критериям.")
