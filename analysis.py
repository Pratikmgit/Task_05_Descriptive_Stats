import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
file_path = "/workspaces/Task_05_Descriptive_Stats/2024 Women's Lacrosse Cumulative Statistics.xlsx"
df = pd.read_excel(file_path)

print(df.head())

# Split GP-GS into two columns
df[['GP', 'GS']] = df['GP-GS'].str.split('-', expand=True)

# Convert numeric columns to appropriate types
numeric_cols = ['GP', 'GS', 'G', 'A', 'PTS', 'SH', 'SH%', 'SOG', 'SOG%',
                'GWG', 'FPG', 'FPS', 'GB', 'TO', 'CT', 'DC', 'Fouls']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Optional: clean name format if needed
df['Name'] = df['Name'].str.strip()

# Drop rows where Name is 'Total' or 'Opponents'
df = df[~df['No'].isin(['Total', 'Opponents'])]

# Reset index after dropping
df.reset_index(drop=True, inplace=True)

# Drop unnecessary columns
df_cleaned = df.drop(columns=['GP-GS', 'RC-YC-GC'])
print(df_cleaned.head(20))


# Show summary stats
print("\n=== Summary Statistics ===")
print(df_cleaned[numeric_cols].describe())

# Top 10 by Goals
top_goals = df_cleaned.sort_values(by='G', ascending=False)[['No', 'Name', 'G']].head(10)
print("\nTop 10 Goal Scorers:")
print(top_goals)

# Top 10 by Points (PTS = G + A)
top_points = df_cleaned.sort_values(by='PTS', ascending=False)[['No', 'Name', 'PTS']].head(10)
print("\nTop 10 Point Scorers:")
print(top_points)

# Filter players with at least 10 shots
shooting_df = df_cleaned[df_cleaned['SH'] >= 10]

# Top 10 by Shooting %
top_shooters = shooting_df.sort_values(by='SH%', ascending=False)[['No', 'Name', 'SH', 'SH%']].head(10)
print("\nTop 10 Efficient Shooters (min 10 shots):")
print(top_shooters)


top_assists = df_cleaned.sort_values(by='A', ascending=False)[['No', 'Name', 'A']].head(10)
print("\nTop 10 Assisters:")
print(top_assists)


# Exclude players with 0 GP
discipline = df_cleaned[df_cleaned['GP'] > 0].sort_values(by='Fouls')[['No', 'Name', 'Fouls']].head(10)
print("\nTop 10 Most Disciplined Players:")
print(discipline)

top_gb = df_cleaned.sort_values(by='GB', ascending=False)[['No', 'Name', 'GB']].head(10)
top_ct = df_cleaned.sort_values(by='CT', ascending=False)[['No', 'Name', 'CT']].head(10)

print("\nTop 10 Ground Ball Collectors:")
print(top_gb)

print("\nTop 10 Caused Turnovers:")
print(top_ct)