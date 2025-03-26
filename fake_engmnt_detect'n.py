# -*- coding: utf-8 -*-
"""Fake Engmnt Detect'n.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LQ3-26oi37suVvFDJMOOt8a8e67Q_A9o

##Importing Lib
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.io as pio

"""##Dataset"""

df = pd.read_csv('/content/Top Influencer Data.csv')
df

"""#Data Exploration"""

# Checking the dataset shape (number of rows and columns)
df.shape

# Displaying summary statistics of numerical columns
df.describe()

# Checking for missing values
df.info()

# Checking for duplicate values
df.duplicated().sum()

# Checking for missing values
print("Missing values before cleaning:")
print(df.isna().sum())

print(df.columns)

print(df.isna().sum())

"""##Data Cleaning & Transformation"""

# Function to convert string based numerical values (10K, 2.5M) to actual numbers
def to_numeric(value):
    if isinstance(value, str):
        value = value.replace(",", "").lower()
        if "k" in value:
            return float(value.replace("k", "")) * 1e3
        elif "m" in value:
            return float(value.replace("m", "")) * 1e6
        elif "b" in value:
            return float(value.replace("b", "")) * 1e9
        elif "%" in value:
            return float(value.replace("%", "")) / 100
    try:
        return float(value)
    except ValueError:
        return None

"""Removeing top 1% outliers in engagement rate"""

# Converting relevant columns to numeric values
cols = ['followers', 'avg_likes', '60_day_eng_rate', 'new_post_avg_like', 'total_likes']
for col in cols:
    df[col] = df[col].apply(to_numeric)
# Dropping any remaining rows with missing values in important columns
df = df.dropna(subset=cols)
# Removing the top 1% outliers in engagement rate to avoid misleading trends
f = df[df['60_day_eng_rate'] < df['60_day_eng_rate'].quantile(0.99)]

"""Categorizing Influencers"""

# Function to classify influencers based on their follower count
def influencer_category(followers):
    if followers < 10_000:
        return "Nano"
    elif followers < 100_000:
        return "Micro"
    elif followers < 1_000_000:
        return "Macro"
    else:
        return "Celebrity"

# Creating a new column to store influencer categories
df['Category'] = df['followers'].apply(influencer_category)

"""#Visualisation"""

pio.templates.default = "plotly_dark"

"""#Scatter Plot: Followers vs. Engagement Rate"""

fig = px.scatter(df, x='followers', y=df['60_day_eng_rate'] * 100,
                 title='Followers vs. Engagement Rate',
                 log_x=True, opacity=0.6, size_max=5, color='Category',
                 labels={'followers': 'Number of Followers',
                         '60_day_eng_rate': 'Engagement Rate (%)'},
                 color_discrete_sequence=px.colors.qualitative.Set2)

# Trend Line
z = np.polyfit(np.log10(df['followers']), df['60_day_eng_rate'], 2)
df['poly_trend'] = np.poly1d(z)(np.log10(df['followers'])) * 100
fig.add_scatter(x=df['followers'], y=df['poly_trend'], mode='lines',
                line=dict(color='red', width=2), name='Trend Line')

fig.show()

"""#Histogram Likes:Follower"""

fig = px.histogram(df, x=(df['avg_likes'] / df['followers']) * 100, nbins=30,
                   title='Histogram of Like-to-Follower Ratio',
                   color_discrete_sequence=['cyan'],
                   template='plotly_dark')

fig.update_layout(xaxis_title='Like-to-Follower Ratio (%)', yaxis_title='Frequency')
fig.show()

"""#KDE Plot Like:Follower"""

fig = px.violin(df, x=(df['avg_likes'] / df['followers']) * 100,
                title='KDE of Like-to-Follower Ratio',
                color_discrete_sequence=['cyan'],
                template='plotly_dark')

fig.update_layout(xaxis_title='Like-to-Follower Ratio (%)', yaxis_title='Density')
fig.show()

"""# Bar Chart - Only Top 10 Categories"""

category_avg = df.groupby('country')['60_day_eng_rate'].mean().sort_values(ascending=False).head(10)

fig = px.bar(category_avg, x=category_avg.index, y=category_avg.values * 100,
             title='Top 10 Countries by Engagement Rate',
             color_discrete_sequence=['cyan'], template='plotly_dark')

fig.update_layout(xaxis_title='Country', yaxis_title='Average Engagement Rate (%)',
                  xaxis_tickangle=-30, yaxis_tickformat=".2f%%",
                  bargap=0.2)

fig.show()

"""# Heatmap Like Vs Comments"""

corr_matrix = df[['avg_likes', 'new_post_avg_like', 'total_likes']].corr().reset_index().melt('index')

fig = px.imshow(corr_matrix.pivot(index='index', columns='variable', values='value'),
                text_auto=".2f", color_continuous_scale='Blues',
                title='Heatmap of Like vs. Comments Correlation',
                template='plotly_dark')

fig.show()
