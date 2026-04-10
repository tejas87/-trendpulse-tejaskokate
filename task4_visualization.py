import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# ================================================
# TrendPulse Task 4 — Visualization with Matplotlib
# Author: Tejas Kokate
# Date: 2026-04-10
# ================================================

print("Starting TrendPulse Task 4 — Creating visualizations...")

# Step 1: Load the analysed CSV from Task 3
if not os.path.exists("data/trends_analysed.csv"):
    raise FileNotFoundError(" data/trends_analysed.csv not found. Please run Task 3 first!")

df = pd.read_csv("data/trends_analysed.csv")
print(f"Loaded {len(df)} stories from data/trends_analysed.csv")

# Create outputs folder
os.makedirs("outputs", exist_ok=True)
print("outputs/ folder ready\n")

# Set style for all charts
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("viridis")

# ====================== CHART 1 ======================
# Top 10 Stories by Score (horizontal bar)
print("Creating Chart 1: Top 10 Stories by Score...")

top10 = df.nlargest(10, 'score').copy()

# Shorten titles longer than 50 characters
top10['short_title'] = top10['title'].apply(
    lambda x: x[:47] + "..." if len(x) > 50 else x
)

plt.figure(figsize=(12, 8))
plt.barh(top10['short_title'], top10['score'], color=sns.color_palette("viridis", 10))
plt.title("Top 10 Stories by Score", fontsize=16, pad=20)
plt.xlabel("Score (Upvotes)")
plt.ylabel("Story Title")
plt.gca().invert_yaxis()  # highest score on top
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png", dpi=300, bbox_inches='tight')
plt.close()  # close figure so next chart is clean
print("   Saved → outputs/chart1_top_stories.png")

# ====================== CHART 2 ======================
# Stories per Category (bar chart)
print("Creating Chart 2: Stories per Category...")

cat_counts = df['category'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
bars = plt.bar(cat_counts.index, cat_counts.values, color=sns.color_palette("Set2", len(cat_counts)))
plt.title("Number of Stories per Category", fontsize=16, pad=20)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.5, f'{int(height)}', ha='center', fontsize=12)
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png", dpi=300, bbox_inches='tight')
plt.close()
print("   Saved → outputs/chart2_categories.png")

# ====================== CHART 3 ======================
# Score vs Comments (scatter plot)
print("Creating Chart 3: Score vs Comments...")

plt.figure(figsize=(10, 7))
colors = ['#1f77b4' if popular else '#ff7f0e' for popular in df['is_popular']]
plt.scatter(df['score'], df['num_comments'], c=colors, alpha=0.7, s=60, edgecolors='w', linewidth=0.5)

# Legend
popular_patch = plt.Line2D([], [], marker='o', color='#1f77b4', label='Popular (score > average)', markersize=8, linestyle='None')
non_popular_patch = plt.Line2D([], [], marker='o', color='#ff7f0e', label='Not Popular', markersize=8, linestyle='None')
plt.legend(handles=[popular_patch, non_popular_patch], loc='upper left')

plt.title("Score vs Number of Comments", fontsize=16, pad=20)
plt.xlabel("Score (Upvotes)")
plt.ylabel("Number of Comments")
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png", dpi=300, bbox_inches='tight')
plt.close()
print("   Saved → outputs/chart3_scatter.png")

# ====================== BONUS DASHBOARD ======================
print("Creating Bonus Dashboard (all 3 charts combined)...")

fig, axes = plt.subplots(2, 2, figsize=(18, 12))
fig.suptitle("TrendPulse Dashboard\nLive HackerNews Trending Stories Analysis", fontsize=20, y=0.98)

# Chart 1 on top-left (full width for better look)
ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)
top10 = df.nlargest(10, 'score').copy()
top10['short_title'] = top10['title'].apply(lambda x: x[:47] + "..." if len(x) > 50 else x)
ax1.barh(top10['short_title'], top10['score'], color=sns.color_palette("viridis", 10))
ax1.set_title("Top 10 Stories by Score")
ax1.set_xlabel("Score")
ax1.invert_yaxis()

# Chart 2 bottom-left
ax2 = plt.subplot2grid((2, 2), (1, 0))
cat_counts = df['category'].value_counts().sort_index()
bars = ax2.bar(cat_counts.index, cat_counts.values, color=sns.color_palette("Set2", len(cat_counts)))
ax2.set_title("Stories per Category")
ax2.set_ylabel("Count")
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, height + 0.3, f'{int(height)}', ha='center')

# Chart 3 bottom-right
ax3 = plt.subplot2grid((2, 2), (1, 1))
colors = ['#1f77b4' if p else '#ff7f0e' for p in df['is_popular']]
ax3.scatter(df['score'], df['num_comments'], c=colors, alpha=0.7, s=60, edgecolors='w')
ax3.set_title("Score vs Comments")
ax3.set_xlabel("Score")
ax3.set_ylabel("Comments")
# Legend
ax3.legend(handles=[popular_patch, non_popular_patch], loc='upper left')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("outputs/dashboard.png", dpi=300, bbox_inches='tight')
plt.close()
print("   Saved → outputs/dashboard.png")

# ====================== FINAL MESSAGE ======================

print("All visualization files saved in the outputs/ folder:")
print("   • chart1_top_stories.png")
print("   • chart2_categories.png")
print("   • chart3_scatter.png")
print("   • dashboard.png  (Bonus)")
