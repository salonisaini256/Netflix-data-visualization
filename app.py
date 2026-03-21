import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🎬 Netflix Analytics Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv('netflix_titles.csv')
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    return df

df = load_data()

# Sidebar - Country filter
st.sidebar.header("🔍 Filters")
selected_country = st.sidebar.selectbox("Select Country:", 
                                       df['country'].value_counts().head(10).index)

# Filter data by selected country
country_df = df[df['country'] == selected_country]

# Charts - NOW UPDATES with country selection!
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Titles", len(country_df))
    fig_pie = px.pie(country_df, names='type', title=f"{selected_country} Content")
    st.plotly_chart(fig_pie, width='stretch')

with col2:
    st.metric("Movies %", f"{(len(country_df[country_df['type']=='Movie'])/len(country_df)*100):.1f}%")

# Growth trend (all countries)
st.subheader("📈 Netflix Growth (All Countries)")
trend_data = df.dropna(subset=['year_added']).groupby('year_added').size().reset_index(name='count')
st.line_chart(trend_data.set_index('year_added'))