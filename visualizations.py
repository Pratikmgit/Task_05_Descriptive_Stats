import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# File path to your Excel file
file_path = "/workspaces/Task_05_Descriptive_Stats/2024 Women's Lacrosse Cumulative Statistics.xlsx"

# Load dataset
df = pd.read_excel(file_path)

# Split 'GP-GS' column into 'GP' and 'GS'
df[['GP', 'GS']] = df['GP-GS'].str.split('-', expand=True)

# Convert all relevant columns to numeric
numeric_cols = ['GP', 'GS', 'G', 'A', 'PTS', 'SH', 'SH%', 'SOG', 'SOG%',
                'GWG', 'FPG', 'FPS', 'GB', 'TO', 'CT', 'DC', 'Fouls']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Drop summary rows
df = df[~df['No'].isin(['Total', 'Opponents'])].reset_index(drop=True)

# Drop unwanted columns
df = df.drop(columns=['GP-GS', 'RC-YC-GC'], errors='ignore')

# Create folder to save visuals
output_dir = "visuals"
os.makedirs(output_dir, exist_ok=True)

# Goals by Player
plt.figure(figsize=(12, 6))
top_goal_scorers = df.sort_values(by="G", ascending=False).head(10)
sns.barplot(data=top_goal_scorers, x="G", y="Name", palette="Blues_d")
plt.title("Top 10 Goal Scorers")
plt.xlabel("Goals")
plt.ylabel("Player")
plt.tight_layout()
plt.savefig(f"{output_dir}/top_goal_scorers.png")
plt.close()

# Assists by Player
plt.figure(figsize=(12, 6))
top_assist = df.sort_values(by="A", ascending=False).head(10)
sns.barplot(data=top_assist, x="A", y="Name", palette="Greens_d")
plt.title("Top 10 Assists")
plt.xlabel("Assists")
plt.ylabel("Player")
plt.tight_layout()
plt.savefig(f"{output_dir}/top_assist_providers.png")
plt.close()

# Shot Accuracy (SH%)
plt.figure(figsize=(12, 6))
df_sorted = df[df['SH%'].notnull()].sort_values(by='SH%', ascending=False).head(10)
sns.barplot(data=df_sorted, x='SH%', y='Name', palette='Purples_d')
plt.title("Top 10 Most Accurate Shooters (SH%)")
plt.xlabel("Shot Accuracy (%)")
plt.ylabel("Player")
plt.tight_layout()
plt.savefig(f"{output_dir}/most_accurate_shooters.png")
plt.close()

# Turnovers vs Ground Balls
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='TO', y='GB', hue='Name')
plt.title("Turnovers vs Ground Balls")
plt.xlabel("Turnovers")
plt.ylabel("Ground Balls")
plt.legend([],[], frameon=False)
plt.tight_layout()
plt.savefig(f"{output_dir}/turnovers_vs_groundballs.png")
plt.close()

# Face-off Win Impact (Draw Controls - DC)
plt.figure(figsize=(12, 6))
top_draws = df.sort_values(by='DC', ascending=False).head(10)
sns.barplot(data=top_draws, x='DC', y='Name', palette='Oranges_r')
plt.title("Top 10 Players by Draw Controls (DC)")
plt.xlabel("Draw Controls")
plt.ylabel("Player")
plt.tight_layout()
plt.savefig(f"{output_dir}/top_draw_controls.png")
plt.close()

# G vs A Correlation
plt.figure(figsize=(8, 6))
sns.regplot(data=df, x='G', y='A', scatter_kws={"s": 60}, line_kws={"color": "red"})
plt.title("Goals vs Assists")
plt.xlabel("Goals (G)")
plt.ylabel("Assists (A)")
plt.tight_layout()
plt.savefig(f"{output_dir}/goals_vs_assists_corr.png")
plt.close()

# SH vs SH% Correlation
plt.figure(figsize=(8, 6))
sns.regplot(data=df, x='SH', y='SH%', scatter_kws={"s": 60}, line_kws={"color": "green"})
plt.title("Shots vs Shooting Percentage")
plt.xlabel("Shots Taken (SH)")
plt.ylabel("Shooting % (SH%)")
plt.tight_layout()
plt.savefig(f"{output_dir}/shots_vs_sh_percent_corr.png")
plt.close()

# Draw Controls vs Fouls
plt.figure(figsize=(8, 6))
sns.regplot(data=df, x='DC', y='Fouls', scatter_kws={"s": 60}, line_kws={"color": "purple"})
plt.title("Draw Controls vs Fouls")
plt.xlabel("Draw Controls (DC)")
plt.ylabel("Fouls")
plt.tight_layout()
plt.savefig(f"{output_dir}/draw_controls_vs_fouls_corr.png")
plt.close()

print("\nCorrelation Coefficients:")
print(f"Goals vs Assists: {df['G'].corr(df['A']):.3f}")
print(f"Shots vs SH%: {df['SH'].corr(df['SH%']):.3f}")
print(f"Draw Controls vs Fouls: {df['DC'].corr(df['Fouls']):.3f}")

print("Visualizations created and saved in the 'visuals/' folder.")

