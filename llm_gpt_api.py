import os
import json
import time
from datetime import datetime
import pandas as pd


DATA_PATH = "/workspaces/Task_05_Descriptive_Stats/2024 Women's Lacrosse Cumulative Statistics.xlsx"
MODEL = "gpt-4o-mini"   
TEMPERATURE = 0.2
MAX_TOKENS = 900
RESULTS_MD = "llm_deep_analysis_results.md"

df = pd.read_excel(DATA_PATH)

# Remove summary rows
df = df[~df["Name"].isin(["Total", "Opponents"])].copy()

# Split GP-GS, coerce to numeric
df[["GP", "GS"]] = df["GP-GS"].astype(str).str.split("-", expand=True)
numeric_cols = [
    "GP","GS","G","A","PTS","SH","SH%","SOG","SOG%","GWG","FPG","FPS","GB","TO","CT","DC","Fouls"
]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

# Per-game helpers (adds signal for deeper analysis)
df["PTS_per_GP"] = (df["PTS"] / df["GP"]).round(3)
df["GB_per_GP"]  = (df["GB"]  / df["GP"]).round(3)
df["CT_per_GP"]  = (df["CT"]  / df["GP"]).round(3)
df["TO_per_GP"]  = (df["TO"]  / df["GP"]).round(3)


facts = {}

# Team summaries (rounded to reduce tokens)
facts["team_totals"] = df[numeric_cols].sum(numeric_only=True).round(3).to_dict()
facts["team_means"]  = df[numeric_cols].mean(numeric_only=True).round(3).to_dict()

# Key correlations
def safe_corr(cols):
    c = df[cols].corr().iloc[0,1]
    return None if pd.isna(c) else round(float(c), 3)

facts["correlations"] = {
    "G_A":      safe_corr(["G","A"]),
    "SH_SHP":   safe_corr(["SH","SH%"]),
    "DC_Fouls": safe_corr(["DC","Fouls"]),
    "PTS_G":    safe_corr(["PTS","G"]),
    "PTS_A":    safe_corr(["PTS","A"]),
}

# Top lists (include names)
def top(df_, col, n=8, min_shots=None):
    sub = df_.copy()
    if min_shots is not None:
        sub = sub[sub["SH"] >= min_shots]
    cols = ["Name", col]
    return sub[cols].sort_values(by=col, ascending=False).head(n).to_dict(orient="records")

facts["leaders"] = {
    "G":      top(df, "G"),
    "A":      top(df, "A"),
    "PTS":    top(df, "PTS"),
    "SH%_vol": top(df, "SH%", min_shots=20),
    "GB":     top(df, "GB"),
    "CT":     top(df, "CT"),
    "DC":     top(df, "DC"),
}

# A small player slice with key fields (limit to top 20 by PTS to save tokens)
keep_cols = ["Name","GP","GS","G","A","PTS","PTS_per_GP","SH","SH%","GB","GB_per_GP","CT","CT_per_GP","TO","TO_per_GP","DC","Fouls"]
facts["players_sample"] = df[keep_cols].sort_values("PTS", ascending=False).head(20).to_dict(orient="records")

# Questions for Deeper Analyis
QUESTIONS = [
    "Which single player's targeted improvement would most likely add two extra wins next season? Justify using efficiency (SH%), usage (SH), turnovers (TO), and per-game impact (PTS_per_GP, CT_per_GP, GB_per_GP). Propose specific numeric targets.",
    "Is scoring more constrained by shot volume or by finishing? Use correlations and extremes (top/bottom shooters by SH and SH%). Recommend which lever to prioritize and by how much.",
    "Choose one offensive KPI and one defensive KPI that would yield the biggest win impact if improved. Propose realistic team targets and the players who most influence each KPI.",
    "Construct a simple two-way index = 0.5*(standardized PTS_per_GP) + 0.25*(standardized GB_per_GP) + 0.25*(standardized CT_per_GP). Based on the provided sample, who ranks highest and why?",
    "Identify high-volume, high-efficiency scorers using a criterion that balances SH and SH%. Name the best candidate and one under-the-radar secondary option.",
    "If the staff focuses on Draw Controls (DC), which player’s development could increase DC while keeping fouls controlled? Explain the tradeoff and set numeric targets.",
    "What profile tends to commit more turnovers? Characterize with relationships among GP, PTS, SH, and CT, and recommend coaching interventions.",
    "Suggest one role or lineup adjustment (e.g., primary finisher vs creator) to add ~5–10% team points. Ground the suggestion in the stats and list risks.",
    "Spot outliers in SH% vs SH (positive and negative). For each, give a coaching action: scale up usage, reallocate shots, or change shot selection.",
    "Propose a concise 3-point development plan for the offseason with measurable targets tied to current weaknesses and the correlations provided."
]


from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = (
    "You are a sports analytics assistant. Use ONLY the provided data to answer. "
    "If a fact isn’t in the data, state that it cannot be verified. Be specific and quantitative. "
    "Prefer bullet points. Include concrete numeric targets when recommending actions."
)

def ask_llm(question: str, facts_pack: dict) -> str:
    user_payload = {
        "question": question,
        "data_facts": facts_pack,
    }
    resp = client.chat.completions.create(
        model=MODEL,
        temperature=TEMPERATURE,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(user_payload)}
        ],
        max_tokens=MAX_TOKENS,
    )
    return resp.choices[0].message.content.strip()


def main():
    started = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    with open(RESULTS_MD, "w", encoding="utf-8") as f:
        f.write(f"# LLM Deep Analysis Results (Model: {MODEL})\n\n")
        f.write(f"_Run: {started}_\n\n")

        for i, q in enumerate(QUESTIONS, start=1):
            print(f"\nQ{i}: {q}\n")
            answer = ask_llm(q, facts)
            print(answer[:800] + ("\n..." if len(answer) > 800 else ""))
            f.write(f"## Q{i}. {q}\n\n")
            f.write(answer + "\n\n---\n")
            time.sleep(0.6)  # light pacing

    print(f"\nSaved answers to: {RESULTS_MD}")

if __name__ == "__main__":
    main()

