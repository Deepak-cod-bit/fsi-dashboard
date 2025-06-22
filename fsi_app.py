import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#import all libries

st.set_page_config(page_title="FSI 2023 Dashboard", layout="wide")


st.markdown("""
<div style='background-color: green; padding: 15px; border-radius: 10px; text-align: center;'>
    <h1 style='color: teal;'> FSI 2023 DASHBOARD</h1>
    <p>This is a tool to analyze the Fragile States Index 2023 data. It allows users to select a country and view its FSI score, high-risk indicators, summary categories, and visualizations.</p>
</div>
""", unsafe_allow_html=True)


mll = pd.read_excel("FSI-2023-DOWNLOAD.xlsx")#mll is a name of the variable and import the excel file


country = st.sidebar.selectbox(" Select a Country", mll["Country"].unique())
row = mll[mll["Country"] == country].iloc[0]

#markdown is use for write the html code and style code in python
st.markdown(f"""
<div style="display: flex; align-items: center; margin-top: 30px;">
    <h2 style="color: white; font-family: 'Segoe UI', sans-serif; margin-right: 15px;">
        Analysis of
    </h2>
    <div style="
        background-color: #e6f2ff;
        color: #003366;
        padding: 8px 20px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 24px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    ">
        {country}
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div style="
    background-color: #003366;
    color: #ffffff;
    padding: 15px 30px;
    border-radius: 12px;
    text-align: center;
    font-size: 26px;
    font-weight: bold;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    margin: 20px auto;
    width: fit-content;
">
    Fragile States Index (FSI) Score: {:.2f}
</div>
""".format(row["Total"]), unsafe_allow_html=True)


st.subheader("🔴High Risk Indicators (Score > 9.0)")
for col in mll.columns[4:]:
    value = row[col]
    if pd.notna(value) and value > 9.0:
        st.write(f"**{col}**: {value:.2f}")


st.subheader("📋 Summary by Category")
st.markdown(f"""
- **Economic:**  
  - Economy: {row['E1: Economy']}  
  - Inequality: {row['E2: Economic Inequality']}  
- **Political:**  
  - Legitimacy: {row['P1: State Legitimacy']}  
  - Services: {row['P2: Public Services']}  
  - Rights: {row['P3: Human Rights']}  
- **Security:**  
  - Apparatus: {row['C1: Security Apparatus']}  
  - Elites: {row['C2: Factionalized Elites']}  
  - External: {row['X1: External Intervention']}
""")


st.subheader("📊 Indicator Correlation Heatmap")#heat6map
numeric_mll = mll.select_dtypes(include='number').drop(columns=['Year'])
correlation = numeric_mll.corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation, ax=ax, cmap="coolwarm", annot=True)
st.pyplot(fig)


st.subheader("🚨 Top 10 Most Fragile Countries")#top 10 count
top_10 = mll.sort_values(by="Total", ascending=False).head(10)
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_10, x="Total", y="Country", palette="Reds_d", ax=ax2)
ax2.set_title("Top 10 Most Fragile Countries")
st.pyplot(fig2)


st.subheader("📐 Statistical Summary of All Countries")
summary_df = numeric_mll.describe().T[["mean", "50%", "std"]]
summary_df.rename(columns={"50%": "median"}, inplace=True)
st.dataframe(summary_df.style.format("{:.2f}").background_gradient(cmap="Blues"))

st.subheader("📈 Distribution of Total FSI Scores")#distribution graph
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.histplot(data=mll, x="Total", bins=20, kde=True, color="skyblue", ax=ax3)
ax3.set_title("Distribution of Total Fragility Scores")
ax3.set_xlabel("FSI Total Score")
ax3.set_ylabel("Number of Countries")
st.pyplot(fig3)



st.subheader("📊 Country vs Global Average Across Indicators")
global_avg = numeric_mll.mean()
selected_scores = row[numeric_mll.columns]

fig4, ax4 = plt.subplots(figsize=(12, 6))
x = numeric_mll.columns
ax4.plot(x, global_avg, label='🌍 Global Avg', marker='o', linestyle='--')
ax4.plot(x, selected_scores, label=f'📌 {country}', marker='o')
ax4.set_xticks(range(len(x)))
ax4.set_xticklabels(x, rotation=45, ha="right")
ax4.set_title(f"{country} vs Global Average Across Indicators")
ax4.set_ylabel("Score")
ax4.grid(True, linestyle='--', alpha=0.5)
ax4.legend()
st.pyplot(fig4)
