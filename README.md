# ▶️ YouTube Data Analyst Course Finder
🚀 [Live App on Streamlit](https://youtube-data-analyst-finder-ctjfkbtp4usktsunkftkqn.streamlit.app)

A smart video recommendation tool to help aspiring and current data analysts find **short, high-quality tutorials** across tools like SQL, Excel, Python, Power BI, and more.

![App Screenshot](https://user-images.githubusercontent.com/your-screenshot.png) <!-- Add later if needed -->

---

## Why This Project?

Learning online is hard — too many long, low-quality videos waste your time.  
This app solves that by letting you:

- 🔍 Search tutorials using **semantic keyword matching**
- ⏱️ Filter by video length (e.g. < 15 minutes)
- 📊 See **total views by skill**
- ✅ Explore **latest & relevant** videos only

---

## Features

| Feature               | Description                                      |
|-----------------------|--------------------------------------------------|
| 🔍 Smart Search (NLP) | Uses sentence transformer to match topics        |
| ⏳ Duration Filter    | Choose max video length in minutes               |
| 📊 Views by Skill     | Shows total video views per skill                |
| 🧠 Skill Tagging      | Tags videos with detected skills (SQL, Excel...) |
| ⚡ Fast & Lightweight | Powered by Streamlit & YouTube API               |

---

## Tech Stack

- Python (`requests`, `pandas`, `isodate`)
- Streamlit (dashboard UI)
- YouTube Data API v3 
- Sentence Transformers (semantic search)
- scikit-learn (cosine similarity)

---

## Try the App (Hosted)

Click below to try the live version (hosted via Streamlit Cloud):  
👉 **https://[your-streamlit-link].streamlit.app**

---

## 💻 How to Run Locally

1. Clone this repo:
   ```bash
   git clone https://github.com/your-username/youtube-data-analyst-finder.git
   cd youtube-data-analyst-finder
   ```
2. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the Streamlit app:
    ```bash
    streamlit run youtube_dashboard.py
    ```
    
4. Refresh YouTube video data:
    ```bash
    python fetch_youtube_videos.py
    ```
