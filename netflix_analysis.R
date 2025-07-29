pdf(NULL)


library(ggplot2)
library(dplyr)
library(readr)
library(viridis)

cat("Starting R analysis of Netflix data...\n")

if (file.exists("data/Netflix_shows_movies.csv")) {
  netflix_data <- read_csv("data/Netflix_shows_movies.csv")
  cat("Loaded original dataset - will do basic cleaning\n")
  
  # Quick cleaning
  netflix_data$director[is.na(netflix_data$director)] <- "Unknown"
  netflix_data$cast[is.na(netflix_data$cast)] <- "Unknown"
  netflix_data$country[is.na(netflix_data$country)] <- "Unknown"
  netflix_data$rating[is.na(netflix_data$rating)] <- "Not Rated"
  netflix_data$listed_in[is.na(netflix_data$listed_in)] <- "Unknown"
} else {
  stop("Cannot find dataset file!")
}

cat(paste("Dataset has", nrow(netflix_data), "rows and", ncol(netflix_data), "columns\n"))

cat("Creating ratings visualization...\n")

ratings_summary <- netflix_data %>%
  count(rating, sort = TRUE) %>%
  mutate(percentage = n / sum(n) * 100)

# Create ggplot visualization
ratings_plot <- ggplot(ratings_summary, aes(x = reorder(rating, n), y = n, fill = rating)) +
  geom_col(width = 0.8, alpha = 0.8) +
  geom_text(aes(label = paste(n, "\n(", round(percentage, 1), "%)", sep = "")), 
            hjust = -0.1, size = 3) +
  coord_flip() +
  labs(title = "Netflix Content Rating Distribution",
       subtitle = "Analysis using R and ggplot2",
       x = "Content Rating",
       y = "Number of Titles") +
  theme_minimal() +
  theme(plot.title = element_text(size = 14, face = "bold"),
        plot.subtitle = element_text(size = 11),
        axis.title = element_text(size = 11),
        legend.position = "none") +
  scale_fill_viridis_d()

print(ratings_plot)

ggsave("charts/netflix_ratings_R_version.png", ratings_plot, width = 10, height = 6, dpi = 300)
cat("Ratings plot saved as charts/netflix_ratings_R_version.png\n")

cat("Creating genre analysis...\n")

all_genres <- c()
for (i in 1:nrow(netflix_data)) {
  if (!is.na(netflix_data$listed_in[i])) {
    genres <- strsplit(as.character(netflix_data$listed_in[i]), ",")[[1]]
    genres <- trimws(genres)  # Remove whitespace
    all_genres <- c(all_genres, genres)
  }
}

# Count and get top genres
genre_counts <- table(all_genres)
genre_counts <- sort(genre_counts, decreasing = TRUE)
top_genres <- head(genre_counts, 12)  # Top 12 for better display

# Create data frame for plotting
genres_expanded <- data.frame(
  listed_in = names(top_genres),
  n = as.numeric(top_genres)
) %>%
  mutate(listed_in = reorder(listed_in, n))

# Create genre plot
genre_plot <- ggplot(genres_expanded, aes(x = listed_in, y = n)) +
  geom_col(fill = "steelblue", alpha = 0.7) +
  geom_text(aes(label = n), hjust = -0.2, size = 3) +
  coord_flip() +
  labs(title = "Top Netflix Genres",
       x = "Genre",
       y = "Number of Titles") +
  theme_minimal() +
  theme(plot.title = element_text(size = 14, face = "bold"))

print(genre_plot)
ggsave("charts/netflix_genres_R_version.png", genre_plot, width = 10, height = 6, dpi = 300)
cat("Genre plot saved as charts/netflix_genres_R_version.png\n")

cat("\n--- R ANALYSIS SUMMARY ---\n")
cat(paste("Total titles analyzed:", nrow(netflix_data), "\n"))

movie_count <- sum(netflix_data$type == "Movie", na.rm = TRUE)
tv_count <- sum(netflix_data$type == "TV Show", na.rm = TRUE)

cat(paste("Movies:", movie_count, "(", round(movie_count/nrow(netflix_data)*100, 1), "%)\n"))
cat(paste("TV Shows:", tv_count, "(", round(tv_count/nrow(netflix_data)*100, 1), "%)\n"))

cat("\nTop 5 ratings:\n")
top_ratings <- head(ratings_summary, 5)
for(i in 1:nrow(top_ratings)) {
  cat(paste(i, ".", top_ratings$rating[i], ":", top_ratings$n[i], "titles\n"))
}

cat("\nFiles created:\n")
cat("- charts/netflix_ratings_R_version.png\n")
cat("- charts/netflix_genres_R_version.png\n")

cat("\nR analysis completed!\n")
