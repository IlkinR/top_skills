import time
from typing import Counter
import requests
from prettytable import PrettyTable

HOME_URL = "https://api.hh.ru/vacancies"
VACANCY_URL = "https://api.hh.ru/vacancies/"


def main():
    # 1. Collect all vacancy urls
    payload = {"text": "Python", "page": 1, "per_page": 100}
    response = requests.get(HOME_URL, params=payload)
    vacancies = response.json().get("items")
    vacancies_urls = [VACANCY_URL + v["id"] for v in vacancies]

    # 2. Extract key skills from 1
    all_skills = []

    for pos, vacancy_url in enumerate(vacancies_urls, 1):
        vacancy_response = requests.get(vacancy_url)
        skills_list = vacancy_response.json().get("key_skills")
        skills = [skill.get("name") for skill in skills_list]
        all_skills += skills
        print(f"{pos}) {vacancy_url} --- {skills}")

    # 3. Find most frequent ones
    skill_freqs = Counter(all_skills).most_common(15)
    table = PrettyTable(field_names=["skill", "frequency"], title="Top Skills")
    table.add_rows([[skill, frequency] for skill, frequency in skill_freqs])
    print(table)


start = time.perf_counter()
main()
end = time.perf_counter()
run_time = end - start
print(f"Script runs in {run_time} seconds")
