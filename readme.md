# Netflix Data Analysis Project

## Project Overview

This project performs comprehensive data analysis on Netflix's content catalog using both Python and R programming languages. The analysis includes data cleaning, exploration, and visualization to understand content distribution patterns, ratings, and genre preferences within Netflix's streaming platform.

## Objectives

The analysis addresses the following requirements:

1. **Data Preparation**: Load dataset "Netflix_shows_movies".
2. **Data Cleaning**: Handle missing values systematically across all columns
3. **Data Exploration**: Perform statistical analysis and generate data summaries
4. **Data Visualization**: Create visualizations for genre distribution and content ratings
5. **R Integration**: Implement visualization components using R programming language

> While the requirement requires the data to be unzipped and renamed, the provided data is not in zipped format so I just renamed it manually.

**Generated Outputs:**

- charts/netflix_genres_chart.png (Python-generated)
- charts/netflix_ratings_chart.png (Python-generated)
- charts/netflix_timeline.png (Python-generated)
- charts/netflix_ratings_R_version.png (R-generated)
- charts/netflix_genres_R_version.png (R-generated)

## Technical Stack

### Python Libraries

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib**: Static plotting and visualization
- **seaborn**: Statistical data visualization
- **collections**: Data counting and processing utilities

### R Packages

- **ggplot2**: Grammar of graphics visualization
- **dplyr**: Data manipulation and transformation
- **readr**: Data reading utilities
- **viridis**: Color palettes for visualization

## Dataset Information

- **Source**: Netflix Movies and TV Shows Dataset
- **Dimensions**: 6,234 rows × 12 columns
- **Content**: Comprehensive information about Netflix titles including metadata

## Installation and Setup

### Prerequisites

- Python 3.7 or higher
- R 4.0 or higher
- RStudio (recommended for R development)

### Python Environment Setup

1. **Install Python dependencies**

```bash
pip3 install -r requirements.txt
```

2. **Verify dataset placement**
   Ensure `data/Netflix_shows_movies.csv` is located in the project root directory.

### R Environment Setup

1. **Install required R packages**

```r
R -e "install.packages(c('ggplot2', 'dplyr', 'readr', 'viridis'), repos='https://cran.r-project.org/')"
```

2. **Set working directory to project location**

## Execution Instructions

### Python Analysis

Execute the complete Python analysis:

```bash
python3 netflix_analysis.py
```

### R Analysis

```bash
R -e "source('netflix_analysis.R')"
```

## Analysis Results

### Dataset Characteristics

**Content Distribution:**

- Movies: Approximately 70% of catalog
- TV Shows: Approximately 30% of catalog

**Genre Analysis:**

- International Movies: Most prevalent category
- Dramas: Second most common genre
- Comedies: Significant representation
- International TV Shows: Growing category
- Documentaries: Substantial content volume

**Rating Distribution:**

- TV-MA: Most frequent rating classification
- TV-14: Second most common rating
- R-rated content: Significant movie category

**Geographic Distribution:**

- United States: Primary content producer
- India: Major international contributor
- Global content: Diverse international representation

**Temporal Analysis:**

- Peak production period: 2017-2019
- Recent trend: Increased TV show production
- Content span: Multiple decades of releases

### Visualization Components

#### Python-Generated Visualizations

1. **Genre Distribution**: Horizontal bar chart displaying top 15 genres
2. **Ratings Distribution**: Combined bar chart and pie chart visualization
3. **Content Timeline**: Stacked area chart showing production trends over time

#### R-Generated Visualizations

1. **Ratings Distribution**: Enhanced ggplot2 bar chart with percentage annotations
2. **Genre Distribution**: Alternative implementation using viridis color palette

## Data Quality Management

### Missing Value Treatment Strategy

**Systematic Approach Applied:**

- **Directors**: Replaced with "No Director Listed"
- **Cast Information**: Replaced with "No Cast Info"
- **Country Data**: Replaced with "Country Not Specified"
- **Date Information**: Replaced with "Date Unknown"
- **Rating Classifications**: Replaced with "Not Rated"
- **Duration Data**: Type-specific modal replacement
- **Genre Classifications**: Replaced with "Genre Not Listed"
- **Descriptions**: Replaced with "No description available"

### Data Validation

- Zero missing values in final cleaned dataset
- Consistent data type formatting
- Logical relationship validation
- No duplicate record identification
