import datetime
import streamlit as st
from data_processing import load_and_preprocess_data, filter_by_sentiment
from visualizations import (
    create_and_display_wordcloud,
    plot_hourly_sentiment_counts,
    plot_ngram_frequencies_interactive,
    plot_sentiment_distribution,
    plot_sentiment_proportions,
    plot_source_distribution_by_sentiment,
    plot_token_length_distribution,
)

def main():
    st.title("News Headline Dashboard \U0001F4F0")
    st.subheader("Sentiment and N-gram Analysis")
    news_data_url = "https://newsdata.io/"
    st.write(f"This data is sourced every 4 hours using the [News Data API]({news_data_url}) with a keyword search of **Colorado**.")
    st.image("streamlit_app/colorado-banner.png")
    github_url = "https://github.com/kpperez"
    st.write(f"Check out the full code and my other projects at [GitHub]({github_url})")

    # Load and preprocess data
    df = load_and_preprocess_data()

    # Sidebar Configuration
    st.sidebar.header("Filter Options")

    # Sentiment filter
    sentiment_choice = st.sidebar.selectbox(
        'Select Sentiment', 
        options=['All', 'Positive', 'Negative', 'Neutral'],
        key='sentiment_selectbox'
    )

    unique_sources = df['source_id'].dropna().unique()

    # Source filter
    source_choices = st.sidebar.multiselect(
        'Select Source',
        options=sorted(unique_sources),
        default=[],
        key='source_multiselect'
    )

    # Category filter
    all_categories = set(cat for sublist in df['category'].dropna() for cat in sublist)
    category_choices = st.sidebar.multiselect(
        'Select Category',
        options=sorted(all_categories),
        default=[],
        key='category_multiselect'
    )

    # Date range selection
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=[df['pubdate'].min(), df['pubdate'].max()],
        min_value=df['pubdate'].min(),
        max_value=df['pubdate'].max(),
        key='date_range_selectbox'
    )

    # Apply filters
    source_filtered_df = df[df['source_id'].isin(source_choices)] if source_choices else df

    if isinstance(date_range, (list, tuple)):
        start_date, end_date = date_range[0], date_range[-1]
    else:
        start_date = end_date = date_range
    date_filtered_df = source_filtered_df[
        (source_filtered_df['pubdate'].dt.date >= start_date) & 
        (source_filtered_df['pubdate'].dt.date <= end_date)
    ]

    if category_choices:
        category_filtered_df = date_filtered_df[
            date_filtered_df['category'].apply(lambda cats: any(cat in category_choices for cat in cats) if cats else False)
        ]
    else:
        category_filtered_df = date_filtered_df

    if sentiment_choice != 'All':
        filtered_df = filter_by_sentiment(category_filtered_df, sentiment=sentiment_choice)
    else:
        filtered_df = category_filtered_df

    # Visualization Calls
    if not filtered_df.empty:
        plot_sentiment_distribution(filtered_df)
        plot_sentiment_proportions(filtered_df)
        plot_hourly_sentiment_counts(filtered_df)
        plot_source_distribution_by_sentiment(filtered_df)

        # Prepare text for WordCloud
        filtered_df['json_text'] = filtered_df['tokens_json'].apply(lambda tokens: ' '.join(tokens) if isinstance(tokens, list) else ' ')
        create_and_display_wordcloud(filtered_df['json_text'])

        plot_ngram_frequencies_interactive(filtered_df)
        plot_token_length_distribution(filtered_df)

if __name__ == "__main__":
    main()
