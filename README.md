# Task_05_Descriptive_Stats
# 2024 Women's Lacrosse Statistics Analysis

This project explores player performance from the 2024 season of Syracuse University's Women’s Lacrosse team. The objective is to clean the dataset, compute descriptive and relational statistics, and visually answer performance-related questions using Python.

---

## Objectives

- Extract insights from raw season statistics
- Clean and standardize inconsistent data formats
- Generate descriptive statistics and visualizations
- Answer natural language questions using code
- Store LLM prompt comparisons (if applicable)

---

## Dataset Overview

- **Source**: [Syracuse University Athletics – Women’s Lacrosse](https://cuse.com)
- **Original Format**: PDF, then converted to `.xlsx`
- **Filename**: `2024 Women's Lacrosse Cumulative Statistics.xlsx`
- **Note**: This file is `.gitignore`-excluded

The dataset includes player names, games played, goals, assists, shots, ground balls, fouls, and other performance metrics.

---

## Data Cleaning Steps

The raw Excel file had several inconsistencies:

| Issue | Solution |
|-------|----------|
| `GP-GS` and `RC-YC-GC` columns were compound fields | Split them into separate fields or dropped |
| Last two rows were totals | Dropped using row filtering |
| Some columns had numeric strings | Converted to numeric with `errors='coerce'` |
| Name column formatting varied | Stripped extra whitespace and aligned |

```python
# Example cleaning steps
df[['GP', 'GS']] = df['GP-GS'].str.split('-', expand=True)
df = df.drop(columns=['GP-GS', 'RC-YC-GC'])
df = df[~df['Name'].str.contains("Total|Opponent", na=False)]
numeric_cols = ['G', 'A', 'SH', 'SH%', 'SOG%', 'DC', 'Fouls']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

Task_05_Descriptive_Stats/
├── analysis.py                  # Data loading & cleaning
├── visualizations.py           # Visualization script
├── des_stats.ipynb             # Optional Jupyter version
├── llm_prompts.md              # LLM-generated answers & comparisons
├── README.md                   # Project overview (this file)
├── .gitignore                  # Excludes dataset
├── visuals/                    # All output charts
│   ├── top_goal_scorers.png
│   ├── goals_vs_assists_corr.png
│   └── ...
