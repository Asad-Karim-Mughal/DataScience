import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter
import re
from datetime import datetime
import time


# Headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_indeed(search_term="software engineer", location="United States", max_jobs=50):
    """Scrape job listings from Indeed."""
    jobs = []
    base_url = "https://www.indeed.com/jobs"
    params = {'q': search_term, 'l': location, 'sort': 'date'}
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        job_cards = soup.find_all('div', class_='job_seen_beacon')[:max_jobs]
        for card in job_cards:
            try:
                title = card.find('h2', class_='jobTitle').text.strip() if card.find('h2', class_='jobTitle') else 'N/A'
                company = card.find('span', class_='companyName').text.strip() if card.find('span', class_='companyName') else 'N/A'
                location = card.find('div', class_='companyLocation').text.strip() if card.find('div', class_='companyLocation') else 'N/A'
                date_posted = card.find('span', class_='date').text.strip() if card.find('span', class_='date') else 'N/A'

                # Get job description for skills
                job_link = card.find('a', class_='jcs-JobTitle')['href']
                full_link = f"https://www.indeed.com{job_link}"
                job_response = requests.get(full_link, headers=headers)
                job_soup = BeautifulSoup(job_response.text, 'html.parser')
                description = job_soup.find('div', id='jobDescriptionText').text.strip() if job_soup.find('div', id='jobDescriptionText') else ''

                skills = extract_skills(description)

                jobs.append({
                    'title': title,
                    'company': company,
                    'location': location,
                    'skills': skills,
                    'date_posted': date_posted,
                    'source': 'Indeed'
                })
            except Exception as e:
                print(f"Error scraping Indeed job card: {e}")
            time.sleep(1)  # Be polite

        return jobs
    except Exception as e:
        print(f"Error scraping Indeed: {e}")
        return []

def scrape_linkedin(search_term="software engineer", location="United States", max_jobs=50):
    """Simulated LinkedIn scraper (HTML scraping of LinkedIn is blocked; placeholder)."""
    print("LinkedIn scraping is restricted; skipping...")
    return []

def extract_skills(description):
    """Extract skills from job description using keyword matching."""
    common_skills = [
        'Python', 'Java', 'JavaScript', 'C++', 'SQL', 'HTML', 'CSS', 'React', 'Angular',
        'Node.js', 'AWS', 'Azure', 'Docker', 'Kubernetes', 'Git', 'Linux', 'Agile',
        'Scrum', 'Machine Learning', 'Data Analysis', 'Cloud Computing'
    ]
    skills_found = []
    description = description.lower()
    for skill in common_skills:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', description):
            skills_found.append(skill)
    return skills_found

def analyze_jobs(jobs):
    """Analyze scraped job data."""
    df = pd.DataFrame(jobs)
    if df.empty:
        return "No job data to analyze."

    # Trending technologies (skills)
    all_skills = [skill for job in df['skills'] for skill in job]
    skill_counts = Counter(all_skills).most_common(5)

    # Top job roles
    job_titles = df['title'].str.lower().str.replace(r'senior|junior|lead|principal', '', regex=True).str.strip()
    role_counts = Counter(job_titles).most_common(5)

    # Most hiring cities
    cities = df['location'].apply(lambda x: x.split(',')[0].strip() if ',' in x else x).str.strip()
    city_counts = Counter(cities).most_common(5)

    # Summary
    analysis = f"""
Analysis of {len(jobs)} Job Listings (as of {datetime.now().strftime('%Y-%m-%d')}):
    
Top 5 Trending Technologies:
{chr(10).join([f"{skill}: {count} listings" for skill, count in skill_counts])}

Top 5 Job Roles:
{chr(10).join([f"{role}: {count} listings" for role, count in role_counts])}

Top 5 Hiring Cities:
{chr(10).join([f"{city}: {count} listings" for city, count in city_counts])}
"""
    return analysis

def save_to_csv(df, filename):
    df.to_csv(filename, index=False)
    print(f"Saved job listings to {filename}")

def save_to_json(df, filename):
    df.to_json(filename, orient='records', lines=True)
    print(f"Saved job listings to {filename}")

def main():
    print("Scraping Indeed...")
    indeed_jobs = scrape_indeed()
    linkedin_jobs = scrape_linkedin()  # Simulated

    all_jobs = indeed_jobs + linkedin_jobs
    print(f"Total jobs scraped: {len(all_jobs)}")

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    if all_jobs:
        df = pd.DataFrame(all_jobs)
        save_to_csv(df, f'job_listings_{timestamp}.csv')
        save_to_json(df, f'job_listings_{timestamp}.json')

    analysis_result = analyze_jobs(all_jobs)
    print(analysis_result)

if __name__ == "__main__":
    main()

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

# def scrape_rozee_roti(search_term="data analyst", location="Pakistan", max_jobs=20):
#     options = Options()
#     options.add_argument("--headless")  # run headless for speed
#     options.add_argument("--disable-gpu")
#     options.add_argument("--window-size=1920,1080")

#     driver = webdriver.Chrome(options=options)
    
#     # Construct the search URL (verify actual url structure)
#     search_url = f"https://rozee.pk/jobs?q={search_term.replace(' ', '+')}&l={location.replace(' ', '+')}"

#     print(f"Loading page: {search_url}")
#     driver.get(search_url)

#     wait = WebDriverWait(driver, 15)

#     try:
#         # Wait until job cards load (update the selector accordingly)
#         wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job")))

#         jobs = []

#         job_cards = driver.find_elements(By.CSS_SELECTOR, ".job")  # update '.job' selector
#         print(f"Found {len(job_cards)} job cards")

#         for card in job_cards[:max_jobs]:
#             try:
#                 title = card.find_element(By.CSS_SELECTOR, ".job-title").text.strip()
#                 company = card.find_element(By.CSS_SELECTOR, ".company-name").text.strip()
#                 location = card.find_element(By.CSS_SELECTOR, ".location").text.strip()
#                 date_posted = card.find_element(By.CSS_SELECTOR, ".date-posted").text.strip()
#                 link = card.find_element(By.TAG_NAME, "a").get_attribute("href")

#                 jobs.append({
#                     "title": title,
#                     "company": company,
#                     "location": location,
#                     "date_posted": date_posted,
#                     "link": link,
#                     "source": "Rozee Roti"
#                 })
#             except Exception as e:
#                 print(f"Error parsing job card: {e}")

#         return jobs

#     except Exception as e:
#         print(f"Error loading jobs: {e}")
#         return []

#     finally:
#         driver.quit()

# # Example usage
# jobs = scrape_rozee_roti("data analyst", "Pakistan", max_jobs=10)
# print(f"Scraped {len(jobs)} jobs:")
# for job in jobs:
#     print(job)
