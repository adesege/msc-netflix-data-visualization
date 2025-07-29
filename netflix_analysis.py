import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

plt.style.use('default')
sns.set_palette("husl")
matplotlib.use('Agg')  # Prevents plot windows from opening
plt.ioff()  # Turn off interactive mode

print("Starting Netflix Data Analysis...")
print("=" * 40)

def load_data(filename):
    try:
        df = pd.read_csv(filename)
        print(f"Successfully loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except FileNotFoundError:
        print("Error: Could not find the dataset file!")
        return None

Netflix_shows_movies = load_data('data/Netflix_shows_movies.csv')

if Netflix_shows_movies is not None:
    # Quick look at the data
    print("\nFirst few rows:")
    print(Netflix_shows_movies.head())
    
    print("\nDataset info:")
    print(Netflix_shows_movies.info())

# Handle missing values
print("\n" + "=" * 40)
print("DATA CLEANING SECTION")
print("=" * 40)

print("Missing values before cleaning:")
print(Netflix_shows_movies.isnull().sum())

# Fill missing values - different approach for each column
Netflix_shows_movies['director'].fillna('No Director Listed', inplace=True)
Netflix_shows_movies['cast'].fillna('No Cast Info', inplace=True)
Netflix_shows_movies['country'].fillna('Country Not Specified', inplace=True)
Netflix_shows_movies['date_added'].fillna('Date Unknown', inplace=True)
Netflix_shows_movies['rating'].fillna('Not Rated', inplace=True)

# For duration - fill based on content type
movie_duration = Netflix_shows_movies[Netflix_shows_movies['type'] == 'Movie']['duration'].mode()
if len(movie_duration) > 0:
    Netflix_shows_movies.loc[(Netflix_shows_movies['type'] == 'Movie') & 
                           (Netflix_shows_movies['duration'].isnull()), 'duration'] = movie_duration[0]

tv_duration = Netflix_shows_movies[Netflix_shows_movies['type'] == 'TV Show']['duration'].mode()
if len(tv_duration) > 0:
    Netflix_shows_movies.loc[(Netflix_shows_movies['type'] == 'TV Show') & 
                           (Netflix_shows_movies['duration'].isnull()), 'duration'] = tv_duration[0]

Netflix_shows_movies['duration'].fillna('Duration Unknown', inplace=True)
Netflix_shows_movies['listed_in'].fillna('Genre Not Listed', inplace=True)
Netflix_shows_movies['description'].fillna('No description available', inplace=True)

print("\nMissing values after cleaning:")
print(Netflix_shows_movies.isnull().sum())

print("\n" + "=" * 40)
print("DATA EXPLORATION")
print("=" * 40)

print("Basic dataset statistics:")
print(f"Total number of titles: {len(Netflix_shows_movies)}")

# Content type breakdown
content_types = Netflix_shows_movies['type'].value_counts()
print(f"\nContent breakdown:")
for content_type, count in content_types.items():
    percentage = (count / len(Netflix_shows_movies)) * 100
    print(f"{content_type}: {count} ({percentage:.1f}%)")

# Rating distribution
print(f"\nTop 10 ratings:")
rating_counts = Netflix_shows_movies['rating'].value_counts().head(10)
print(rating_counts)

# Release year stats
print(f"\nRelease year information:")
print(f"Oldest content: {Netflix_shows_movies['release_year'].min()}")
print(f"Newest content: {Netflix_shows_movies['release_year'].max()}")
print(f"Average release year: {Netflix_shows_movies['release_year'].mean():.1f}")

# Country analysis
print(f"\nTop countries (handling multiple countries):")
all_countries = []
for country_list in Netflix_shows_movies['country'].dropna():
    if ',' in str(country_list):
        countries = [c.strip() for c in str(country_list).split(',')]
        all_countries.extend(countries)
    else:
        all_countries.append(str(country_list).strip())

country_counter = Counter(all_countries)
top_countries = country_counter.most_common(10)
for country, count in top_countries:
    print(f"{country}: {count}")

# Visualization 1: Most watched genres (using listed_in as proxy)
print("\n" + "=" * 40)
print("CREATING VISUALIZATIONS")
print("=" * 40)

# Process genres
all_genres = []
for genre_list in Netflix_shows_movies['listed_in'].dropna():
    if ',' in str(genre_list):
        genres = [g.strip() for g in str(genre_list).split(',')]
        all_genres.extend(genres)
    else:
        all_genres.append(str(genre_list).strip())

genre_counter = Counter(all_genres)
top_genres = dict(genre_counter.most_common(15))

# Create genre plot
plt.figure(figsize=(12, 8))
genres = list(top_genres.keys())
counts = list(top_genres.values())

# Horizontal bar plot
bars = plt.barh(genres, counts)
plt.title('Top 15 Most Common Genres on Netflix', fontsize=14, fontweight='bold')
plt.xlabel('Number of Titles')
plt.ylabel('Genres')

# Add numbers on bars
for i, (bar, count) in enumerate(zip(bars, counts)):
    plt.text(count + 10, i, str(count), va='center')

plt.tight_layout()
plt.savefig('charts/netflix_genres_chart.png', dpi=300, bbox_inches='tight')
plt.close()

print("Genre visualization created and saved!")

# Visualization 2: Ratings distribution
rating_data = Netflix_shows_movies['rating'].value_counts()

# Create subplot with bar chart and pie chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Bar chart
ax1.bar(rating_data.index, rating_data.values, color='skyblue')
ax1.set_title('Netflix Content Ratings - Bar Chart')
ax1.set_xlabel('Rating')
ax1.set_ylabel('Count')
ax1.tick_params(axis='x', rotation=45)

# Add count labels on bars
for i, (rating, count) in enumerate(zip(rating_data.index, rating_data.values)):
    ax1.text(i, count + 5, str(count), ha='center')

# Pie chart
ax2.pie(rating_data.values, labels=rating_data.index, autopct='%1.1f%%', startangle=90)
ax2.set_title('Netflix Content Ratings - Distribution')

plt.tight_layout()
plt.savefig('charts/netflix_ratings_chart.png', dpi=300, bbox_inches='tight')
plt.close()

print("Ratings visualization created and saved!")

# Additional visualization - Content over time
plt.figure(figsize=(12, 6))
yearly_data = Netflix_shows_movies.groupby(['release_year', 'type']).size().unstack(fill_value=0)

# Filter for recent years (2000 onwards)
recent_data = yearly_data.loc[yearly_data.index >= 2000]

plt.stackplot(recent_data.index, 
              recent_data.get('Movie', 0), 
              recent_data.get('TV Show', 0),
              labels=['Movies', 'TV Shows'], 
              alpha=0.7)

plt.title('Netflix Content Production Over Time (2000-Present)')
plt.xlabel('Release Year')
plt.ylabel('Number of Titles')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('charts/netflix_timeline.png', dpi=300, bbox_inches='tight')
plt.close()

print("Timeline visualization created!")

# Summary statistics
print("\n" + "=" * 40)
print("ANALYSIS SUMMARY")
print("=" * 40)

print(f"Dataset processed: {len(Netflix_shows_movies)} titles")
print(f"Movies: {len(Netflix_shows_movies[Netflix_shows_movies['type'] == 'Movie'])}")
print(f"TV Shows: {len(Netflix_shows_movies[Netflix_shows_movies['type'] == 'TV Show'])}")

print(f"\nTop 5 genres:")
for i, (genre, count) in enumerate(list(top_genres.items())[:5], 1):
    print(f"{i}. {genre}: {count}")

print(f"\nMost common rating: {rating_data.index[0]} ({rating_data.iloc[0]} titles)")

# Save cleaned dataset
Netflix_shows_movies.to_csv('data/Netflix_shows_movies_cleaned.csv', index=False)
print(f"\nCleaned dataset saved as 'data/Netflix_shows_movies_cleaned.csv'")
print("Analysis complete!")
