import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Load the dataset (without caching)
def load_data():
    filepath = os.path.join(os.getcwd(), 'df1.csv')
    return pd.read_csv(filepath)

# Load data
df1 = load_data()

# First Visualization: Average number of guesses per country
st.write("### Average Number of Guesses Needed per Country")

# Calculate average guesses per country
avg_guesses = df1.groupby('country')['number_of_guesses'].mean().reset_index().sort_values(by='number_of_guesses')

# Create an interactive bar chart with Plotly
fig_avg = px.bar(
    avg_guesses,
    x='number_of_guesses',
    y='country',
    orientation='h',
    labels={'number_of_guesses': 'Average Guesses', 'country': 'Country'},
    title='Average Number of Guesses Needed per Country',
    color='number_of_guesses',
    color_continuous_scale='viridis'
)
st.plotly_chart(fig_avg)

# Second Visualization: Number of occurrences per country
st.write("### Number of Occurrences per Country")

# Count occurrences per country
country_counts = df1['country'].value_counts().reset_index()
country_counts.columns = ['country', 'count']

# Create an interactive bar chart with Plotly
fig_count = px.bar(
    country_counts,
    x='count',
    y='country',
    orientation='h',
    labels={'count': 'Occurrences', 'country': 'Country'},
    title='Number of Occurrences per Country',
    color='count',
    color_continuous_scale='viridis'
)
st.plotly_chart(fig_count)


