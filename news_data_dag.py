# PLEASE NOTE: This is a copy of the python dag code

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
import pandas as pd
from newsdataapi import NewsDataApiClient
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
import json
import string
import logging


# Ensure necessary NLTK resources are available
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')

# Define the file paths
NEWS_DATA_CSV = '/home/ubuntu/airflow/tmp/news_data.csv'
TRANSFORMED_DATA_CSV = '/home/ubuntu/airflow/tmp/transformed_news_data.csv'

# Define DAG arguments and the DAG itself
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'news_data_pipeline',
    default_args=default_args,
    description='Fetch news data, transform it, and load into RDS.',
    schedule_interval=timedelta(hours=4),
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

def remove_existing_articles(df, conn_id='news_data_postgres_conn'):
    """
    Removes rows from the DataFrame if their title already exists in the database.
    """
    hook = PostgresHook(postgres_conn_id=conn_id)
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM news_articles")  # Adjusted to select titles
    existing_titles = {row[0] for row in cursor.fetchall()}  # Normalize titles for comparison
    # Filter DataFrame based on whether the lowercase, stripped title exists in the set of existing titles
    filtered_df = df[~df.title.isin(existing_titles)]
    return filtered_df

# Task 1: Fetch and Process News Data
def fetch_process_news_data(api_key, news_data_csv, transformed_data_csv):
    logging.info("Starting to fetch news data...")
    try:
        api = NewsDataApiClient(apikey=api_key)
        response = api.news_api(q='Colorado', language='en', country='us', scroll=True, max_result=100)
        
        # Initialize seen_ids as an empty set
        seen_ids = set()
        
        unique_articles = []
        for article in response['results']:
            if article['article_id'] not in seen_ids:
                unique_articles.append({
                    'article_id': article['article_id'],
                    'title': article['title'],
                    'link': article['link'],
                    'description': article['description'],
                    'pubDate': article['pubDate'],
                    'source_id': article['source_id'],
                    'category': json.dumps(article.get('category', []))
                })
                seen_ids.add(article['article_id'])

        df_raw = pd.DataFrame(unique_articles)
        df_raw.to_csv(news_data_csv, index=False)
        logging.info(f"Raw news data successfully saved to {news_data_csv}")
        
    except Exception as e:
        logging.error(f"Failed to fetch and process news data: {e}")
        return  # Important to return here to avoid executing the next part if the API call fails

    # Data transformation and sentiment analysis
    try:
        df = df_raw.copy()
        stop_words = set(stopwords.words('english')) | set(['colorado', 's']) | set(string.punctuation)
        lemmatizer = WordNetLemmatizer()
        sid = SentimentIntensityAnalyzer()

        df['clean_title'] = df['title'].apply(lambda x: x.lower())
        df['tokens'] = df['clean_title'].apply(word_tokenize)
        df['filtered_tokens'] = df['tokens'].apply(lambda x: [lemmatizer.lemmatize(word, pos='v') for word in x if word not in stop_words and word.isalpha()])
        df['tokens_json'] = df['filtered_tokens'].apply(json.dumps)
        df['sentiment_score'] = df['clean_title'].apply(lambda x: sid.polarity_scores(x)['compound'])
        df['sentiment'] = df['sentiment_score'].apply(lambda score: 'Positive' if score >= 0.05 else ('Negative' if score <= -0.05 else 'Neutral'))
        df.rename(columns={'pubDate': 'pubdate'}, inplace=True)

        df = df[['article_id', 'title', 'link', 'description', 'pubdate', 'source_id', 'sentiment_score', 'sentiment', 'tokens_json', 'category']]

        # Filter out articles that already exist in the database
        df_filtered = remove_existing_articles(df)
        print(f"The number of rows in df_filtered is: {df_filtered.shape[0]}")

        # Proceed with saving the filtered DataFrame and any subsequent logic
        df_filtered.to_csv(transformed_data_csv, index=False)
        logging.info(f"Filtered and transformed data saved to {transformed_data_csv}")
    except Exception as e:
        logging.error("Failed during data transformation and sentiment analysis: {}".format(e))


fetch_process_news_data_task = PythonOperator(
    task_id='fetch_process_news_data',
    python_callable=fetch_process_news_data,
    op_kwargs={
        'api_key': 'news_data_api_key',
        'news_data_csv': NEWS_DATA_CSV,
        'transformed_data_csv': TRANSFORMED_DATA_CSV,
    },
    dag=dag,
)

# Task 2: Load Processed Data to PostgreSQL
def load_news_data_to_postgres(transformed_data_csv: str):
    try:
        hook = PostgresHook(postgres_conn_id='news_data_postgres_conn')
        sql = "COPY news_articles(article_id, title, link, description, pubdate, source_id, sentiment_score, sentiment, tokens_json, category) FROM stdin WITH CSV HEADER DELIMITER as ','"
        hook.copy_expert(sql=sql, filename=transformed_data_csv)
        logging.info(f"Data successfully loaded into PostgreSQL from {transformed_data_csv}.")
    except Exception as e:
        logging.error(f"Error loading data to PostgreSQL: {e}")

load_to_postgres_task = PythonOperator(
    task_id='load_news_data_to_postgres',
    python_callable=load_news_data_to_postgres,
    op_kwargs={'transformed_data_csv': TRANSFORMED_DATA_CSV},
    dag=dag,
)

# Set task dependencies
fetch_process_news_data_task >> load_to_postgres_task
