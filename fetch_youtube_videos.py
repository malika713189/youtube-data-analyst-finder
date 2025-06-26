import requests, pandas as pd, isodate, time

# Replace with your actual API key
API_KEY = 'AIzaSyCucQDSqePWYIxH1fq9g-ATGrD0kdvw6C0'  

# Keywords for ALL major data analyst skills
SEARCH_TERMS = [
    "SQL for data analysts", "CTE SQL tutorial", "window functions SQL", "joins SQL", "group by SQL",
    "subqueries SQL", "case statement SQL", "SQL interview questions", "advanced SQL",
    "Excel for data analysis", "pivot tables Excel", "vlookup Excel", "formulas Excel", "Excel dashboard tutorial",
    "Power BI for beginners", "Power BI dashboard tutorial", "Power BI interview questions",
    "Tableau for data analysts", "Tableau dashboard tutorial", "Tableau calculated fields",
    "Python for data analysts", "pandas tutorial", "data cleaning pandas", "numpy for data analysis", "matplotlib tutorial",
    "EDA in Python", "exploratory data analysis Python", "data visualization in seaborn", "statistics for data analysts",
    "probability for data analysts", "hypothesis testing data analyst",
    "data analyst portfolio project", "data analyst case study", "data analyst interview preparation",
    "business intelligence tutorial", "dashboarding tutorial", "data storytelling for analysts"
]

def get_video_ids(query, max_results=25):
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'q': query,
        'maxResults': max_results,
        'type': 'video',
        'videoDuration': 'any',
        'key': API_KEY
    }
    r = requests.get(url, params=params).json()
    return [item['id']['videoId'] for item in r.get('items', [])]

def get_video_details(video_ids):
    url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part': 'snippet,contentDetails,statistics',
        'id': ','.join(video_ids),
        'key': API_KEY
    }
    r = requests.get(url, params=params).json()
    videos = []

    skill_keywords = {
        'SQL': ['sql', 'cte', 'joins', 'window function', 'subquery'],
        'Excel': ['excel', 'vlookup', 'pivot table', 'spreadsheet'],
        'Power BI': ['power bi'],
        'Tableau': ['tableau'],
        'Python': ['python', 'pandas', 'numpy', 'matplotlib', 'seaborn'],
        'Statistics': ['statistics', 'probability', 'hypothesis testing'],
        'Interview': ['interview', 'interview questions'],
        'Portfolio': ['portfolio', 'case study', 'project'],
        'BI Tools': ['dashboard', 'business intelligence', 'data storytelling']
    }

    for item in r.get('items', []):
        try:
            title = item['snippet']['title'].lower()
            desc = item['snippet'].get('description', '').lower()
            duration = isodate.parse_duration(item['contentDetails']['duration']).total_seconds() / 60

            matched_skills = [skill for skill, keywords in skill_keywords.items()
                              if any(kw in title or kw in desc for kw in keywords)]
            skills_found = ', '.join(matched_skills) if matched_skills else 'Other'

            videos.append({
                'video_id': item['id'],
                'title': item['snippet']['title'],
                'description': item['snippet'].get('description', ''),
                'published_at': item['snippet']['publishedAt'],
                'duration_min': round(duration, 2),
                'view_count': int(item['statistics'].get('viewCount', 0)),
                'like_count': int(item['statistics'].get('likeCount', 0)),
                'skills_found': skills_found
            })
        except:
            continue

    return videos

# Loop over all search terms
all_videos = []
for term in SEARCH_TERMS:
    print(f"Fetching for: {term}")
    ids = get_video_ids(term)
    if ids:
        all_videos.extend(get_video_details(ids))
    time.sleep(1)  # avoid hitting quota too fast

# Remove duplicates and save to CSV
df = pd.DataFrame(all_videos).drop_duplicates(subset='video_id')
df.to_csv('short_tagged_youtube_videos.csv', index=False)
print(f"\n✅ Done! Saved {len(df)} videos to 'short_tagged_youtube_videos.csv'")
