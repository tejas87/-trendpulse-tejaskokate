import pandas as pd
import numpy as np
import os

# ================================================
# TrendPulse Task 3 — Analysis with Pandas & NumPy
# Author: Tejas Kokate
# Date: 2026-04-10
# ================================================

print("Starting TrendPulse Task 3 — Analysis with Pandas & NumPy...")

# Step 1: Load the cleaned CSV from Task 2
if not os.path.exists("data/trends_clean.csv"):
    raise FileNotFoundError(" data/trends_clean.csv not found.")

df = pd.read_csv("data/trends_clean.csv")

print(f"\nLoaded data: {df.shape}")
print("\nFirst 5 rows:")
print(df.head(5))

# Print basic averages
avg_score = df['score'].mean()
avg_comments = df['num_comments'].mean()
print(f"\nAverage score   : {avg_score:,.0f}")
print(f"Average comments: {avg_comments:,.0f}")

# Step 2: Basic Analysis with NumPy
scores = df['score'].to_numpy()          # Convert to NumPy array (required)

print("\n--- NumPy Stats ---")
print(f"Mean score   : {np.mean(scores):,.0f}")
print(f"Median score : {np.median(scores):,.0f}")
print(f"Std deviation: {np.std(scores):,.0f}")
print(f"Max score    : {np.max(scores):,.0f}")
print(f"Min score    : {np.min(scores):,.0f}")

# Category with the most stories
most_common_cat = df['category'].value_counts().idxmax()
most_common_count = df['category'].value_counts().max()
print(f"\nMost stories in: {most_common_cat} ({most_common_count} stories)")

# Story with the most comments
most_commented_idx = df['num_comments'].idxmax()
title = df.loc[most_commented_idx, 'title']
comments = df.loc[most_commented_idx, 'num_comments']
print(f"\nMost commented story: \"{title}\"  — {comments:,} comments")

# Step 3: Add two new columns
df['engagement'] = df['num_comments'] / (df['score'] + 1)          # engagement ratio
df['is_popular'] = df['score'] > df['score'].mean()                # True if above average score

# Step 4: Save the analysed data
os.makedirs("data", exist_ok=True)
analysed_file = "data/trends_analysed.csv"
df.to_csv(analysed_file, index=False)

print(f"\nSaved to {analysed_file}")
