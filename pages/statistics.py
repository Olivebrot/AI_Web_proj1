import streamlit as st
import pandas as pd
import os

# Load the dataset
@st.cache_data  # Streamlit caching for efficiency
def load_data():
    filepath = os.path.join(os.getcwd(), 'df1.csv')
    return pd.read_csv(filepath)

# Load data
df1 = load_data()



# First Visualization: Average number of guesses per country
st.write("### Average Number of Guesses Needed per Country")

# Calculate average guesses per country
avg_guesses = df1.groupby('country')['number_of_guesses'].mean().sort_values()

# Streamlit's built-in bar chart
st.bar_chart(avg_guesses)

# Second Visualization: Number of occurrences per country
st.write("### Number of Occurrences per Country")

# Count occurrences per country
country_counts = df1['country'].value_counts()

# Streamlit's built-in bar chart
st.bar_chart(country_counts)
