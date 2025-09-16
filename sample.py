#%%
# =============================================
# Job Listings Scraper + Analysis
# =============================================

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import re
import time
from collections import Counter

# ---------------------------------------------
# Step 1: Define Target URL
# (Example: Indeed India - Data Analyst Jobs)
# ⚠️ Check robots.txt before scraping
# ---------------------------------------------
base_url = "https://in.indeed.com/jobs?q=data+analyst&l=India"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

job_list = []

# ---------------------------------------------
# Step 2: Scrape Multiple Pages
# ---------------------------------------------
for page in range(0, 3):   # scrape 3 pages (can increase)
    print(f"Scraping page {page+1} ...")
    url = base_url + f"&start={page*10}"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    jobs = soup.find_all("div", class_="job_seen_beacon")

    for job in jobs:
        # Job Title
        title = job.find("h2")
        title = title.text.strip() if title else None

        # Company
        company = job.find("span", class_="companyName")
        company = company.text.strip() if company else None

        # Location
        location = job.find("div", class_="companyLocation")
        location = location.text.strip() if location else None

        # Salary
        salary = job.find("div", class_="salary-snippet")
        salary = salary.text.strip() if salary else "Not mentioned"

        # Skills (example: from job snippet text, cleaned with regex)
        summary = job.find("div", class_="job-snippet")
        summary = summary.text.strip() if summary else ""
        # Extract simple skill-like words (python, sql, excel, etc.)
        skills = re.findall(r"(Python|SQL|Excel|Power BI|Tableau|R|ML|AI)", summary, re.IGNORECASE)

        job_list.append({
            "Title": title,
            "Company": company,
            "Location": location,
            "Salary": salary,
            "Skills": [s.lower() for s in skills]
        })

    time.sleep(2)  # polite scraping delay

# ---------------------------------------------
# Step 3: Create DataFrame
# ---------------------------------------------
df = pd.DataFrame(job_list)
print("Total Jobs Scraped:", len(df))
df.head()

#%%
jobs = soup.find_all("a", class_="tapItem")
print("Jobs found:", len(jobs))
for job in jobs:
    # Title
    title_tag = job.find("h2", class_="jobTitle")
    title = title_tag.text.strip() if title_tag else "Not specified"

    # Company
    company_tag = job.find("span", class_="companyName")
    company = company_tag.text.strip() if company_tag else "Not specified"

    # Location
    location_tag = job.find("div", class_="companyLocation")
    location = location_tag.text.strip() if location_tag else "Not specified"

    # Salary
    salary_tag = job.find("div", class_="salary-snippet")
    salary = salary_tag.text.strip() if salary_tag else "Not mentioned"

    # Skills from job snippet
    summary_tag = job.find("div", class_="job-snippet")
    summary = summary_tag.text.strip() if summary_tag else ""
    skills = re.findall(r"(Python|SQL|Excel|Power BI|Tableau|R|ML|AI)", summary, re.IGNORECASE)

    job_list.append({
        "Title": title,
        "Company": company,
        "Location": location,
        "Salary": salary,
        "Skills": [s.lower() for s in skills] if skills else []
    })

#%%
for page in range(0, 3):   # scrape 3 pages
    print(f"Scraping page {page+1} ...")
    url = base_url + f"&start={page*10}"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    jobs = soup.find_all("div", class_="job_seen_beacon")

    for job in jobs:
        # Title
        title_tag = job.find("h2")
        title = title_tag.text.strip() if title_tag else "Not specified"

        # Company
        company_tag = job.find("span", class_="companyName")
        company = company_tag.text.strip() if company_tag else "Not specified"

        # Location
        location_tag = job.find("div", class_="companyLocation")
        location = location_tag.text.strip() if location_tag else "Not specified"

        # Salary
        salary_tag = job.find("div", class_="salary-snippet")
        salary = salary_tag.text.strip() if salary_tag else "Not mentioned"

        # Skills from job snippet
        summary_tag = job.find("div", class_="job-snippet")
        summary = summary_tag.text.strip() if summary_tag else ""
        skills = re.findall(r"(Python|SQL|Excel|Power BI|Tableau|R|ML|AI)", summary, re.IGNORECASE)

        # Always append full record
        job_list.append({
            "Title": title,
            "Company": company,
            "Location": location,
            "Salary": salary,
            "Skills": [s.lower() for s in skills] if skills else []
        })

    time.sleep(2)  # avoid getting blocked

#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import re
from collections import Counter
import matplotlib.pyplot as plt

# Launch browser (make sure you have Chrome + chromedriver installed)
driver = webdriver.Chrome()

# Open Indeed jobs page
driver.get("https://in.indeed.com/jobs?q=data+analyst&l=India")
time.sleep(3)  # wait for JS to load

job_list = []

# Scroll to load more jobs
for _ in range(3):  # scrape 3 scrolls/pages
    jobs = driver.find_elements(By.CLASS_NAME, "tapItem")

    for job in jobs:
        try:
            title = job.find_element(By.CLASS_NAME, "jobTitle").text
        except:
            title = "Not specified"

        try:
            company = job.find_element(By.CLASS_NAME, "companyName").text
        except:
            company = "Not specified"

        try:
            location = job.find_element(By.CLASS_NAME, "companyLocation").text
        except:
            location = "Not specified"

        try:
            salary = job.find_element(By.CLASS_NAME, "salary-snippet").text
        except:
            salary = "Not mentioned"

        try:
            summary = job.find_element(By.CLASS_NAME, "job-snippet").text
            skills = re.findall(r"(Python|SQL|Excel|Power BI|Tableau|R|ML|AI)", summary, re.IGNORECASE)
        except:
            skills = []

        job_list.append({
            "Title": title,
            "Company": company,
            "Location": location,
            "Salary": salary,
            "Skills": [s.lower() for s in skills]
        })

    # go to next page
    try:
        next_btn = driver.find_element(By.XPATH, '//a[@aria-label="Next"]')
        next_btn.click()
        time.sleep(3)
    except:
        break

driver.quit()

# Convert to DataFrame
df = pd.DataFrame(job_list)
print("Total Jobs Scraped:", len(df))
print(df.head())

#%%
for job in jobs:
    try:
        title = job.find_element(By.CSS_SELECTOR, "h2.jobTitle").text
    except:
        title = "Not specified"

    try:
        company = job.find_element(By.CSS_SELECTOR, "span.companyName").text
    except:
        company = "Not specified"

    try:
        location = job.find_element(By.CSS_SELECTOR, "div.companyLocation").text
    except:
        location = "Not specified"

    try:
        salary = job.find_element(By.CSS_SELECTOR, "div.metadata.salary-snippet-container").text
    except:
        salary = "Not mentioned"

    try:
        summary = job.find_element(By.CSS_SELECTOR, "div.job-snippet").text
        skills = re.findall(r"(Python|SQL|Excel|Power BI|Tableau|R|ML|AI)", summary, re.IGNORECASE)
    except:
        skills = []

    job_list.append({
        "Title": title,
        "Company": company,
        "Location": location,
        "Salary": salary,
        "Skills": [s.lower() for s in skills]
    })

#%%
# Convert to DataFrame
df = pd.DataFrame(job_list)

print("✅ Scraping Completed")
print("Total Jobs Scraped:", len(df))
print("\nColumns in DataFrame:", df.columns.tolist())
print("\nSample Data:")
print(df.head(10))

#%%
import matplotlib.pyplot as plt

# Replace missing/blank locations with "Unknown"
df['Location'] = df['Location'].replace("", "Unknown")
df['Location'] = df['Location'].fillna("Unknown")

# Count top 5
top_locations = df['Location'].value_counts().head(5)

print("Top 5 Locations:")
print(top_locations)

# Plot
plt.figure(figsize=(8,5))
top_locations.plot(kind='bar', color='skyblue', edgecolor='black')

plt.title("Top 5 Job Locations")
plt.xlabel("Location")
plt.ylabel("Number of Jobs")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

#%%
