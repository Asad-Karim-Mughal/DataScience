import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import re
from datetime import datetime, timedelta

# Load data
df = pd.read_csv('data.csv')

# ================================
# 1. Top 5 Most In-Demand Job Titles
# ================================
top_titles = df['title'].value_counts().nlargest(5)
plt.figure(figsize=(8, 5))
top_titles.plot(kind='bar', color='skyblue')
plt.title('Top 5 In-Demand Job Titles')
plt.xlabel('Job Title')
plt.ylabel('Number of Openings')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ================================
# 2. Most Frequent Skills Required
# ================================
# Clean skill strings and extract as list
def clean_skills(skill_str):
    skills = re.findall(r"'(.*?)'", str(skill_str))
    return [s.strip().lower() for s in skills if s.strip()]

all_skills = df['skills'].dropna().apply(clean_skills).sum()
skill_counts = Counter(all_skills)
top_skills = dict(skill_counts.most_common(10))

# Bar plot for skills
plt.figure(figsize=(10, 5))
plt.bar(top_skills.keys(), top_skills.values(), color='orange')
plt.title('Top 10 Most Required Skills')
plt.xticks(rotation=45)
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# WordCloud (optional)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(skill_counts)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Most Frequent Skills (WordCloud)')
plt.show()

# ================================
# 3. Cities with the Highest Number of Openings
# ================================
top_cities = df['location'].value_counts().nlargest(10)
plt.figure(figsize=(8, 6))
top_cities.plot(kind='barh', color='green')
plt.title('Top Cities by Job Openings')
plt.xlabel('Number of Openings')
plt.ylabel('City')
plt.tight_layout()
plt.show()

# ================================
# 4. Posting Trends Over Time
# ================================
# Convert relative time like "3 days ago" to actual dates
def parse_relative_date(text):
    text = str(text).lower()
    today = datetime.today()
    if "day" in text:
        days = int(re.search(r'(\d+)', text).group(1))
        return today - timedelta(days=days)
    elif "week" in text:
        weeks = int(re.search(r'(\d+)', text).group(1))
        return today - timedelta(weeks=weeks)
    elif "month" in text:
        months = int(re.search(r'(\d+)', text).group(1))
        return today - timedelta(days=30*months)
    else:
        return None

df['parsed_date'] = df['date_posted'].apply(parse_relative_date)
df = df.dropna(subset=['parsed_date'])

# Group by month
df['month'] = df['parsed_date'].dt.to_period('M')
trend = df['month'].value_counts().sort_index()

plt.figure(figsize=(10, 5))
trend.plot(marker='o', linestyle='-', color='purple')
plt.title('Job Postings Over Time')
plt.xlabel('Month')
plt.ylabel('Number of Postings')
plt.grid(True)
plt.tight_layout()
plt.show()
