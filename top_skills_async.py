import asyncio
import itertools as it
import time
from typing import Counter

import aiohttp
import requests
from prettytable import PrettyTable

HOME_URL = "https://api.hh.ru/vacancies"
VACANCY_URL = "https://api.hh.ru/vacancies/"


def timer(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        run_time = round(end - start, 3)
        print(f"Script runs in {run_time} seconds")

    return wrapper


def collect_vacancy_urls(searched_job):
    payload = {"text": searched_job, "page": 1, "per_page": 100}
    response = requests.get(HOME_URL, params=payload)
    vacancies = response.json().get("items")
    return [VACANCY_URL + v["id"] for v in vacancies]


def show_skills_frequencies(all_skills):
    skill_freqs = Counter(all_skills).most_common(15)
    table = PrettyTable(field_names=["skill", "frequency"], title="Top Skills")
    table.add_rows([[skill, frequency] for skill, frequency in skill_freqs])
    print(table)


async def extract_vacancy_skills(vacancy_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(vacancy_url) as response:
            vacancy_data = await response.json()
            # print(vacancy_data["key_skills"])
            skills = vacancy_data["key_skills"]
            return [skill.get("name") for skill in skills]


async def make_extract_skill_tasks(vacancy_urls):
    tasks = [asyncio.create_task(extract_vacancy_skills(url)) for url in vacancy_urls]
    result = await asyncio.gather(*tasks)
    return result

@timer
def show_stats(searched_job):
    urls = collect_vacancy_urls(searched_job)
    loop = asyncio.get_event_loop()
    skills = loop.run_until_complete(make_extract_skill_tasks(urls))
    show_skills_frequencies(list(it.chain(*skills)))


if __name__ == "__main__":
    job = input("Enter your job: ")
    print('I am analyzing ...')
    show_stats(job)