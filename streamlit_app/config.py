import pytz

# Adjust the timezone of start_date and end_date to MST
mst = pytz.timezone('MST')

# Define the color palette for sentiments
sentiment_colors = {
    'Negative': '#FF0000',  # Red
    'Neutral': '#808080',  # Gray
    'Positive': '#008000'   # Green
}
