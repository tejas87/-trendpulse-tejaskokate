import pandas as pd
import glob
import os
from datetime import datetime

# ================================================
# TrendPulse Task 2 — Data Processing & Cleaning
# Author: Tejas Kokate
# Date: 2026-04-10
# ================================================

print("Starting TrendPulse Task 2 — Cleaning HackerNews data...")

# Step 1: Find and load the latest JSON file from Task 1
json_files = glob.glob("data/trends_*.json")

if not json_files:
    raise FileNotFoundError(" No trends_*.json file found in data/ folder")

# Get the most recent file (newest by filename date)
latest_json = max(json_files, key=os.path.getctime)
print(f" Loading latest file: {latest_json}")

df = pd.read_json(latest_json)

print(f"Loaded {len(df)} stories from {latest_json}\n")

# Step 2: Clean the data

# 2.1 Remove duplicates based on post_id
df = df.drop_duplicates(subset=['post_id'])
print(f"After removing duplicates: {len(df)}")

# 2.2 Drop rows where post_id, title, or score is missing
df = df.dropna(subset=['post_id', 'title', 'score'])
print(f"After removing nulls: {len(df)}")

# 2.3 Convert score and num_comments to integers
df['score'] = df['score'].astype(int)
df['num_comments'] = df['num_comments'].astype(int)

# 2.4 Remove low-quality stories (score < 5)
df = df[df['score'] >= 5]
print(f"After removing low scores: {len(df)}")

# 2.5 Clean whitespace in title
df['title'] = df['title'].str.strip()

# Step 3: Save cleaned data as CSV
os.makedirs("data", exist_ok=True)
clean_file = "data/trends_clean.csv"
df.to_csv(clean_file, index=False, encoding='utf-8')

print(f"\nSaved {len(df)} rows to {clean_file}")

# Final summary: stories per category
print("\nStories per category:")
print(df['category'].value_counts().sort_index())
