import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from config import sentiment_colors
from collections import Counter
from nltk import ngrams
import ast


def plot_sentiment_distribution(filtered_df):
    fig = px.histogram(filtered_df, x='sentiment', color='sentiment',
                        title='Sentiment Distribution',
                        labels={'sentiment': 'Sentiment'},
                        color_discrete_map=sentiment_colors)
    st.plotly_chart(fig)

def plot_sentiment_proportions(filtered_df):
    fig_pie = px.pie(filtered_df, names='sentiment', title='Sentiment Proportions',
                     color='sentiment',  
                     color_discrete_map=sentiment_colors) 
    st.plotly_chart(fig_pie)

def plot_hourly_sentiment_counts(filtered_df):
    # Group by 'pubdate' and 'sentiment', then count occurrences per hour
    hourly_sentiment = filtered_df.groupby([pd.Grouper(key='pubdate', freq='H'), 'sentiment']).size().reset_index(name='count')

    # Pivot the result to have separate columns for each sentiment
    hourly_sentiment_pivot = hourly_sentiment.pivot(index='pubdate', columns='sentiment', values='count').fillna(0)

    # Create the figure
    fig_hourly_sentiment_counts = go.Figure()

    # Add a trace for each sentiment category
    for sentiment, color in sentiment_colors.items():
        if sentiment in hourly_sentiment_pivot.columns:
            fig_hourly_sentiment_counts.add_trace(go.Scatter(
                x=hourly_sentiment_pivot.index, 
                y=hourly_sentiment_pivot[sentiment],
                mode='lines',
                name=sentiment,
                line=dict(color=color)
            ))

    # Update the layout
    fig_hourly_sentiment_counts.update_layout(
        title='Hourly Sentiment Counts',
        xaxis_title='Time',
        yaxis_title='Count',
        legend_title='Sentiment'
    )

    st.plotly_chart(fig_hourly_sentiment_counts)

def plot_source_distribution_by_sentiment(filtered_df):
    # Calculate sentiment counts for the filtered DataFrame
    sentiment_counts_filtered = filtered_df.groupby(['source_id', 'sentiment']).size().reset_index(name='counts')

    # Aggregate counts across sentiments for each source to identify the top 20 sources
    top_sources = sentiment_counts_filtered.groupby('source_id')['counts'].sum().sort_values(ascending=False).index

    # Filter the sentiment_counts_filtered DataFrame to include only the top 20 sources
    sentiment_counts_top_sources = sentiment_counts_filtered[sentiment_counts_filtered['source_id'].isin(top_sources)]

    # Create a stacked bar chart using the filtered sentiment counts
    fig_source_distribution_by_sentiment = px.bar(sentiment_counts_top_sources, x='source_id', y='counts', color='sentiment',
                 title='Source Distribution by Sentiment',
                 labels={'counts': 'Number of Articles', 'sentiment': 'Sentiment'},
                 text='counts',
                 color_discrete_map=sentiment_colors)  # Apply custom colors

    # Update layout for better readability
    fig_source_distribution_by_sentiment.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
    fig_source_distribution_by_sentiment.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    st.plotly_chart(fig_source_distribution_by_sentiment)

# In visualizations.py
def create_and_display_wordcloud(text_data):
    """
    Generates and displays a word cloud from the provided text data.

    Args:
    text_data (pd.Series or list): Text data from which to generate the word cloud.
    """
    st.subheader("WordCloud")
    # Combine all text items into a single string
    combined_text = ' '.join(text_data)

    # Generate the word cloud
    wordcloud = WordCloud(background_color='white', max_words=200, width=800, height=400).generate(combined_text)

    # Create a matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')  # Remove axis

    # Display the figure in Streamlit
    st.pyplot(fig)



def plot_ngram_frequencies_interactive(filtered_df):
    # Interactive Toggles for N-gram Visualization within the function
    st.header("N-gram Analysis")

    # Slider for selecting n-gram size
    n_size = st.slider('Select N-gram Size', min_value=1, max_value=3, value=2, key='ngram_size')

    # Slider for selecting the number of top n-grams to display
    top_n = st.slider('Select Number of Top N-grams', min_value=10, max_value=50, value=20, key='top_n')

    # Convert string representations of lists back to actual lists if needed
    token_lists = filtered_df['tokens_json'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    # Generate n-grams from the list of token lists using n_size for the n-gram size
    all_n_grams = [ngram for tokens in token_lists for ngram in ngrams(tokens, n_size)]

    # Count the frequency of each n-gram
    n_gram_freq = Counter(all_n_grams)

    # Select top n-grams
    top_n_grams = n_gram_freq.most_common(top_n)
    top_n_grams = [(' '.join(gram), freq) for gram, freq in top_n_grams]

    df_ngrams = pd.DataFrame(top_n_grams, columns=['n-gram', 'Frequency'])

    fig = px.bar(df_ngrams, x='n-gram', y='Frequency', title=f'Top {top_n} {n_size}-grams',
                 labels={'n-gram': f'{n_size}-gram', 'Frequency': 'Frequency'})

    st.plotly_chart(fig)


def plot_token_length_distribution(filtered_df):
    filtered_df['token_length'] = filtered_df['tokens_json'].apply(lambda x: len(ast.literal_eval(x)) if isinstance(x, str) else len(x))

    fig = px.histogram(filtered_df, x='token_length', title='Headline Length Distribution',
                       labels={'token_length': 'Number of Headline Words'},
                       color_discrete_sequence=['#636EFA'])  # Adjust the color as needed

    fig.update_xaxes(title_text='Number of Headline Words')
    fig.update_yaxes(title_text='Count')

    st.plotly_chart(fig)
