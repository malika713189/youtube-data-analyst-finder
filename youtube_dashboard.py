import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load cleaned/tagged data
df = pd.read_csv('short_tagged_youtube_videos.csv')

# App title and description
st.markdown("<h1 style='text-align: center;'>▶️ YouTube Data Analyst Course Finder</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Quickly find top short video tutorials to upskill efficiently!</p>", unsafe_allow_html=True)

# Sidebar filters
search_input = st.sidebar.text_input("🔍 Search for a keyword in title or description", "")
max_duration = st.sidebar.slider("⏳ Max Duration (minutes)", 1, 20, 15)

# Optional category shortcut
category = st.sidebar.radio("🎯 I’m preparing for...", ["All", "Beginner", "Advanced", "Interview Questions"])

# Auto-fill search for beginner/interview/advanced users
if category == "Beginner":
    search_input = "beginner data analyst"
elif category == "Interview Questions":
    search_input = "data analyst interview questions"
elif category == "Advanced":
    search_input = "advanced analytics python tableau powerbi"

# Filter by duration first
filtered = df[df['duration_min'] <= max_duration]

# Load and cache model
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# Smart search and filtering
known_keywords = ['sql', 'excel', 'power bi', 'powerbi', 'tableau', 'python', 'pandas', 'statistics', 'interview', 'portfolio']

if search_input:
    # Compute similarity
    title_embeddings = model.encode(filtered['title'].astype(str).tolist())
    query_embedding = model.encode([search_input])
    filtered['similarity'] = cosine_similarity(query_embedding, title_embeddings)[0]

    # Keyword filter
    keyword_matched = False
    for kw in known_keywords:
        if kw in search_input.lower():
            keyword_matched = True
            filtered = filtered[
                filtered['title'].str.contains(fr"\b{kw}\b", case=False, na=False) |
                filtered['description'].str.contains(fr"\b{kw}\b", case=False, na=False)
            ]
            break

    # Semantic fallback
    if not keyword_matched:
        filtered = filtered[filtered['similarity'] > 0.4]
        filtered = filtered.sort_values(by='similarity', ascending=False)

# Show results
if not filtered.empty:
    st.markdown(f"### ✅ Top videos for '**{search_input or 'All'}**' under **{max_duration} mins**")
    for _, row in filtered.iterrows():
        st.markdown(f"**{row['title']}**")
        st.markdown(f"⏳ {row['duration_min']} min | 👁️ {row['view_count']:,} views | 👍 {row['like_count']:,} likes")
        st.markdown(f"🎯 Skill Focus: `{row['skills_found']}`")
        st.markdown(f"[▶️ Watch on YouTube](https://www.youtube.com/watch?v={row['video_id']})")
        st.markdown("---")
else:
    st.warning("No videos found matching your filters.")

# Bar chart
st.markdown("## 📊 Total Views by Skill (in current filter)")
skill_views = filtered.groupby('skills_found')['view_count'].sum().sort_values(ascending=False)
if not skill_views.empty:
    st.bar_chart(skill_views)
else:
    st.info("No data to show in chart.")
