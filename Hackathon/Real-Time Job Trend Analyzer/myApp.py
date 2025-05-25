import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import re
from datetime import datetime, timedelta

st.title("📊 Job Market Insights Dashboard")

# Load data directly
@st.cache_data
def load_data():
    return pd.read_csv('data.csv')

df = load_data()

# Search/filter for job titles
# Set of allowed U.S. cities (customize this list)
# ✅ Define allowed U.S. cities
allowed_cities = {
    'new york', 'san francisco', 'chicago', 'los angeles', 'seattle',
    'austin', 'boston', 'dallas', 'atlanta', 'washington'
}

# ✅ Search bar
search_term = st.text_input("🔍 Search by U.S. City or Job Title:").strip().lower()

# ✅ Safe string conversion for search
df['clean_location'] = df['location'].astype(str).str.lower()
df['clean_title'] = df['title'].astype(str).str.lower()

# ✅ Default full data
filtered_df = df.copy()

# ✅ Handle search safely
if search_term:
    try:
        is_title_match = df['clean_title'].str.contains(search_term, na=False, regex=False)
        is_city_match = df['clean_location'].str.contains(search_term, na=False, regex=False)

        is_allowed_city = any(city in search_term for city in allowed_cities)

        if is_title_match.any() or is_city_match.any():
            filtered_df = df[is_title_match | is_city_match]
            st.success(f"✅ Showing {len(filtered_df)} results for: '{search_term}'")
        else:
            if not is_allowed_city:
                st.warning("⚠️ Please search for U.S.-based cities only (e.g., New York, Chicago, San Francisco, etc.)")
            else:
                st.warning("🔍 No matching job postings found.")
            filtered_df = df.iloc[0:0]  # Empty safe DataFrame

    except Exception as e:
        st.warning("⚠️ Something went wrong with the search. Please try a simpler term.")
        filtered_df = df.iloc[0:0]

else:
    st.info(f"📋 Showing all {len(filtered_df)} job postings.")



st.write(f"Showing {len(filtered_df)} job postings matching: '{search_term}'" if search_term else f"Showing all {len(filtered_df)} job postings.")

# 1. Top 5 Most In-Demand Job Titles
st.subheader("1️⃣ Top 5 In-Demand Job Titles")
top_titles = filtered_df['title'].value_counts().nlargest(5)
fig1, ax1 = plt.subplots(figsize=(8, 5))
top_titles.plot(kind='bar', color='skyblue', ax=ax1)
ax1.set_title('Top 5 In-Demand Job Titles')
ax1.set_xlabel('Job Title')
ax1.set_ylabel('Number of Openings')
ax1.tick_params(axis='x', rotation=45)
st.pyplot(fig1)

# 2. Most Frequent Skills Required
st.subheader("2️⃣ Top 10 Most Required Skills")

def clean_skills(skill_str):
    skills = re.findall(r"'(.*?)'", str(skill_str))
    return [s.strip().lower() for s in skills if s.strip()]

all_skills = filtered_df['skills'].dropna().apply(clean_skills).sum()
skill_counts = Counter(all_skills)
top_skills = dict(skill_counts.most_common(10))

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.bar(top_skills.keys(), top_skills.values(), color='orange')
ax2.set_title('Top 10 Most Required Skills')
ax2.set_ylabel('Frequency')
ax2.tick_params(axis='x', rotation=45)
st.pyplot(fig2)

st.subheader("☁️ Skill WordCloud")
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(skill_counts)
fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
ax_wc.imshow(wordcloud, interpolation='bilinear')
ax_wc.axis('off')
st.pyplot(fig_wc)

# 3. Cities with the Highest Number of Openings
st.subheader("3️⃣ Cities with the Most Job Openings")
top_cities = filtered_df['location'].value_counts().nlargest(10)
fig3, ax3 = plt.subplots(figsize=(8, 6))
top_cities.plot(kind='barh', color='green', ax=ax3)
ax3.set_title('Top Cities by Job Openings')
ax3.set_xlabel('Number of Openings')
ax3.set_ylabel('City')
st.pyplot(fig3)

# 4. Posting Trends Over Time
st.subheader("4️⃣ Job Postings Over Time")

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

filtered_df['parsed_date'] = filtered_df['date_posted'].apply(parse_relative_date)
filtered_df = filtered_df.dropna(subset=['parsed_date'])

filtered_df['month'] = filtered_df['parsed_date'].dt.to_period('M')
trend = filtered_df['month'].value_counts().sort_index()

fig4, ax4 = plt.subplots(figsize=(10, 5))
trend.plot(marker='o', linestyle='-', color='purple', ax=ax4)
ax4.set_title('Job Postings Over Time')
ax4.set_xlabel('Month')
ax4.set_ylabel('Number of Postings')
ax4.grid(True)
st.pyplot(fig4)


