# ================================================
# Filename: task1_data_collection.py
# TrendPulse: Task 1 — Fetch Data from HackerNews API
# Author: Tejas Kokate
# Date: 2026-04-07
# ================================================

import requests
import json
import os
from datetime import datetime
import time
from typing import Optional

# Step 1 : Fetch trending stories JSON file from the HackerNews API and categorize them

# Category keywords
CATEGORIES = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

# Function to get the category of a story
def get_category(title: str) -> Optional[str]:
    """Return the first matching category (in priority order) or None."""
    if not title:
        return None
    title_lower = title.lower()
    for cat in CATEGORIES:
        for keyword in CATEGORIES.get(cat, []):
            if keyword.lower() in title_lower:
                return cat
    return None

# Function to fetch a single story from HackerNews API
def fetch_story(story_id: int) -> Optional[dict]:
    """Fetch a single story from HackerNews API with error handling."""
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    headers = {"User-Agent": "TrendPulse/1.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch story {story_id} (HTTP {response.status_code})")
            return None
    except Exception as e:
        print(f"Error fetching story {story_id}: {e}")
        return None

# Main script
print("Starting TrendPulse Task 1 — Fetching live trending stories from HackerNews...")

# Step 1: Get the list of top story IDs (first 500)
topstories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
headers = {"User-Agent": "TrendPulse/1.0"}
try:
    response = requests.get(topstories_url, headers=headers, timeout=10)
    response.raise_for_status()
    top_ids = response.json()[:500]
    print(f"Fetched {len(top_ids)} top story IDs")
    # If a request fails print a message and move on
except Exception as e:
    print(f"Failed to fetch top stories: {e}")
    top_ids = []

if not top_ids:
    print("No story IDs retrieved. Exiting.")
    exit(1)

    # Prepare collection
collected_stories = []
story_index = 0
collected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Step 2: Get each story details and categorize them
print("Collecting up to 100 stories per category (scanning top stories)...\n")

for cat in CATEGORIES:
    count_before = len(collected_stories)
    print(f"Collecting for category: {cat.upper()}")

    while len(collected_stories) - count_before < 100 and story_index < len(top_ids):
        story_id = top_ids[story_index]
        story_index += 1

        story = fetch_story(story_id)
        if not story or "title" not in story or not story["title"]:
            continue

        assigned_cat = get_category(story["title"])

        if assigned_cat == cat:
            story_dict = {
                "post_id": story["id"],
                "title": story["title"],
                "category": cat,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "unknown"),
                "collected_at": collected_at
            }
            collected_stories.append(story_dict)

    print(f"   → Collected {len(collected_stories) - count_before} stories for {cat}")

    # Wait 2 seconds between each category
    time.sleep(2)

# Step 3: Save to JSON in data/ folder
os.makedirs("data", exist_ok=True)
date_str = datetime.now().strftime("%Y%m%d")
filename = f"data/trends_{date_str}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(collected_stories, f, ensure_ascii=False, indent=4)

# Print how many stories were collected
print("\n" + "=" * 60)
print(" TASK 1 COMPLETE!")
print(f"Collected {len(collected_stories)} stories.")
print(f"Saved to {filename}")
print("=" * 60)
print(f"Stories per category: {{ { {cat: len([s for s in collected_stories if s['category'] == cat])} for cat in CATEGORIES } }}")
