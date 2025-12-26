# VideoGameRecommender

End-to-end video game recommendation system built using real Steam data.  
This project covers the full data science lifecycle, from raw data ingestion to model deployment through a REST API.

---

## 📌 Overview

VideoGameRecommender is a machine learning–based system designed to generate personalized video game recommendations.  
It integrates data engineering, feature engineering, model training, and API deployment into a reproducible and modular pipeline.

---

## 🧱 Project Architecture

```
EDA/ # Exploratory Data Analysis
ETL/ # Data extraction and transformation
Feature Engineering/ # Sentiment analysis
ML/ # Model training and inference
data/ # Raw datasets
functions/ # Reusable ETL and EDA functions
src/
├── CSV/ # Processed data (CSV)
└── Parquet/ # Processed data (Parquet)
main.py # FastAPI application
requirements.txt
```


---

## ⚙️ Technologies

- Python
- Pandas, NumPy
- Scikit-learn
- FastAPI & Uvicorn
- Parquet
- Joblib
- Jupyter Notebooks

---

## 🧠 Methodology

- **ETL:** cleaning, normalization, and optimization of raw Steam datasets.
- **EDA:** manual exploratory analysis to identify patterns and relationships.
- **Feature Engineering:** sentiment analysis on user reviews.
- **Machine Learning:** item-item recommendation model using cosine similarity.
- **API:** RESTful API exposing analytical insights and recommendations.

---

## 🚀 How to Run

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run API

```bash
uvicorn main:app --reload
```

Access:

- API root: http://localhost:8000
- Interactive docs: http://localhost:8000/docs

## 🔍 API Endpoints

- /developer/{developer}
- /userdata/{user_id}
- /UserForGenre/{genre}
- /best_developer_year/{year}
- /developer_reviews_analysis/{developer}
- /recomendacion_juego/{id}

## 📊 Data Source

All datasets were extracted from Steam APIs, including games, users, and reviews.

## 🎯 Project Scope

This project was designed as a functional MVP, prioritizing clarity, reproducibility, and real-world applicability over over-engineering.

## 👤 Author

Agostina Ailén Fernández Rodríguez
