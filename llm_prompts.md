# Research Task 05: Natural Language Querying with Python and LLMs

## Project Overview

This project explores how well natural language queries can be interpreted and answered using both:
- Python data analysis scripts
- Large Language Models (LLMs) like GPT-4

The dataset used is **2024 Syracuse Women’s Lacrosse Cumulative Statistics**, sourced from [cuse.com](https://cuse.com).

---

---

## 📌 Goals

- Clean and preprocess the dataset
- Run descriptive statistics and correlation analysis
- Answer 10 natural language questions with Python
- Evaluate how accurately an LLM can match the answers

---

## 🔟 Natural Language Questions Answered

| # | Question |
|---|----------|
| 1 | Who were the top goal scorers in the 2024 season? |
| 2 | Which players had the highest shooting percentage? |
| 3 | Which players had the most assists? |
| 4 | Which players participated in the most games (GP)? |
| 5 | Who were the most efficient shooters (high SH% with reasonable SH)? |
| 6 | Which players caused the most turnovers (CT)? |
| 7 | Which players had the highest ground balls (GB)? |
| 8 | Is there a relationship between goals scored and assists? |
| 9 | Is there a relationship between shots taken and shooting percentage? |
|10 | Do players with more draw controls (DC) tend to commit more fouls? |

All questions were successfully answered using:
- **Python (Pandas, Seaborn, Matplotlib)**
- **LLM (GPT-4)** with matching and correct logic

---

## 📈 Visualizations

Visual answers to the correlation-based questions are saved under `visuals/`:
- `goals_vs_assists.png`
- `shots_vs_shooting_pct.png`
- `draw_controls_vs_fouls.png`

---

## ✅ Outcome

This project demonstrates that:
- Python can reliably answer structured natural language queries.
- A well-tuned LLM can replicate the same answers with correct logic.
- Visuals help validate and interpret correlation questions effectively.

---

## 🛠️ Technologies Used

- Python 3.x  
- pandas, matplotlib, seaborn  
- Jupyter / VS Code / GitHub  
- GPT-4 (via ChatGPT)

---

## 📬 How to Run

1. Clone this repo  
2. Install dependencies  
   ```bash
   pip install pandas matplotlib seaborn openpyxl


    