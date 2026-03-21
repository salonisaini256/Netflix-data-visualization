import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno
import streamlit as st

df = pd.read_csv('netflix_titles.csv')
print("Shape:", df.shape)
print(df.head())
print(df.info())
msno.matrix(df)  # Missing data viz
# Cell 2: CLEAN DATA (Safe Version)
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year
df['rating'] = df['rating'].fillna('Not Rated')

# Extract duration numbers
df['duration_num'] = df['duration'].str.extract(r'(\d+)').astype(float)

print("✅ Cleaning COMPLETE!")
print("New columns added:")
print("- year_added")
print("- duration_num") 
print("\nFirst cleaned rows:")
print(df[['title', 'type', 'year_added', 'duration_num']].head())
# Cell 3: PIE CHART - Movies vs TV Shows
import plotly.express as px

fig = px.pie(df, names='type', 
             title='🍿 Netflix: Movies vs TV Shows Distribution',
             hole=0.3,  # Donut style
             color_discrete_map={'Movie':'#FF6B6B', 'TV Show':'#4ECDC4'})

fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()
# Cell 4: Top 10 Countries
top_countries = df['country'].value_counts().head(10)
fig2 = px.bar(x=top_countries.values, y=top_countries.index,
              title='🌍 Top 10 Countries by Netflix Content',
              orientation='h',  # Horizontal bar
              color=top_countries.values,
              color_continuous_scale='Viridis')
fig2.show()
# Cell 5: Netflix Growth Over Years
release_trend = df.groupby(['year_added', 'type']).size().unstack(fill_value=0)
fig5 = px.line(release_trend, title='📈 Netflix Content Growth (Movies vs TV Shows)')
fig5.update_xaxes(title='Year Added')
fig5.update_yaxes(title='Number of Titles')
fig5.show()
# Cell 6: Most Common Ratings
top_ratings = df['rating'].value_counts().head(10)
fig6 = px.bar(x=top_ratings.index, y=top_ratings.values,
              title='📺 Top 10 Netflix Ratings')
fig6.show()