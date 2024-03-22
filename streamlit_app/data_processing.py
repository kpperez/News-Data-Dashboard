import streamlit as st
import pandas as pd
import ast
from sqlalchemy import create_engine
from config import mst

def create_db_engine():
    db_params = st.secrets["db"]
    engine_url = f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"
    return create_engine(engine_url)

def load_and_preprocess_data():
    engine = create_db_engine()
    df = pd.read_sql_query('SELECT * FROM news_articles', engine)
    df['pubdate'] = pd.to_datetime(df['pubdate'], utc=True).dt.tz_convert('MST')
    return df

def filter_by_sentiment(df, sentiment='All'):
    if sentiment == 'All':
        return df
    else:
        return df[df['sentiment'] == sentiment]


def safely_convert_to_list(row):
    try:
        if isinstance(row, str):
            return ast.literal_eval(row)  # Convert string to list
        elif isinstance(row, list):
            return row  # Already a list
        else:
            return []  # Fallback to an empty list
    except Exception as e:
        print(f"Error converting row: {e}")  # Log conversion errors
        return []
