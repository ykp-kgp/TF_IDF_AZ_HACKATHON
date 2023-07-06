# LeetCode Query Search

LeetCode Query Search is a web application that allows users to search for relevant LeetCode questions based on their queries. The application uses a TF-IDF model trained on a dataset of LeetCode questions to match the user's query with the most relevant questions.

## Features

- Scrapes LeetCode question data using Selenium
- Trains a TF-IDF model on the question dataset
- Performs NLP processing to filter relevant words based on user queries
- Matches the top 20 results from the dataset based on the filtered words
- Provides a web interface for users to enter their queries and view the results

## Technologies Used

- Python
- Selenium
- Flask
- scikit-learn (for TF-IDF implementation)
- HTML/CSS (for the web interface)

Repository: https://github.com/ykp-kgp/TF_IDF_AZ_HACKATHON

