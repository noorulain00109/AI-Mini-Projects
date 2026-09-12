# MovieMatch | Movie Recommendation System

MovieMatch is a content-based movie recommendation system that recommends movies based on their similarity to a selected movie. The project uses Natural Language Processing and machine learning techniques to process movie metadata and generate recommendations.

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* NLTK
* Streamlit
* Requests
* Jupyter Notebook

## Project Setup

### Step 1: Create the Python Environment

Open PowerShell or Command Prompt in the project folder.

Check the Python version:

```bash
py --version
```

Create a virtual environment:

```bash
py -m venv venv
```

Activate the virtual environment:

```bash
.\venv\Scripts\activate
```

Install the required libraries:

```bash
pip install pandas numpy scikit-learn nltk streamlit requests
```

## Step 2: Download the Dataset

Download the **TMDB 5000 Movie Dataset** from Kaggle:

[TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata/data?select=tmdb_5000_movies.csv)

The dataset contains movie information such as titles, genres, keywords, cast, crew, overview, and other metadata.

## Step 3: Create the Project Structure

Create the following folders:

```text
MovieMatch/
│
├── data/
│   └── tmdb_5000_movies.csv
│
├── models/
│   ├── movies.pkl
│   └── similarity.pkl
│
├── notebook/
│   └── recommender.ipynb
│
├── app.py
├── requirements.txt
└── README.md
```

### Folder Description

**data/**
Contains the movie dataset downloaded from Kaggle.

**models/**
Contains the saved movie data and similarity matrix used by the recommendation system.

**notebook/**
Contains the Jupyter Notebook used for data preprocessing, feature engineering, model development, and testing.

**app.py**
Contains the Streamlit application.

## Step 4: Data Preprocessing

Open the Jupyter Notebook:

```text
notebook/recommender.ipynb
```

The notebook performs the following tasks:

1. Load the TMDB dataset.
2. Select relevant movie features.
3. Handle missing values.
4. Extract useful information from genres, keywords, cast, crew, and overview.
5. Combine relevant features into a single text representation.
6. Apply text preprocessing.
7. Convert the text data into numerical features.
8. Calculate similarity between movies.
9. Save the processed data and similarity matrix.

## Step 5: Feature Engineering

Relevant movie information is combined into a single feature representation.

For example:

```text
Genres + Keywords + Cast + Crew + Overview
```

This combined information is used to identify movies with similar characteristics.

## Step 6: Text Vectorization

The project uses **TF-IDF vectorization** to convert the processed movie information into numerical vectors.

TF-IDF helps identify important words and reduces the importance of commonly occurring words.

## Step 7: Calculate Movie Similarity

The project uses **Cosine Similarity** to calculate how similar movies are to each other.

The similarity scores are used to identify the most similar movies for a selected movie.

## Step 8: Save the Models

After processing the data and calculating similarity, save the required objects using Pickle.

Example:

```python
import pickle

with open("models/movies.pkl", "wb") as f:
    pickle.dump(movies, f)

with open("models/similarity.pkl", "wb") as f:
    pickle.dump(similarity, f)
```

Make sure the filenames and paths match those used in `app.py`.

## Step 9 — Run the Streamlit Application

Activate the virtual environment if it is not already active:

```bash
.\venv\Scripts\activate
```

Run the application:

```bash
streamlit run app.py
```

The Streamlit application will open in your browser.

## Features

* Search and select a movie
* Generate similar movie recommendations
* Select the number of recommendations
* Simple Streamlit interface
* Content-based recommendation approach
* Uses movie metadata for recommendations

## Project Objective

The objective of this project is to develop a practical movie recommendation system using machine learning and natural language processing techniques. The project demonstrates data preprocessing, feature engineering, text vectorization, similarity computation, model serialization, and deployment through Streamlit.
